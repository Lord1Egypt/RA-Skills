#!/usr/bin/env python3
"""
HTML 转图片中文无乱码示例脚本
演示如何正确使用中文字体生成图片
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import io
import base64
import os

# 字体文件路径
font_path = '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc'

# 检查字体文件是否存在
if not os.path.exists(font_path):
    print(f"⚠️ 字体文件不存在：{font_path}")
    print("请先安装中文字体：")
    print("  Ubuntu/Debian: apt-get install fonts-noto-cjk -y")
    print("  CentOS/RHEL: yum install google-noto-sans-cjk-fonts -y")
    exit(1)

# 加载字体
font_prop = FontProperties(fname=font_path)
font_prop_title = FontProperties(fname=font_path, size=16, weight='bold')
font_prop_label = FontProperties(fname=font_path, size=12)
font_prop_small = FontProperties(fname=font_path, size=9)

print("✅ 字体加载成功")

# 创建图表
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('中文标题示例 - K 线图', fontsize=16, fontweight='bold', fontproperties=font_prop_title)

# 模拟数据
x = range(10)
y = [100, 102, 105, 103, 107, 110, 108, 112, 115, 113]

# 绘制
ax.plot(x, y, 'r-', linewidth=2, label='价格曲线')
ax.fill_between(x, y, alpha=0.3, color='red')

# 设置标签
ax.set_xlabel('日期', fontsize=12, fontproperties=font_prop_label)
ax.set_ylabel('价格 (元)', fontsize=12, fontproperties=font_prop_label)
ax.set_title('股票价格走势', fontsize=12, fontproperties=font_prop_label)

# 设置图例
leg = ax.legend(loc='upper left')
for text in leg.get_texts():
    text.set_fontproperties(font_prop)

# 设置坐标轴刻度
for label in ax.get_xticklabels():
    label.set_fontproperties(font_prop)
for label in ax.get_yticklabels():
    label.set_fontproperties(font_prop)

# 添加标注
ax.annotate('最高点\n115 元', xy=(8, 115), xytext=(6, 118),
            fontproperties=font_prop_small,
            arrowprops=dict(arrowstyle='->', color='green'))
ax.annotate('支撑位', xy=(5, 107), xytext=(7, 105),
            fontproperties=font_prop_small,
            arrowprops=dict(arrowstyle='->', color='blue'))

# 添加水平线（支撑位/压力位）
ax.axhline(y=107, color='blue', linestyle='--', alpha=0.5, label='支撑位')
ax.axhline(y=115, color='green', linestyle='--', alpha=0.5, label='压力位')

# 网格
ax.grid(True, alpha=0.3)

# 保存
plt.tight_layout()
output_file = '/tmp/cn-font-test.png'
plt.savefig(output_file, dpi=100, bbox_inches='tight', facecolor='white')
plt.close()

print(f"✅ 图片生成成功：{output_file}")
print(f"📊 图片大小：{os.path.getsize(output_file)} bytes")

# 也可以生成 base64
buf = io.BytesIO()
plt = plt.subplots(figsize=(10, 6))[0]
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
img_base64 = base64.b64encode(buf.read()).decode('utf-8')
print(f"📦 Base64 长度：{len(img_base64)} characters")

print("\n✅ 完成！请检查 /tmp/cn-font-test.png")
print("如果中文显示正常，说明字体配置成功！")
