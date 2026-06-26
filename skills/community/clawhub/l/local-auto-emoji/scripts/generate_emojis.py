#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
表情生成模块
- 调用 GetEmoji 项目的 QwenImageGenerator
- 为 8 种情感各生成 1 张
"""

import sys
import os
import json
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from PIL import Image

# 添加 GetEmoji 项目到 Python 路径
GETEMOJI_ROOT = Path(__file__).parent.parent.parent.parent / "projects" / "getemoji"
sys.path.insert(0, str(GETEMOJI_ROOT))

try:
    from lib.image_models.qwen_image_generator import QwenImageGenerator
except ImportError as e:
    print(f"[GenerateEmojis] 导入 QwenImageGenerator 失败: {e}")
    print(f"[GenerateEmojis] 请确保 dashscope SDK 已安装: pip install dashscope")
    raise

class EmojiGenerator:
    """表情生成器"""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = GETEMOJI_ROOT / "config" / "image_model.json"

        self.generator = QwenImageGenerator(Path(config_path))
        self.emotions_config = self._load_emotions_config()
        self.emotion_ids = [e["id"] for e in self.emotions_config]
        self.target_size = (512, 512)  # 最终输出尺寸

    def _compress_image(self, src_path: Path, dest_path: Path, size: Tuple[int, int] = (500, 500)):
        """压缩图片到指定尺寸"""
        try:
            with Image.open(src_path) as img:
                # 使用高质量抗锯齿缩放
                img_resized = img.resize(size, Image.Resampling.LANCZOS)
                # 保存为 PNG（保持质量）
                img_resized.save(dest_path, "PNG", optimize=True, quality=95)
            return True
        except Exception as e:
            print(f"[Warning] 图片压缩失败 {src_path}: {e}")
            # 降级：直接复制原文件
            shutil.copy2(src_path, dest_path)
            return False

    def _load_emotions_config(self) -> List[Dict]:
        """加载情感配置"""
        config_file = Path(__file__).parent.parent / "config" / "emotions.json"
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data["emotions"]

    def generate_all(self, avatar_path: str, user_version_dir: Path, progress_callback=None, styles: Optional[List[str]] = None) -> Tuple[bool, List[Path], str]:
        """
        生成表情并保存到用户版本目录
        返回：(success, output_paths, error_msg)
        """
        try:
            input_path = Path(avatar_path)
            if not input_path.exists():
                return False, [], f"头像不存在: {avatar_path}"

            # 确定要生成的情感列表
            if styles is None:
                styles = self.emotion_ids  # 默认全部

            # 调用 QwenImageGenerator（它会下载到 self.generator.output_dir）
            generated_paths = self.generator.generate(input_path, styles)

            if len(generated_paths) != len(styles):
                return False, [], f"生成数量不匹配: 期望 {len(styles)}，实际 {len(generated_paths)}"

            # 复制到用户版本目录，并重命名为情感名（同时压缩到 500×500）
            output_paths = []
            for emo_id, src_path in zip(styles, generated_paths):
                dest_path = user_version_dir / f"{emo_id}.png"
                self._compress_image(src_path, dest_path, self.target_size)
                output_paths.append(dest_path)

                if progress_callback:
                    # 进度回调（这里简化处理，因为 generate 是顺序的）
                    pass

            return True, output_paths, ""

        except Exception as e:
            import traceback
            return False, [], f"{str(e)}\n{traceback.format_exc()}"

    def _cleanup_generated(self, paths: List[Path]):
        """清理 generator 输出目录中的临时文件"""
        try:
            for p in paths:
                if p.exists():
                    p.unlink()
        except Exception:
            pass


if __name__ == "__main__":
    # 简单测试
    import argparse

    parser = argparse.ArgumentParser(description="表情生成模块")
    parser.add_argument("avatar", help="头像路径")
    parser.add_argument("--output", help="输出目录（用户版本目录）")
    args = parser.parse_args()

    generator = EmojiGenerator()
    output_dir = Path(args.output) if args.output else Path("/tmp/test_emojis")
    output_dir.mkdir(parents=True, exist_ok=True)

    success, paths, error = generator.generate_all(args.avatar, output_dir)
    if success:
        print(f"✅ 生成成功，共 {len(paths)} 张表情:")
        for p in paths:
            print(f"  - {p.name}")
    else:
        print(f"❌ 生成失败: {error}")
