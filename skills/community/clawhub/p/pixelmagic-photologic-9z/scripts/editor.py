#!/usr/bin/env python3
"""
专业图像后期处理核心模块
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class ImageMagickChecker:
    """ImageMagick 检测和安装器"""
    
    def __init__(self):
        self.magick_path = None
        self._find_magick()
    
    def _find_magick(self):
        """查找 magick 命令"""
        # 尝试直接调用
        try:
            result = subprocess.run(
                ['magick', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.magick_path = 'magick'
                return
        except:
            pass
        
        # 尝试常见安装路径
        common_paths = [
            r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe",
            r"C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\magick.exe",
            r"C:\Program Files\ImageMagick-7.0.11-Q16-HDRI\magick.exe",
            r"C:\Program Files\ImageMagick-7.1.1-Q16\magick.exe",
            r"C:\Program Files\ImageMagick-7.1.0-Q16\magick.exe",
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                self.magick_path = path
                return
    
    def is_installed(self) -> bool:
        """检查是否已安装"""
        return self.magick_path is not None
    
    def get_install_command(self) -> str:
        """获取安装命令"""
        if sys.platform == 'win32':
            return "winget install ImageMagick.ImageMagick"
        elif sys.platform == 'darwin':
            return "brew install imagemagick"
        else:
            return "sudo apt-get install imagemagick"
    
    def run_magick(self, args: List[str]) -> Tuple[bool, str]:
        """运行 magick 命令"""
        if not self.magick_path:
            return False, "ImageMagick not found"
        
        cmd = [self.magick_path] + args
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)


class StylePreset:
    """修图风格预设"""
    
    PRESETS = {
        "apocalyptic": {
            "name": "末日大片",
            "description": "低饱和、青橙色调、暗角、颗粒",
            "steps": [
                {"name": "对比度", "params": "-brightness-contrast 0x15"},
                {"name": "色调", "params": "-modulate 105,65 -fill #2a5a6a -tint 20"},
                {"name": "锐化", "params": "-sharpen 0x1.2"},
                {"name": "颗粒", "params": "-attenuate 0.4 +noise gaussian"},
            ],
            "vignette": True,
            "vignette_strength": 25
        },
        "japanese": {
            "name": "日系清新",
            "description": "高明度、低对比、偏青绿",
            "steps": [
                {"name": "曝光", "params": "-brightness-contrast 10x-10"},
                {"name": "色调", "params": "-modulate 115,80 -fill #4a6a5a -tint 15 -gamma 1.05"},
                {"name": "柔化", "params": "-blur 0x0.5"},
            ],
            "vignette": False
        },
        "vintage": {
            "name": "复古胶片",
            "description": "暖色调、褪色感",
            "steps": [
                {"name": "对比度", "params": "-brightness-contrast 0x12"},
                {"name": "色调", "params": "-modulate 102,60 -fill #8a6a4a -tint 25"},
                {"name": "颗粒", "params": "-attenuate 0.3 +noise gaussian"},
            ],
            "vignette": True,
            "vignette_strength": 30
        },
        "bw-high": {
            "name": "黑白高对比",
            "description": "黑白、高对比",
            "steps": [
                {"name": "转黑白", "params": "-colorspace Gray"},
                {"name": "对比度", "params": "-brightness-contrast 0x35"},
                {"name": "锐化", "params": "-sharpen 0x2"},
            ],
            "vignette": False
        }
    }
    
    @classmethod
    def get_preset(cls, name: str) -> Optional[Dict]:
        return cls.PRESETS.get(name)
    
    @classmethod
    def list_presets(cls) -> List[str]:
        return list(cls.PRESETS.keys())


class ImageEditor:
    """图像编辑器主类"""
    
    def __init__(self, workspace: str = None):
        self.checker = ImageMagickChecker()
        self.workspace = workspace or self._get_default_workspace()
        self.work_dir = None
        self.log_file = None
        
    def _get_default_workspace(self) -> str:
        """获取默认工作目录"""
        return os.path.join(os.getcwd(), "image-editor-work")
    
    def _setup_workspace(self, input_path: str):
        """设置工作目录"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = Path(input_path).stem
        self.work_dir = os.path.join(self.workspace, f"{filename}_{timestamp}")
        
        # 创建子目录
        os.makedirs(os.path.join(self.work_dir, "originals"), exist_ok=True)
        os.makedirs(os.path.join(self.work_dir, "temp"), exist_ok=True)
        os.makedirs(os.path.join(self.work_dir, "temp", "params"), exist_ok=True)
        os.makedirs(os.path.join(self.work_dir, "final"), exist_ok=True)
        
        # 初始化日志
        self.log_file = os.path.join(self.work_dir, "log.txt")
        self._log(f"开始处理: {input_path}")
        self._log(f"工作目录: {self.work_dir}")
        
        # 备份原始图
        shutil.copy2(input_path, os.path.join(self.work_dir, "originals"))
        self._log("原始图已备份")
    
    def _log(self, message: str):
        """记录日志"""
        if self.log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {message}\n")
    
    def _get_image_info(self, path: str) -> Dict:
        """获取图片信息"""
        success, output = self.checker.run_magick(['identify', path])
        if success:
            parts = output.strip().split()
            if len(parts) >= 3:
                return {
                    "path": path,
                    "format": parts[1],
                    "resolution": parts[2],
                    "success": True
                }
        return {"success": False, "error": output}
    
    def _apply_steps_from_original(self, input_path: str, preset: Dict) -> List[str]:
        """从原始图逐步应用每个步骤，生成中间文件，返回累积参数列表"""
        all_params = []

        for i, step in enumerate(preset['steps'], 1):
            step_params = step['params'].split()
            all_params.extend(step_params)

            # 从原始图 + 累积参数生成中间 JPG
            temp_output = os.path.join(
                self.work_dir, "temp",
                f"step{i:02d}_{step['name']}.jpg"
            )
            cmd = [input_path] + all_params + ['-quality', '100', temp_output]

            success, error = self.checker.run_magick(cmd)
            if not success:
                self._log(f"步骤{i}失败: {error}")
                raise Exception(f"处理失败: {error}")

            # 记录参数
            param_file = os.path.join(
                self.work_dir, "temp", "params",
                f"step{i:02d}.txt"
            )
            with open(param_file, 'w', encoding='utf-8') as f:
                f.write(f"步骤{i}: {step['name']}\n")
                f.write(f"参数: {step['params']}\n")

            self._log(f"步骤{i}完成: {step['name']}")

        return all_params

    def _build_vignette_args(self, input_path: str, strength: int) -> List[str]:
        """构建暗角参数（作为 magick 命令的一部分）"""
        info = self._get_image_info(input_path)
        if not info['success']:
            raise Exception("无法获取图片信息")

        resolution = info['resolution']
        return [
            '(', '-size', resolution, 'radial-gradient:black-white',
            '-level', '0%,50%', ')',
            '-compose', 'blend',
            '-define', f'compose:args={strength}',
            '-composite'
        ]
    
    def process(self, input_path: str, style: str = "apocalyptic", 
                output_name: str = None, keep_temp: bool = False) -> str:
        """
        处理单张图片
        
        Args:
            input_path: 输入图片路径
            style: 修图风格
            output_name: 输出文件名（不含扩展名）
            keep_temp: 是否保留中间文件
            
        Returns:
            最终输出文件路径
        """
        # 检查 ImageMagick
        if not self.checker.is_installed():
            raise Exception(
                "ImageMagick 未安装。请运行安装命令:\n"
                f"{self.checker.get_install_command()}"
            )
        
        # 检查输入文件
        if not os.path.exists(input_path):
            raise Exception(f"输入文件不存在: {input_path}")
        
        # 获取预设
        preset = StylePreset.get_preset(style)
        if not preset:
            raise Exception(f"未知风格: {style}。可用风格: {StylePreset.list_presets()}")
        
        # 设置工作目录
        self._setup_workspace(input_path)
        
        # 获取图片信息
        info = self._get_image_info(input_path)
        self._log(f"图片信息: {info}")
        
        # 从原始图逐步处理，累积参数并生成中间文件（仅用于验证）
        all_params = self._apply_steps_from_original(input_path, preset)

        # 生成最终图像：从原始图一次性应用所有参数
        if not output_name:
            output_name = f"{Path(input_path).stem}_{style}"
        final_path = os.path.join(self.work_dir, "final", f"{output_name}_final.jpg")

        final_cmd = [input_path] + all_params

        # 添加暗角（从原始图一起合成，不参与链式处理）
        if preset.get('vignette'):
            strength = preset.get('vignette_strength', 40)
            vignette_args = self._build_vignette_args(input_path, strength)
            final_cmd.extend(vignette_args)

        final_cmd.extend(['-quality', '100', final_path])

        success, error = self.checker.run_magick(final_cmd)
        if not success:
            self._log(f"最终生成失败: {error}")
            raise Exception(f"最终生成失败: {error}")

        self._log(f"最终文件: {final_path}")

        # 清理中间文件（如果不保留）
        if not keep_temp:
            temp_dir = os.path.join(self.work_dir, "temp")
            shutil.rmtree(temp_dir)
            self._log("中间文件已清理")

        return final_path
    
    def batch_process(self, input_dir: str, style: str = "apocalyptic",
                      output_dir: str = None) -> List[str]:
        """批量处理目录中的图片"""
        if not output_dir:
            output_dir = os.path.join(input_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        
        # 支持的格式
        extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.dng', '.cr2', '.nef']
        
        results = []
        for filename in os.listdir(input_dir):
            ext = Path(filename).suffix.lower()
            if ext in extensions:
                input_path = os.path.join(input_dir, filename)
                try:
                    output_path = self.process(
                        input_path, 
                        style=style,
                        output_name=Path(filename).stem
                    )
                    # 复制到输出目录
                    final_name = f"{Path(filename).stem}_{style}.jpg"
                    final_output = os.path.join(output_dir, final_name)
                    shutil.copy2(output_path, final_output)
                    results.append(final_output)
                except Exception as e:
                    self._log(f"处理失败 {filename}: {str(e)}")
        
        return results
    
    def create_preset(self, name: str, params: Dict):
        """创建自定义预设"""
        preset_path = os.path.join(
            Path(__file__).parent.parent,
            "presets",
            f"{name}.json"
        )
        
        with open(preset_path, 'w', encoding='utf-8') as f:
            json.dump(params, f, indent=2)
        
        return preset_path


def main():
    """CLI 入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='专业图像后期处理工具')
    parser.add_argument('input', help='输入图片路径或目录')
    parser.add_argument('--style', default='apocalyptic', 
                       choices=StylePreset.list_presets(),
                       help='修图风格')
    parser.add_argument('--output', '-o', help='输出文件名或目录')
    parser.add_argument('--batch', '-b', action='store_true', help='批量处理')
    parser.add_argument('--keep-temp', '-k', action='store_true', help='保留中间文件')
    
    args = parser.parse_args()
    
    editor = ImageEditor()
    
    # 检查 ImageMagick
    if not editor.checker.is_installed():
        print("❌ ImageMagick 未安装")
        print(f"请运行: {editor.checker.get_install_command()}")
        print("安装完成后请重启终端")
        sys.exit(1)
    
    try:
        if args.batch:
            results = editor.batch_process(args.input, args.style, args.output)
            print(f"✅ 批量处理完成，共处理 {len(results)} 张图片")
            for r in results:
                print(f"  - {r}")
        else:
            result = editor.process(
                args.input, 
                args.style, 
                args.output,
                args.keep_temp
            )
            print(f"✅ 处理完成: {result}")
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
