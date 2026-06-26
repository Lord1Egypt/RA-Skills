#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地 Whisper 模型延迟下载工具

在用户选择转写方案后，再下载模型，而不是在加载时就自动下载。
这样可以：
1. 避免用户不需要的模型占用磁盘空间
2. 让用户明确知道正在下载什么模型
3. 提供下载进度和取消选项
"""

import os
import sys
from pathlib import Path
from typing import Optional


class ModelDownloader:
    """Whisper 模型延迟下载器"""
    
    def __init__(self):
        self.cache_dir = Path.home() / ".cache" / "whisper"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def model_exists(self, model_name: str) -> bool:
        """检查模型是否已下载
        
        Args:
            model_name: 模型名称（tiny/base/small/medium/large/large-v3）
        
        Returns:
            bool: 模型是否已存在
        """
        # Whisper 模型文件命名规则：{model_name}.pt 或 {model_name}.en.pt
        model_paths = [
            self.cache_dir / f"{model_name}.pt",
            self.cache_dir / f"{model_name}.en.pt"
        ]
        return any(p.exists() for p in model_paths)
    
    def get_model_info(self, model_name: str) -> dict:
        """获取模型信息（大小、描述等）
        
        Args:
            model_name: 模型名称
        
        Returns:
            dict: 包含大小、描述、准确率等信息的字典
        """
        model_info = {
            "base": {
                "size": "74 MB",
                "description": "基础模型，用于语言检测",
                "accuracy": "中等",
                "use_case": "仅用于自动语言检测，不用于转写"
            },
            "small": {
                "size": "471 MB",
                "description": "高准确率，平衡性能",
                "accuracy": "高",
                "use_case": "推荐用于日常会议转写"
            },
            "medium": {
                "size": "1.5 GB",
                "description": "更高准确率",
                "accuracy": "很高",
                "use_case": "对准确率要求较高的场景"
            },
            "large": {
                "size": "3 GB",
                "description": "最高准确率",
                "accuracy": "最高",
                "use_case": "重要会议、专业领域转写"
            },
            "large-v3": {
                "size": "3 GB",
                "description": "最新最高准确率模型",
                "accuracy": "最高",
                "use_case": "最高准确率要求的场景"
            }
        }
        return model_info.get(model_name, {})
    
    def download_model(self, model_name: str) -> bool:
        """下载模型
        
        Args:
            model_name: 模型名称
        
        Returns:
            bool: 下载是否成功
        """
        try:
            import whisper
        except ImportError:
            print("❌ 错误：whisper 未安装")
            print("💡 请运行：pip install openai-whisper")
            return False
        
        info = self.get_model_info(model_name)
        
        print("\n" + "="*60)
        print(f"📥 准备下载 Whisper 模型：{model_name}")
        print("="*60)
        print(f"📊 模型大小：{info.get('size', '未知')}")
        print(f"📝 准确率：{info.get('accuracy', '未知')}")
        print(f"💡 使用场景：{info.get('use_case', '未知')}")
        print(f"💾 保存位置：{self.cache_dir}")
        print("="*60)
        
        # 询问用户是否确认下载
        confirm = input("\n⚠️  注意：首次下载需要时间，请确认是否继续？（y/n，默认 y）: ").strip().lower()
        if confirm == 'n':
            print("❌ 已取消下载")
            return False
        
        try:
            print("\n⏳ 开始下载...")
            print("💡 提示：按 Ctrl+C 可随时中断下载\n")
            
            # 调用 whisper.load_model 下载模型
            model = whisper.load_model(
                model_name, 
                download_root=str(self.cache_dir),
                in_memory=True  # 不加载到内存，仅下载
            )
            
            print("\n✅ 模型下载完成！")
            return True
            
        except KeyboardInterrupt:
            print("\n\n❌ 用户中断下载")
            return False
        except Exception as e:
            print(f"\n\n❌ 下载失败：{e}")
            return False
    
    def load_model_delayed(self, model_name: str, device: Optional[str] = None):
        """延迟加载模型（先检查是否存在，不存在则下载）
        
        Args:
            model_name: 模型名称
            device: 设备类型（cuda/cpu），默认自动检测
        
        Returns:
            whisper 模型对象
        """
        # 检查模型是否已下载
        if not self.model_exists(model_name):
            print(f"\n⚠️  模型 {model_name} 尚未下载")
            if not self.download_model(model_name):
                print("❌ 无法继续，缺少模型文件")
                sys.exit(1)
        
        # 模型已存在，直接加载
        try:
            import whisper
            
            # 自动检测设备
            if device is None:
                try:
                    device = "cuda" if whisper.cuda.is_available() else "cpu"
                except:
                    device = "cpu"
            
            print(f"\n⏳ 正在加载模型 {model_name}...")
            print(f"🔧 使用设备：{device}")
            
            model = whisper.load_model(model_name, device=device, download_root=str(self.cache_dir))
            
            print("✅ 模型加载完成！")
            return model
            
        except Exception as e:
            print(f"❌ 模型加载失败：{e}")
            sys.exit(1)


def get_model_name_from_provider(provider: str) -> str:
    """从转写方案映射到 Whisper 模型名称
    
    Args:
        provider: 转写方案标识（local-large/local-small等）
    
    Returns:
        str: Whisper 模型名称
    """
    mapping = {
        "local-large": "large-v3",
        "local-small": "small",
        "local-medium": "medium",
        "local-base": "base"
    }
    return mapping.get(provider, "small")


def download_if_needed(provider: str) -> bool:
    """检查并下载所需的模型（如果需要）
    
    Args:
        provider: 转写方案标识
    
    Returns:
        bool: 下载/加载是否成功
    """
    model_name = get_model_name_from_provider(provider)
    downloader = ModelDownloader()
    
    # 检查模型是否已存在
    if downloader.model_exists(model_name):
        print(f"✅ 模型 {model_name} 已存在，跳过下载")
        return True
    
    # 下载模型
    return downloader.download_model(model_name)


if __name__ == "__main__":
    # 命令行测试
    if len(sys.argv) > 1:
        provider = sys.argv[1]
        print(f"测试转写方案：{provider}")
        model_name = get_model_name_from_provider(provider)
        print(f"对应模型：{model_name}")
        
        downloader = ModelDownloader()
        print(f"模型已下载：{downloader.model_exists(model_name)}")
        print(f"模型信息：{downloader.get_model_info(model_name)}")
    else:
        print("用法：python model_downloader.py <provider>")
        print("示例：python model_downloader.py local-small")
