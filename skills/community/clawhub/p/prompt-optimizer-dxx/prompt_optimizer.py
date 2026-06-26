#!/usr/bin/env python3
"""
Prompt Optimizer Skill - Prompt 优化器 v3.1 (重构版)
支持全类型任务优化 + 配置文件 + LRU 缓存 + 日志系统

CLI 用法:
    python prompt_optimizer.py "帮我写个排序"
    python prompt_optimizer.py --json "帮我写个排序"
    python prompt_optimizer.py --file input.txt
    python -m prompt_optimizer "帮我写个排序"

Python 调用:
    from prompt_optimizer import PromptOptimizer
    optimizer = PromptOptimizer()
    result = optimizer.optimize("帮我写个排序")
"""

import re
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import OrderedDict

# 导入配置数据
from config_data import (
    __version__,
    DEFAULT_CONFIG,
    TASK_PATTERNS,
    LANGUAGE_PATTERNS,
    FORMAT_PATTERNS,
    STYLE_PATTERNS,
)


# ============ 版本信息 ============
__all__ = ["__version__", "PromptOptimizer", "OptimizationResult", "optimize_prompt"]


# ============ 日志配置 ============

def setup_logger(name: str = "prompt_optimizer", level: int = logging.INFO) -> logging.Logger:
    """设置日志器"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s │ %(levelname)-8s │ %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


logger = setup_logger()


# ============ LRU 缓存 ============

class LRUCache:
    """简单的 LRU 缓存实现"""
    
    def __init__(self, maxsize: int = 128):
        self.cache: OrderedDict = OrderedDict()
        self.maxsize = maxsize
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[str]:
        """获取缓存"""
        if key in self.cache:
            self.hits += 1
            self.cache.move_to_end(key)
            logger.debug(f"📦 缓存命中: {key[:20]}...")
            return self.cache[key]
        self.misses += 1
        return None
    
    def set(self, key: str, value: str):
        """设置缓存"""
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info("🗑️ 缓存已清空")
    
    def stats(self) -> dict:
        """缓存统计"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "size": len(self.cache),
            "maxsize": self.maxsize,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1f}%"
        }


# 全局缓存
_prompt_cache = LRUCache(maxsize=128)


# ============ 结果类 ============

@dataclass
class OptimizationResult:
    """优化结果"""
    original: str           # 原始 prompt
    optimized: str          # 优化后 prompt
    task_type: str          # 任务类型
    missing_info: List[str] # 缺失信息
    enhancements: List[str] # 增强项
    timestamp: str          # 时间戳
    cached: bool = False    # 是否命中缓存
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ============ 优化器核心 ============

