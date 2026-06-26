#!/usr/bin/env python3
"""测试指定字体的显示效果"""

import sys
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 检查参数
if len(sys.argv) < 2:
    print("用法: python3 test_font.py <字体名称> [输出路径]")
    print("示例: python3 test_font.py 'Heiti TC' /tmp/font_test.png")
    sys.exit(1)

font_name = sys.argv[1]
output_path = sys.argv[2] if len(sys.argv) > 2 else '/tmp/font_test.png'

# 检查字体是否存在
available_fonts = set([f.name for f in fm.fontManager.ttflist])
if font_name not in available_fonts:
    print(f"❌ 字体 '{font_name}' 不存在")
    print("\n可用中文字体:")
    chinese_keywords = ['hei', 'song', 'kai', 'fang', 'ming', 'ping']
    for f in sorted(available_fonts):
        if any(kw in f.lower() for kw in chinese_keywords):
            print(f"  - {f}")
    sys.exit(1)

# 创建测试图
plt.figure(figsize=(8, 4))
plt.rcParams['axes.unicode_minus'] = False

x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x), linewidth=2)

plt.title(f'字体测试: {font_name} - 数据可视化图表', fontsize=14, fontname=font_name)
plt.xlabel('X 轴标签', fontsize=12, fontname=font_name)
plt.ylabel('Y 轴标签', fontsize=12, fontname=font_name)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_path, dpi=120, bbox_inches='tight')
print(f"✅ 测试图已保存到 {output_path}")
print(f"使用字体: {font_name}")
