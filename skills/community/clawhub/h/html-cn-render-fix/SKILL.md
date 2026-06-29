# 🔧 HTML 转图片中文无乱码解决方案

> 解决 Python 生成图片时中文显示为方框/乱码的问题

## 问题背景

在使用 matplotlib、pyppeteer 等工具生成包含中文的图片时，经常遇到：
- ❌ 中文显示为方框 □□□
- ❌ 部分字符显示为乱码
- ❌ emoji 显示异常

## 根本原因

1. **字体缺失** - 系统没有安装中文字体
2. **字体配置错误** - matplotlib 默认使用 DejaVu 字体（不支持中文）
3. **emoji 兼容性问题** - 某些 emoji 在某些字体/系统中不支持

## 解决方案

### 方案 1：使用 FontProperties 直接加载字体文件（推荐）

```python
from matplotlib.font_manager import FontProperties

# 直接加载字体文件
font_path = '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc'
font_prop = FontProperties(fname=font_path)

# 在每个文本渲染处使用
fig.suptitle('中文标题', fontsize=16, fontproperties=font_prop)
ax.set_xlabel('X 轴标签', fontproperties=font_prop)
ax.set_ylabel('Y 轴标签', fontproperties=font_prop)
ax.annotate('标注文字', xy=(x, y), fontproperties=font_prop)

# 设置图例
leg = ax.legend()
for text in leg.get_texts():
    text.set_fontproperties(font_prop)

# 设置坐标轴标签
for label in ax.get_xticklabels():
    label.set_fontproperties(font_prop)
```

**优点：**
- ✅ 不依赖系统字体配置
- ✅ 明确指定字体文件，可靠性高
- ✅ 适用于所有 matplotlib 文本元素

### 方案 2：配置 rcParams（不推荐）

```python
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
```

**缺点：**
- ❌ 依赖系统字体配置
- ❌ 可能被其他配置覆盖
- ❌ 在某些环境下无效

### 方案 3：避免使用 emoji（最安全）

某些 emoji（特别是国旗 emoji 🇨🇳🇺🇸）在某些系统中不支持：

```python
# ❌ 避免使用
title = "🇨🇳 中国股票"

# ✅ 使用文字代替
title = "中国股票"

# ✅ 或使用通用 emoji
title = "📈 中国股票"  # 图表 emoji 兼容性更好
```

## 完整示例

```python
#!/usr/bin/env python3
"""
HTML 转图片中文无乱码示例
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import io
import base64

# 加载字体文件
font_path = '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc'
font_prop = FontProperties(fname=font_path)
font_prop_title = FontProperties(fname=font_path, size=16, weight='bold')
font_prop_label = FontProperties(fname=font_path, size=12)

# 创建图表
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('中文标题示例', fontsize=16, fontproperties=font_prop_title)

# 绘制数据
ax.plot([1, 2, 3, 4], [1, 4, 2, 3], label='数据曲线')

# 设置标签（使用 fontproperties）
ax.set_xlabel('X 轴', fontsize=12, fontproperties=font_prop_label)
ax.set_ylabel('Y 轴', fontsize=12, fontproperties=font_prop_label)
ax.set_title('图表标题', fontsize=12, fontproperties=font_prop_label)

# 设置图例
leg = ax.legend()
for text in leg.get_texts():
    text.set_fontproperties(font_prop)

# 设置坐标轴刻度标签
for label in ax.get_xticklabels():
    label.set_fontproperties(font_prop)
for label in ax.get_yticklabels():
    label.set_fontproperties(font_prop)

# 添加标注
ax.annotate('最高点', xy=(2, 4), xytext=(2.5, 4.5),
            fontproperties=font_prop,
            arrowprops=dict(arrowstyle='->'))

# 保存为 base64
buf = io.BytesIO()
plt.savefig(buf, dpi=100, bbox_inches='tight', format='png')
buf.seek(0)
img_base64 = base64.b64encode(buf.read()).decode('utf-8')
plt.close()

print(f"✅ 生成成功！图片大小：{len(img_base64)} bytes")
```

## 系统字体安装

### Ubuntu/Debian

```bash
# 安装 Noto CJK 字体
apt-get install fonts-noto-cjk -y

# 或安装文泉驿字体
apt-get install fonts-wqy-microhei fonts-wqy-zenhei -y
```

### CentOS/RHEL

```bash
# 安装 Noto CJK 字体
yum install google-noto-sans-cjk-fonts -y

# 或安装文泉驿字体
yum install wqy-microhei-fonts wqy-zenhei-fonts -y
```

### macOS

```bash
# 使用 Homebrew
brew install --cask font-noto-sans-cjk
```

## 检查字体

```bash
# 查看已安装的中文字体
fc-list :lang=zh

# 查看特定字体
fc-list | grep -i "noto\|cjk\|wenquanyi"

# 测试字体
fc-match "Noto Sans CJK SC"
```

## 常见问题

### Q: 为什么设置了字体还是乱码？

A: 确保：
1. 字体文件路径正确
2. 每个文本元素都使用了 `fontproperties=font_prop`
3. 清除了 matplotlib 缓存：`rm -rf ~/.cache/matplotlib`

### Q: emoji 显示为方框怎么办？

A: 避免使用复杂 emoji（特别是国旗 emoji），改用：
- 简单 emoji（📈📉📊💰等）
- 纯文字
- Unicode 基本字符（↑↓←→等）

### Q: 图片生成很慢？

A: 首次运行会加载字体，后续会使用缓存。可以预加载字体：
```python
from matplotlib import font_manager
font_manager.fontManager.addfont(font_path)
```

## 最佳实践

1. ✅ **始终使用 FontProperties** - 不依赖 rcParams
2. ✅ **避免复杂 emoji** - 使用简单 emoji 或文字
3. ✅ **清理缓存** - 字体问题时常清理 `~/.cache/matplotlib`
4. ✅ **测试验证** - 生成后检查图片是否有方框
5. ✅ **记录字体路径** - 在代码中明确记录使用的字体文件路径

## 参考资源

- [Matplotlib 字体管理文档](https://matplotlib.org/stable/users/explain/text/font_management.html)
- [Noto CJK 字体下载](https://github.com/googlefonts/noto-cjk)
- [文泉驿字体](https://sourceforge.net/projects/wqy/)

---

**许可证：** MIT

**版本：** 1.0.0
