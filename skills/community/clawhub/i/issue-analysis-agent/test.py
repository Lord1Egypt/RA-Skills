#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能测试脚本 - 验证客服问题分析技能
版本：v1.1.0
"""

import sys
import os
from pathlib import Path

# 切换到技能目录
os.chdir(Path(__file__).parent)

print("=" * 60)
print("🧪 客服问题分析技能 - 测试")
print("=" * 60)

# 测试 1: 检查依赖
print("\n【测试 1/5】检查依赖...")
try:
    import openpyxl
    print("  ✅ openpyxl 已安装")
except:
    print("  ❌ openpyxl 未安装，运行：pip3 install openpyxl")
    sys.exit(1)

try:
    from qcloud_cos import CosConfig
    print("  ✅ qcloud_cos 已安装")
except:
    print("  ❌ qcloud_cos 未安装，运行：pip3 install cos-python-sdk-v5")
    sys.exit(1)

# 测试 2: 检查脚本
print("\n【测试 2/5】检查脚本文件...")
scripts = [
    'analyze.py',
    'generate_report.py',
    'upload_cos.py',
    'weekly_report.py'
]

for script in scripts:
    if Path(script).exists():
        print(f"  ✅ {script}")
    else:
        print(f"  ❌ {script} 不存在")
        sys.exit(1)

# 测试 3: 检查配置
print("\n【测试 3/5】检查配置文件...")
if Path('config.json').exists():
    print("  ✅ config.json")
else:
    print("  ❌ config.json 不存在")

# 测试 4: 检查输出目录
print("\n【测试 4/5】检查输出目录...")
output_dir = Path('output')
output_dir.mkdir(exist_ok=True)
print(f"  ✅ output/ 目录已创建")

# 测试 5: 检查示例数据
print("\n【测试 5/5】检查示例数据...")
test_files = [
    '../../projects/issue_analysis/issue_data_latest.xlsx'
]

test_file = None
for f in test_files:
    if Path(f).exists():
        test_file = f
        print(f"  ✅ 找到测试文件：{f}")
        break

if not test_file:
    print("  ⚠️ 未找到测试文件，跳过实际运行测试")
    print("\n" + "=" * 60)
    print("✅ 技能配置检查完成！")
    print("=" * 60)
    print("\n使用方法:")
    print("  python3 weekly_report.py /path/to/issue_data.xlsx")
    sys.exit(0)

# 运行实际测试
print("\n" + "=" * 60)
print("🚀 开始实际运行测试...")
print("=" * 60)

from weekly_report import weekly_report

result = weekly_report(test_file)

if result:
    print("\n" + "=" * 60)
    print("✅ 所有测试通过！")
    print("=" * 60)
    print(f"\n📊 测试报告链接:")
    print(f"  {result['url']}")
else:
    print("\n" + "=" * 60)
    print("❌ 测试失败")
    print("=" * 60)
    sys.exit(1)
