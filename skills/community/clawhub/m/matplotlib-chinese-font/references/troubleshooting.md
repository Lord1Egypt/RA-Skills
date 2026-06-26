# 故障排查指南

## 字体不生效

### 症状
- 图表中中文显示为方块 (□□□)
- 字体设置后无变化

### 解决方案

1. **清除字体缓存**
   ```bash
   rm -rf ~/.matplotlib
   ```
   或运行:
   ```bash
   python3 scripts/clear_cache.py
   ```

2. **使用强制指定方式**
   不要用 `rcParams`，改用 `fontname` 参数:
   ```python
   plt.title('标题', fontname='Heiti TC')
   ```

3. **确认字体存在**
   ```bash
   python3 scripts/list_fonts.py
   ```

## 负号显示异常

### 症状
- 图表中的负号显示为方块

### 解决方案
```python
plt.rcParams['axes.unicode_minus'] = False
```

## 保存图片中文乱码

### 症状
- 图表窗口中显示正常，保存后中文变方块

### 解决方案
1. 使用 `fontname` 参数强制指定字体
2. 保存前确保所有文字元素都设置了字体:
   ```python
   plt.savefig('output.png', dpi=120, bbox_inches='tight')
   ```

## 字体名称错误

### 症状
```
findfont: Font family 'xxx' not found.
```

### 解决方案
- 字体名称区分大小写
- 使用 `scripts/list_fonts.py` 查看正确名称
- 常见错误:
  - `'heiti tc'` → `'Heiti TC'`
  - `'Songti SC'` → `'Songti SC'` (正确)

## macOS 特有问题

### 症状
- 系统有字体但 matplotlib 找不到

### 解决方案
1. 清除缓存
2. 重启 Python 进程
3. 使用完整字体路径:
   ```python
   font_path = '/System/Library/Fonts/STHeiti Medium.ttc'
   font_prop = fm.FontProperties(fname=font_path)
   plt.title('标题', fontproperties=font_prop)
   ```

## 代码示例：完整配置模板

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# ============ 字体配置 ============
# 方法1: 全局配置
plt.rcParams['font.sans-serif'] = ['Heiti TC']
plt.rcParams['axes.unicode_minus'] = False

# 方法2: 强制指定（推荐，更可靠）
FONT = 'Heiti TC'
# ==================================

# 绘图代码
fig, ax = plt.subplots(figsize=(10, 6))
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), linewidth=2, label='正弦曲线')
ax.plot(x, np.cos(x), linewidth=2, label='余弦曲线')

ax.set_title('三角函数图表', fontsize=14, fontname=FONT)
ax.set_xlabel('角度 (弧度)', fontsize=12, fontname=FONT)
ax.set_ylabel('数值', fontsize=12, fontname=FONT)
ax.legend(prop={'family': FONT})
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/tmp/chart.png', dpi=120, bbox_inches='tight')
plt.show()
```
