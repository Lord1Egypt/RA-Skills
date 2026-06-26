---
name: matplotlib-chinese-font
description: Configure Chinese fonts for matplotlib plotting. Use when plotting charts with Chinese characters or getting garbled text.
---

# Matplotlib 中文字体配置

## 何时使用

- matplotlib 图表中出现中文乱码（显示为方块）
- 需要在图表中使用中文标题、标签、图例
- 需要区分不同中文字体效果（如宋体 vs 黑体）

## 快速配置

### 方法 1：全局配置（推荐）

```python
import matplotlib.pyplot as plt

# 配置中文字体
plt.rcParams['font.sans-serif'] = ['Heiti TC']  # 华文黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 绘制图表
plt.plot([1, 2, 3], [1, 2, 3])
plt.title('测试标题', fontsize=14)
plt.xlabel('X 轴')
plt.ylabel('Y 轴')
plt.show()
```

### 方法 2：强制指定字体（更可靠）

当全局配置不生效时，在具体元素上强制指定：

```python
plt.title('图表标题', fontsize=14, fontname='Heiti TC')
plt.xlabel('X 轴', fontsize=12, fontname='Heiti TC')
plt.ylabel('Y 轴', fontsize=12, fontname='Heiti TC')
plt.text(0.5, 0.5, '文本标注', fontname='Heiti TC')
```

### 可用字体

常用系统字体：
- **Heiti TC** - 华文黑体（用户偏好）
- Songti SC - 华文宋体

查询所有可用字体：
```bash
python3 -c "import matplotlib.font_manager as fm; print('\n'.join(sorted(set([f.name for f in fm.fontManager.ttflist]))))"
```

## 常见问题

### 字体不生效

1. **清除字体缓存**
   ```bash
   rm -rf ~/.matplotlib
   ```
   或运行 `scripts/clear_cache.py`

2. **强制指定字体**
   使用 `fontname` 参数而不是 `rcParams`

3. **检查字体是否存在**
   运行 `scripts/list_fonts.py` 查看系统可用字体

### 负号显示为方块

```python
plt.rcParams['axes.unicode_minus'] = False
```

### 保存图片时中文乱码

确保保存前字体已正确设置：
```python
plt.savefig('/tmp/chart.png', dpi=120, bbox_inches='tight')
```

## 脚本工具

- `scripts/clear_cache.py` - 清除 matplotlib 字体缓存
- `scripts/list_fonts.py` - 列出系统可用中文字体
- `scripts/test_font.py` - 测试指定字体的显示效果

## 参考资料

- `references/troubleshooting.md` - 详细问题排查指南
