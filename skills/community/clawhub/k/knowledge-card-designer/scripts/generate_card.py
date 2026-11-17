#!/usr/bin/env python3
"""
GTC 2026 产业趋势版 知识卡片生成器
基于 Chrome Headless 截图 + PIL裁剪
"""

import os
import subprocess
from pathlib import Path
from PIL import Image

# 配置
OUTPUT_DIR = Path("/root/.openclaw/workspace/output/gtc_industry_cards")
TEMPLATE_DIR = Path("/root/.openclaw/workspace/skills/knowledge-card-designer/assets/templates")

def generate_card(html_file, output_file, width=1080, height=1350):
    """使用Chrome headless生成PNG截图并裁剪"""
    # 先生成临时文件
    temp_file = str(output_file) + ".temp.png"
    
    cmd = [
        "google-chrome",
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--hide-scrollbars",
        "--disable-software-rasterizer",
        f"--window-size={width},{height}",
        f"--screenshot={temp_file}",
        f"file://{html_file}"
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=30)
        
        # 使用PIL裁剪到精确尺寸
        img = Image.open(temp_file)
        
        # 如果图片尺寸不对，调整大小或裁剪
        if img.size != (width, height):
            # 创建新画布，用深色背景填充
            new_img = Image.new('RGB', (width, height), color=(15, 23, 42))
            
            # 复制原图到新画布（从顶部开始）
            if img.width == width:
                # 宽度匹配，复制可见部分
                crop_height = min(height, img.height)
                cropped = img.crop((0, 0, width, crop_height))
                new_img.paste(cropped, (0, 0))
            else:
                # 需要缩放
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                new_img = img
            
            new_img.save(output_file, "PNG", optimize=True)
            new_img.close()
        else:
            # 尺寸正确，直接复制
            img.save(output_file, "PNG", optimize=True)
        
        img.close()
        os.remove(temp_file)
        
        file_size = os.path.getsize(output_file)
        print(f"✅ 生成成功: {Path(output_file).name} ({file_size/1024:.1f}KB)")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 生成失败: {e}")
        print(f"   stderr: {e.stderr.decode()}")
        return False

def generate_all_cards():
    """批量生成所有卡片"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    cards = [
        ("cover", 900, 383),      # 封面特殊尺寸
        ("trend1", 1080, 1350),   # 算力即权力
        ("trend2", 1080, 1350),   # Token经济
        ("trend3", 1080, 1350),   # 算力爆炸
        ("trend4", 1080, 1350),   # AI智能体
        ("trend5", 1080, 1350),   # 数字员工
        ("trend6", 1080, 1350),   # 物理AI
        ("trend7", 1080, 1350),   # 太空计算
        ("trend8", 1080, 1350),   # AI技术霸权
        ("action", 1080, 1350),   # 行动指南
    ]
    
    print("=" * 50)
    print("GTC 2026 产业趋势卡片生成器 (Chrome + PIL)")
    print("=" * 50)
    
    for name, width, height in cards:
        html_file = TEMPLATE_DIR / f"{name}.html"
        output_file = OUTPUT_DIR / f"{name}.png"
        
        if html_file.exists():
            print(f"\n生成 {name}.png ({width}x{height})...")
            generate_card(str(html_file), str(output_file), width, height)
        else:
            print(f"⚠️ 模板不存在: {html_file}")
    
    print("\n" + "=" * 50)
    print("生成完成！")
    print("=" * 50)

if __name__ == "__main__":
    generate_all_cards()
