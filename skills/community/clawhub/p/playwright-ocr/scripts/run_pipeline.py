#!/usr/bin/env python3
"""
完整数据提取流程
1. Playwright 截图
2. OCR 识别
3. 数据导出
"""
import subprocess, json, os, sys
from datetime import datetime

def run_command(cmd, description):
    """运行命令并显示进度"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True, capture_output=False)
    return result.returncode == 0

def main():
    SKILL_DIR = '/root/.openclaw/workspace/skills/playwright_ocr'
    OUTPUT_DIR = f'{SKILL_DIR}/output'
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print('=' * 60)
    print('🤖 Playwright_OCR 完整流程')
    print('=' * 60)
    print(f"📂 输出目录：{OUTPUT_DIR}")
    
    # 步骤 1: Playwright 截图
    if not run_command(
        f"cd {SKILL_DIR} && node scripts/extract_data.js",
        "步骤 1: Playwright 浏览器自动化"
    ):
        print("❌ Playwright 提取失败")
        sys.exit(1)
    
    # 步骤 2: OCR 处理
    if not run_command(
        f"python3 {SKILL_DIR}/scripts/process_ocr.py",
        "步骤 2: OCR 数据处理"
    ):
        print("⚠️  OCR 处理失败，继续下一步")
    
    # 步骤 3: 数据验证
    csv_file = f'{OUTPUT_DIR}/extracted_data.csv'
    if os.path.exists(csv_file):
        with open(csv_file) as f:
            lines = f.readlines()
        print(f"\n{'='*60}")
        print(f"✅ 数据提取完成！")
        print(f"📊 总记录数：{len(lines)-1} 条")
        print(f"📄 CSV 文件：{csv_file}")
        print(f"{'='*60}")
    else:
        print(f"\n❌ CSV 文件未生成")
        sys.exit(1)

if __name__ == '__main__':
    main()
