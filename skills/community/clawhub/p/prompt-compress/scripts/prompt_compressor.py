#!/usr/bin/env python3
"""
Prompt Compressor - 提示词压缩器

功能:
- 按压缩等级压缩提示词
- 保留语义核心
- 输出压缩统计
"""

import re
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class CompressionLevel(Enum):
    """压缩等级"""
    LIGHT = "light"      # 轻度 20-30%
    MEDIUM = "medium"    # 中度 40-60%
    HEAVY = "heavy"      # 重度 60-80%
    MINIMAL = "minimal"  # 极简 80%+


# 简化的 Token 估算
def estimate_tokens(text: str) -> int:
    """估算文本的 Token 数量"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    other_chars = len(text) - chinese_chars - english_chars
    
    chinese_tokens = chinese_chars / 1.5
    english_tokens = english_chars / 4
    other_tokens = other_chars / 3
    
    return max(1, int(chinese_tokens + english_tokens + other_tokens))


# 压缩规则配置
COMPRESSION_RULES = {
    # 礼貌用语删除
    "polite_removals": [
        (r'请[你您]?帮我[做写看分析处理]?一下', ''),
        (r'请[你您]?', ''),
        (r'麻烦[你您]', ''),
        (r'谢谢[您你]?[,，。]?', ''),
        (r'你好[,，。]?', ''),
        (r'您好[,，。]?', ''),
        (r'非常感谢', ''),
        (r'不好意思', ''),
        (r'如果可以的话[,，]?', ''),
        (r'帮帮忙[,，]?', ''),
    ],
    
    # 修饰词简化
    "modifier_simplifications": [
        (r'非常地?', ''),
        (r'十分', ''),
        (r'特别', ''),
        (r'极其', ''),
        (r'详细地?', '详细'),
        (r'仔细地?', '仔细'),
        (r'认真地?', ''),
        (r'尽可能', '尽量'),
        (r'所有的', '全部'),
    ],
    
    # 句式转换
    "sentence_transforms": [
        (r'我[需要想]要你[帮请]我(.+)', r'\1'),
        (r'我想让你(.+)', r'\1'),
        (r'希望你[能够]?(.+)', r'\1'),
        (r'能不能(.+)', r'\1'),
        (r'可以帮我(.+)吗', r'\1'),
    ],
    
    # 结构化转换
    "structural_transforms": [
        (r'要求如下[：:]?\s*', '\n要求:\n'),
        (r'(\d+)[.、)]\s*', r'\1. '),
        (r'第一步[：:]\s*(.+)', r'1. \1'),
        (r'第二步[：:]\s*(.+)', r'2. \1'),
        (r'第三步[：:]\s*(.+)', r'3. \1'),
    ],
    
    # 符号替换
    "symbol_replacements": [
        (r'优点[是为：:]+\s*', '优点+'),
        (r'缺点[是为：:]+\s*', '缺点-'),
        (r'问题[是为：:]+\s*', 'Q: '),
        (r'答案[是为：:]+\s*', 'A: '),
        (r'例如[,，]?\s*', '如'),
        (r'因为[,，]?\s*', '因'),
        (r'所以[,，]?\s*', '故'),
        (r'但是[,，]?\s*', '但'),
    ],
}


def apply_rules(text: str, rules: List[str], level: CompressionLevel) -> str:
    """应用压缩规则"""
    result = text
    
    for rule_name in rules:
        if rule_name in COMPRESSION_RULES:
            for pattern, replacement in COMPRESSION_RULES[rule_name]:
                result = re.sub(pattern, replacement, result)
    
    # 清理多余空白
    result = re.sub(r'\s+', ' ', result)
    result = re.sub(r'\n\s+', '\n', result)
    result = result.strip()
    
    return result


def compress_light(text: str) -> str:
    """轻度压缩 (20-30%)"""
    return apply_rules(text, ["polite_removals"], CompressionLevel.LIGHT)


def compress_medium(text: str) -> str:
    """中度压缩 (40-60%)"""
    result = apply_rules(text, 
        ["polite_removals", "modifier_simplifications", "sentence_transforms"],
        CompressionLevel.MEDIUM)
    
    # 额外处理
    result = re.sub(r'[。！？，、；："]', lambda m: m.group() if m.group() in '。！？' else '', result)
    
    return result


def compress_heavy(text: str) -> str:
    """重度压缩 (60-80%)"""
    result = apply_rules(text,
        ["polite_removals", "modifier_simplifications", 
         "sentence_transforms", "structural_transforms", "symbol_replacements"],
        CompressionLevel.HEAVY)
    
    # 更激进的清理
    result = re.sub(r'[，、；："]', '', result)
    result = re.sub(r' +', ' ', result)
    
    return result


def compress_minimal(text: str) -> str:
    """极简压缩 (80%+) - 只保留关键词结构"""
    lines = []
    
    # 1. 识别任务类型
    task_patterns = [
        (r'分析|检查|查看|看', '分析'),
        (r'写|创作|生成|编写', '写'),
        (r'总结|概括|提炼', '总结'),
        (r'解释|说明|讲解', '解释'),
        (r'翻译|转换', '翻译'),
        (r'修复|解决|debug', '修复'),
        (r'优化|改进|提升', '优化'),
        (r'创建|设计|开发', '创建'),
        (r'爬取|抓取', '爬取'),
    ]
    
    for pattern, task_name in task_patterns:
        if re.search(pattern, text):
            lines.append(f"[{task_name}]")
            break
    
    # 2. 提取核心对象/主题
    object_patterns = [
        r'(网页爬虫|爬虫|代码|程序|脚本|bug)',
        r'(文章|文档|报告|论文)',
        r'(问题|错误)',
        r'关于(.+?)的(文章|文档|报告)',
    ]
    for pattern in object_patterns:
        match = re.search(pattern, text)
        if match:
            if match.lastindex and match.lastindex > 1:
                lines.append(f"主题: {match.group(1)}")
            else:
                lines.append(f"对象: {match.group(1)}")
            break
    
    # 3. 提取错误信息
    error_match = re.search(r'错误[信息是]*[：:\s]*([^\s，。！？]{1,10})', text)
    if error_match:
        lines.append(f"错误: {error_match.group(1)}")
    
    # 4. 提取目标/需求
    goal_match = re.search(r'爬取.+?(商品|数据|信息|内容)', text)
    if goal_match:
        lines.append(f"目标: 爬取{goal_match.group(1)}")
    
    # 5. 提取约束条件
    constraints = []
    
    # 字数
    word_match = re.search(r'(\d+)[字条]', text)
    if word_match:
        constraints.append(f"{word_match.group(1)}字")
    
    # 时间范围
    time_match = re.search(r'(\d+年代?)[到至](\d+年代?|现在|今)', text)
    if time_match:
        constraints.append(f"{time_match.group(1)}-{time_match.group(2)}")
    
    if constraints:
        lines.append(f"约束: {', '.join(constraints)}")
    
    # 6. 提取要求列表
    requirements = []
    req_keywords = {
        '解决方案': '解决方案',
        '避免': '避免方法',
        '详细': '详细',
        '里程碑': '里程碑事件',
        '科学家': '科学家贡献',
        '通俗': '通俗易懂',
        '未来': '未来展望',
        '优缺点': '优缺点',
        '示例': '示例',
        '代码': '代码示例',
    }
    for kw, label in req_keywords.items():
        if kw in text:
            requirements.append(label)
    
    if requirements:
        lines.append(f"要点: {', '.join(requirements)}")
    
    return '\n'.join(lines) if lines else text[:50]


def compress_prompt(text: str, level: CompressionLevel = CompressionLevel.MEDIUM) -> Tuple[str, Dict]:
    """
    压缩提示词
    
    Args:
        text: 原始提示词
        level: 压缩等级
    
    Returns:
        (压缩后文本, 统计信息)
    """
    original_tokens = estimate_tokens(text)
    
    compressors = {
        CompressionLevel.LIGHT: compress_light,
        CompressionLevel.MEDIUM: compress_medium,
        CompressionLevel.HEAVY: compress_heavy,
        CompressionLevel.MINIMAL: compress_minimal,
    }
    
    compressed = compressors[level](text)
    compressed_tokens = estimate_tokens(compressed)
    
    stats = {
        "original_tokens": original_tokens,
        "compressed_tokens": compressed_tokens,
        "saved_tokens": original_tokens - compressed_tokens,
        "saved_percent": round((1 - compressed_tokens / original_tokens) * 100, 1) if original_tokens > 0 else 0,
        "level": level.value,
    }
    
    return compressed, stats


def format_output(original: str, compressed: str, stats: Dict) -> str:
    """格式化输出结果"""
    output = []
    output.append("=" * 50)
    output.append("[COMPRESS] 提示词压缩结果")
    output.append("=" * 50)
    output.append(f"\n[LEVEL] 压缩等级: {stats['level'].upper()}")
    output.append(f"[TOKENS] 原始 Token: {stats['original_tokens']}")
    output.append(f"[COMPRESSED] 压缩后 Token: {stats['compressed_tokens']}")
    output.append(f"[SAVED] 节省 Token: {stats['saved_tokens']} ({stats['saved_percent']}%)")
    output.append("\n" + "-" * 50)
    output.append("[ORIGINAL] 原始提示词:")
    output.append("-" * 50)
    output.append(original[:500] + ("..." if len(original) > 500 else ""))
    output.append("\n" + "-" * 50)
    output.append("[RESULT] 压缩后提示词:")
    output.append("-" * 50)
    output.append(compressed)
    output.append("\n" + "=" * 50)
    
    return "\n".join(output)


def main():
    """主函数"""
    import sys
    import io
    
    # 设置 UTF-8 输出
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # 解析参数
    level = CompressionLevel.MEDIUM
    text_parts = []
    
    for arg in sys.argv[1:]:
        if arg.startswith("--level="):
            level_str = arg.split("=")[1].lower()
            level_map = {
                "light": CompressionLevel.LIGHT,
                "medium": CompressionLevel.MEDIUM,
                "heavy": CompressionLevel.HEAVY,
                "minimal": CompressionLevel.MINIMAL,
            }
            level = level_map.get(level_str, CompressionLevel.MEDIUM)
        else:
            text_parts.append(arg)
    
    if text_parts:
        text = " ".join(text_parts)
    else:
        print("请输入提示词（Ctrl+D 结束）:")
        text = sys.stdin.read()
    
    if not text.strip():
        print("错误: 未输入文本")
        sys.exit(1)
    
    compressed, stats = compress_prompt(text, level)
    print(format_output(text, compressed, stats))


if __name__ == "__main__":
    main()