class PromptOptimizer:
    """Prompt 优化器 - 重构版"""
    
    def __init__(self, config_path: Optional[str] = None, use_cache: bool = True):
        """
        初始化优化器
        
        Args:
            config_path: 配置文件路径（可选）
            use_cache: 是否启用缓存（默认启用）
        """
        self.config_path = config_path
        self.config = self._deep_copy(DEFAULT_CONFIG)
        self.use_cache = use_cache
        
        # 预编译模式
        self._compiled_patterns: Dict[str, List[tuple]] = {}
        self._sorted_patterns: List[tuple] = []
        
        self._load_config()
        self._compile_patterns()
        
        logger.info(f"🚀 Prompt Optimizer v{__version__} 初始化完成")
        logger.info(f"   任务类型: {len(self.config['task_patterns'])} 种")
        logger.info(f"   缓存: {'启用' if use_cache else '禁用'}")
    
    @staticmethod
    def _deep_copy(data: dict) -> dict:
        """深度复制配置"""
        import copy
        return copy.deepcopy(data)
    
    def _load_config(self):
        """加载配置文件"""
        if self.config_path and Path(self.config_path).exists():
            try:
                import yaml
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_config = yaml.safe_load(f)
                
                self._merge_config(self.config, user_config)
                logger.info(f"📄 已加载配置文件: {self.config_path}")
            except ImportError:
                logger.warning("⚠️ PyYAML 未安装，使用默认配置")
            except Exception as e:
                logger.warning(f"⚠️ 配置文件加载失败: {e}, 使用默认配置")
        
        # 应用缓存设置
        if "cache" in self.config:
            global _prompt_cache
            _prompt_cache.maxsize = self.config["cache"].get("maxsize", 128)
    
    def _merge_config(self, base: dict, update: dict):
        """深度合并配置"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def _compile_patterns(self):
        """预编译关键词模式"""
        logger.debug("🔧 预编译关键词模式...")
        
        self._compiled_patterns = {}
        for task_type, config in self.config["task_patterns"].items():
            if task_type == "通用任务":
                continue
            keywords = config.get("keywords", [])
            priority = config.get("priority", 5)
            self._compiled_patterns[task_type] = [
                (priority, kw.lower(), task_type) 
                for kw in keywords
            ]
        
        all_patterns = []
        for task_type, patterns in self._compiled_patterns.items():
            all_patterns.extend(patterns)
        all_patterns.sort(key=lambda x: -x[0])
        self._sorted_patterns = all_patterns
    
    def _get_cache_key(self, prompt: str) -> str:
        """生成缓存 key"""
        import hashlib
        return hashlib.md5(prompt.strip().encode()).hexdigest()
    
    def optimize(self, prompt: str, use_cache: Optional[bool] = None) -> OptimizationResult:
        """优化 prompt"""
        # 错误处理
        if not prompt:
            raise ValueError("Prompt 不能为空")
        
        if not prompt.strip():
            raise ValueError("Prompt 不能只包含空白字符")
        
        cache_enabled = self.use_cache if use_cache is None else use_cache
        
        # 检查缓存
        if cache_enabled:
            cache_key = self._get_cache_key(prompt)
            cached_result = _prompt_cache.get(cache_key)
            if cached_result:
                task_type = self._detect_task_type(prompt.strip())
                missing_info = self._detect_missing_info(prompt.strip(), task_type)
                return OptimizationResult(
                    original=prompt.strip(),
                    optimized=cached_result,
                    task_type=task_type,
                    missing_info=missing_info,
                    enhancements=["基本格式优化"],
                    timestamp=datetime.now().isoformat(),
                    cached=True
                )
        
        original = prompt.strip()
        
        try:
            task_type = self._detect_task_type(original)
            missing_info = self._detect_missing_info(original, task_type)
            optimized = self._apply_enhancements(original, task_type, missing_info)
            enhancements = self._generate_enhancements(original, optimized)
            
            result = OptimizationResult(
                original=original,
                optimized=optimized,
                task_type=task_type,
                missing_info=missing_info,
                enhancements=enhancements,
                timestamp=datetime.now().isoformat(),
                cached=False
            )
            
            if cache_enabled:
                _prompt_cache.set(cache_key, optimized)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ 优化失败: {e}")
            raise RuntimeError(f"优化失败: {str(e)}") from e
    
    def _detect_task_type(self, prompt: str) -> str:
        """检测任务类型"""
        prompt_lower = prompt.lower()
        
        for priority, keyword, task_type in self._sorted_patterns:
            if keyword in prompt_lower:
                return task_type
        
        return "通用任务"
    
    def _detect_missing_info(self, prompt: str, task_type: str) -> List[str]:
        """检测缺失信息"""
        missing = []
        prompt_lower = prompt.lower()
        
        # 检测编程语言
        if task_type in ["写代码", "改写代码", "代码审查"]:
            all_langs = [lang for langs in self.config["language_patterns"].values() for lang in langs]
            if not any(lang in prompt_lower for lang in all_langs):
                missing.append("编程语言")
        
        # 检测输出格式
        all_formats = [fmt for fmts in self.config["format_patterns"].values() for fmt in fmts]
        if not any(fmt in prompt_lower for fmt in all_formats):
            missing.append("输出格式")
        
        # 检测风格
        all_styles = [s for styles in self.config["style_patterns"].values() for s in styles]
        if not any(s in prompt_lower for s in all_styles):
            missing.append("风格")
        
        # 检测具体细节
        if len(prompt) < 8:
            missing.append("具体需求描述")
        
        # 检测示例
        if task_type in ["写代码", "改写代码"]:
            if not any(x in prompt for x in ["例如", "比如", "示例", "输入"]):
                missing.append("输入输出示例")
        
        # 检测数量
        if task_type == "头脑风暴":
            if not any(x in prompt for x in ["个", "几条", "几个"]):
                missing.append("数量要求")
        
        # 检测字数
        if task_type in ["写文案", "总结摘要"]:
            if not any(x in prompt for x in ["字", "字数", "词"]):
                missing.append("字数要求")
        
        return missing
    
    def _apply_enhancements(self, prompt: str, task_type: str, missing_info: List[str]) -> str:
        """应用增强"""
        patterns = self.config["task_patterns"]
        config = patterns.get(task_type, patterns.get("通用任务", {
            "enhancements": ["请直接输出结果，用合适的格式"]
        }))
        enhancements = config.get("enhancements", [])
        
        enhanced_parts = []
        
        if enhancements:
            enhanced_parts.append(enhancements[0])
        
        enhanced_parts.append(prompt)
        
        for enhancement in enhancements[1:]:
            enhanced_parts.append(enhancement)
        
        # 补全缺失信息
        if "输出格式" in missing_info:
            enhanced_parts.append("请用 Markdown 格式输出")
        
        if "编程语言" in missing_info:
            enhanced_parts.append("(请用 Python 实现)")
        
        if "输入输出示例" in missing_info:
            enhanced_parts.append("请提供一个简单的示例")
        
        if "数量要求" in missing_info:
            enhanced_parts.append("请提供至少 5 个想法")
        
        if "字数要求" in missing_info:
            enhanced_parts.append("请控制在 200 字以内")
        
        if "风格" in missing_info:
            enhanced_parts.append("请用简洁专业的风格")
        
        return "\n\n".join(enhanced_parts)
    
    def _generate_enhancements(self, original: str, optimized: str) -> List[str]:
        """生成增强项列表"""
        enhancements = []
        
        if len(optimized) > len(original):
            enhancements.append("添加了详细的约束条件")
        
        if "你是一个" in optimized:
            enhancements.append("添加了角色设定")
        
        if "Markdown" in optimized:
            enhancements.append("明确了输出格式")
        
        if "注释" in optimized:
            enhancements.append("添加了注释要求")
        
        if "性能" in optimized.lower():
            enhancements.append("添加了性能要求")
        
        if "步骤" in optimized:
            enhancements.append("要求详细步骤")
        
        if "示例" in optimized:
            enhancements.append("要求添加示例")
        
        if not enhancements:
            enhancements.append("基本格式优化")
        
        return enhancements
    
    def format_result(self, result: OptimizationResult) -> str:
        """格式化结果输出"""
        output = []
        output.append("=" * 50)
        output.append(f"🔧 Prompt 优化结果 (v{__version__})")
        if result.cached:
            output.append("📦 (来自缓存)")
        output.append("=" * 50)
        output.append("")
        output.append("📝 原始 Prompt:")
        output.append(f"   {result.original}")
        output.append("")
        output.append("✨ 优化后 Prompt:")
        output.append(f"   {result.optimized}")
        output.append("")
        output.append(f"📋 任务类型: {result.task_type}")
        
        if result.missing_info:
            output.append(f"⚠️ 缺失信息: {', '.join(result.missing_info)}")
        
        if result.enhancements:
            output.append(f"✅ 增强项: {', '.join(result.enhancements)}")
        
        output.append("=" * 50)
        
        return "\n".join(output)
    
    def get_supported_types(self) -> List[str]:
        """获取支持的任务类型"""
        return [k for k in self.config["task_patterns"].keys() if k != "通用任务"]
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "version": __version__,
            "total_task_types": len(self.config["task_patterns"]) - 1,
            "language_patterns": len(self.config["language_patterns"]),
            "format_patterns": len(self.config["format_patterns"]),
            "style_patterns": len(self.config["style_patterns"]),
            "cache": _prompt_cache.stats(),
        }
    
    def clear_cache(self):
        """清空缓存"""
        _prompt_cache.clear()
    
    def reload_config(self, config_path: Optional[str] = None):
        """重新加载配置"""
        if config_path:
            self.config_path = config_path
        self.config = self._deep_copy(DEFAULT_CONFIG)
        self._load_config()
        self._compile_patterns()
        logger.info("🔄 配置已重新加载")


# ============ 入口函数 ============

def optimize_prompt(
    prompt: str, 
    verbose: bool = True,
    json_output: bool = False,
    use_cache: bool = True
) -> Union[str, OptimizationResult]:
    """优化 prompt 的入口函数"""
    optimizer = PromptOptimizer(use_cache=use_cache)
    result = optimizer.optimize(prompt, use_cache=use_cache)
    
    if json_output:
        if verbose:
            print(result.to_json())
        return result
    
    if verbose:
        print(optimizer.format_result(result))
    
    return result.optimized


def optimize_from_file(
    input_file: str,
    output_file: Optional[str] = None,
    json_output: bool = False,
    use_cache: bool = True
) -> List[OptimizationResult]:
    """从文件批量优化 prompt"""
    optimizer = PromptOptimizer(use_cache=use_cache)
    results = []
    
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"输入文件不存在: {input_file}")
    
    prompts = input_path.read_text(encoding="utf-8").strip().split("\n")
    prompts = [p.strip() for p in prompts if p.strip()]
    
    for i, prompt in enumerate(prompts, 1):
        try:
            result = optimizer.optimize(prompt, use_cache=use_cache)
            results.append(result)
            cached_mark = "📦" if result.cached else "✅"
            print(f"[{i}/{len(prompts)}] {cached_mark} {prompt[:30]}...")
        except Exception as e:
            print(f"[{i}/{len(prompts)}] ❌ {prompt[:30]}... 错误: {e}")
    
    if output_file:
        output_path = Path(output_file)
        if json_output:
            output_path.write_text(
                json.dumps([r.to_dict() for r in results], ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        else:
            lines = [r.optimized for r in results]
            output_path.write_text("\n\n---\n\n".join(lines), encoding="utf-8")
        print(f"\n📁 结果已保存到: {output_file}")
    
    return results


# ============ CLI 构建函数 ============

def build_parser() -> argparse.ArgumentParser:
    """构建 CLI 参数解析器"""
    parser = argparse.ArgumentParser(
        description=f"🚀 Prompt Optimizer v{__version__} - AI 任务处理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python prompt_optimizer.py "帮我写个排序"
  python prompt_optimizer.py "帮我写个排序" --json
  python prompt_optimizer.py --file input.txt
  python prompt_optimizer.py --clear-cache
  python prompt_optimizer.py --stats
  python prompt_optimizer.py --config custom.yaml
  python -m prompt_optimizer "帮我写个排序"
        """
    )
    
    parser.add_argument("prompt", nargs="?", help="要优化的 prompt")
    parser.add_argument("-f", "--file", help="从文件读取 prompt（每行一个）")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("-j", "--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("-v", "--verbose", action="store_true", default=True, help="显示详细信息")
    parser.add_argument("-q", "--quiet", action="store_true", help="静默模式")
    parser.add_argument("--stats", action="store_true", help="显示统计信息")
    parser.add_argument("-t", "--types", action="store_true", help="显示支持的任务类型")
    parser.add_argument("--cache", action="store_true", default=True, help="启用缓存（默认）")
    parser.add_argument("--no-cache", action="store_true", help="禁用缓存")
    parser.add_argument("--clear-cache", action="store_true", help="清空缓存")
    parser.add_argument("-c", "--config", help="配置文件路径")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    return parser


def handle_stats(optimizer: PromptOptimizer):
    """处理统计信息显示"""
    stats = optimizer.get_stats()
    print(f"📊 Prompt Optimizer v{__version__} 统计信息")
    print("=" * 50)
    print(f"  任务类型: {stats['total_task_types']} 种")
    print(f"  编程语言: {stats['language_patterns']} 种")
    print(f"  输出格式: {stats['format_patterns']} 种")
    print(f"  风格模式: {stats['style_patterns']} 种")
    print("")
    print("📦 缓存统计:")
    cache_stats = stats["cache"]
    print(f"  当前大小: {cache_stats['size']}/{cache_stats['maxsize']}")
    print(f"  命中/未命中: {cache_stats['hits']}/{cache_stats['misses']}")
    print(f"  命中率: {cache_stats['hit_rate']}")


def handle_types(optimizer: PromptOptimizer):
    """处理类型列表显示"""
    print("📋 支持的任务类型:")
    print("-" * 40)
    for task_type in optimizer.get_supported_types():
        print(f"  • {task_type}")


def handle_file_mode(args) -> List[OptimizationResult]:
    """处理文件模式"""
    return optimize_from_file(
        args.file, args.output, args.json, 
        use_cache=not args.no_cache
    )


def handle_prompt_mode(args, optimizer: PromptOptimizer):
    """处理单个 prompt 模式"""
    result = optimizer.optimize(args.prompt, use_cache=not args.no_cache)
    
    if args.json:
        print(result.to_json())
    else:
        print(result.optimized)
    
    if args.verbose and not args.quiet:
        cache_status = "📦 缓存命中" if result.cached else "✨ 优化完成"
        print(f"\n{cache_status} | 类型: {result.task_type}", file=sys.stderr)


def main():
    """CLI 入口 - 重构版"""
    parser = build_parser()
    args = parser.parse_args()
    
    # 静默模式
    if args.quiet:
        args.verbose = False
        logger.setLevel(logging.WARNING)
    
    # 确定是否使用缓存
    use_cache = not args.no_cache
    
    # 初始化优化器
    optimizer = PromptOptimizer(config_path=args.config, use_cache=use_cache)
    
    # 清空缓存
    if args.clear_cache:
        optimizer.clear_cache()
        return
    
    # 显示统计信息
    if args.stats:
        handle_stats(optimizer)
        return
    
    # 显示支持的类型
    if args.types:
        handle_types(optimizer)
        return
    
    # 处理输入
    try:
        if args.file:
            results = handle_file_mode(args)
            if args.json and not args.output:
                print(json.dumps([r.to_dict() for r in results], ensure_ascii=False, indent=2))
            return
        
        if args.prompt:
            handle_prompt_mode(args, optimizer)
            return
        
        parser.print_help()
        print(f"\n💡 提示: 请提供 prompt 或使用 --file 从文件读取")
        
    except (ValueError, RuntimeError) as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未知错误: {e}", file=sys.stderr)
        sys.exit(1)


# ============ __main__ 入口 ============

if __name__ == "__main__":
    main()