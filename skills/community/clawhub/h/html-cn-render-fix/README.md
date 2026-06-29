# 🔧 HTML 转图片中文无乱码解决方案

快速解决 Python 生成图片时中文显示为方框/乱码的问题。

## 快速使用

### 1. 安装中文字体

```bash
# Ubuntu/Debian
apt-get install fonts-noto-cjk -y

# CentOS/RHEL
yum install google-noto-sans-cjk-fonts -y
```

### 2. 使用示例

```python
from matplotlib.font_manager import FontProperties

# 加载字体
font_path = '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc'
font_prop = FontProperties(fname=font_path)

# 在文本渲染处使用
fig.suptitle('中文标题', fontproperties=font_prop)
ax.set_xlabel('X 轴', fontproperties=font_prop)
```

## 核心要点

1. **使用 FontProperties 直接加载字体文件**
2. **避免使用复杂 emoji（特别是国旗 emoji）**
3. **每个文本元素都要设置 fontproperties**

详细文档请查看 SKILL.md

## 许可证

MIT
