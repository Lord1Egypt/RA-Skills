#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KD Skill 入口脚本模板

使用此模板创建你自己的 KD Skill 入口脚本
编码修复已内置，支持 Windows 中文正常显示

⚠️ 安全提示：
1. 修改下方 SKILL_PATH 为你实际的安装路径
2. 修改 OUTPUT_PATH 为你希望保存输出的目录
3. 首次运行前请检查所有路径配置
"""

import sys
import io

# ========== Windows 编码修复 - 必须在所有导入之前 ==========
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
# ==========================================================

# ========== 配置区域 - 修改为你自己的路径 ==========
# KD Skill 安装路径
SKILL_PATH = r'C:\Users\YOUR_USERNAME\.agents\skills\kd'  # <-- 修改这里

# 输出文件保存路径（请确保目录存在）
OUTPUT_PATH = r'C:\Users\YOUR_USERNAME\Documents\kd_output.txt'  # <-- 修改这里
# ==================================================

# 安全提示
print("⚠️  安全提示：首次运行前请确认：")
print(f"  1. SKILL_PATH: {SKILL_PATH}")
print(f"  2. OUTPUT_PATH: {OUTPUT_PATH}")
print("  3. 这些路径是你期望的")
print()
response = input("是否继续? (yes/no): ")
if response.lower() != 'yes':
    print("已取消")
    sys.exit(0)

# 添加 KD Skill 到路径
sys.path.insert(0, SKILL_PATH)

# 导入 KD Skill 模块
from scripts import (
    ConfigManager,
    ScriptGenerator,
    ExcelManager,
    WorkflowManager,
    FormatChecker
)

# ========== 你的代码从这里开始 ==========

def main():
    # 使用用户指定的输出路径
    output_file = OUTPUT_PATH
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("快导(KD) Skill 入口脚本\n")
        f.write("=" * 50 + "\n")
        
        # 示例：加载配置
        f.write("\n[1] 加载平台配置\n")
        config = ConfigManager()
        platform = config.get_platform_config('xiaohongshu')
        f.write(f"  平台: {platform['name']}\n")
        f.write(f"  用户画像: {platform['user_profile']}\n")
        f.write(f"  内容风格: {platform['content_style']}\n")
        
        # 示例：创建脚本生成器
        f.write("\n[2] 创建脚本生成器\n")
        generator = ScriptGenerator('xiaohongshu')
        f.write(f"  分镜数量: {generator.segments_count}\n")
        
        f.write("\n" + "=" * 50 + "\n")
        f.write("运行成功！\n")
        f.write("=" * 50 + "\n")
    
    print(f"输出已保存到: {output_file}")

if __name__ == '__main__':
    main()
