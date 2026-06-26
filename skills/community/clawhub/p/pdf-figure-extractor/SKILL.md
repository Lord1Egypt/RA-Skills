---
name: pdf-figure-extractor
description: 从PDF论文中精确提取Figure图片，自动分析PDF结构、定位caption位置、裁剪干净图形，并验证图片质量。支持学术新闻稿、论文写作等场景的自动化图片处理。
---

# PDF Figure提取技能

## 使用场景

- 从学术论文PDF提取Figure插入Word文档
- 需要干净、无caption、无正文的纯图形图片
- 批量提取多个Figure

## 标准工作流程

### 步骤1: 分析PDF结构
```python
import fitz

doc = fitz.open(pdf_path)
page = doc[page_num]

# 获取所有文本块
blocks = page.get_text("blocks")
for block in blocks:
    x0, y0, x1, y1, text, block_no, block_type = block
    if "Fig." in text or "Figure" in text:
        print(f"Figure相关: y={y0:.0f}-{y1:.0f}, {text[:50]}...")
```

### 步骤2: 定位Caption位置
```python
# 搜索Fig. X的精确位置
text_instances = page.search_for(f"Fig. {fig_num}")
for inst in text_instances:
    print(f"Fig.{fig_num}位置: y={inst.y0:.0f}-{inst.y1:.0f}")
```

### 步骤3: 确定裁剪区域
根据caption位置判断图形区域：

| Caption位置 | 图形区域 |
|------------|---------|
| y=400 (页面中部) | y=100-395 (caption上方) |
| y=666 (页面底部) | y=350-660 (caption上方) |
| y=326 (页面底部) | y=100-320 (caption上方) |

### 步骤4: 精确裁剪
```python
rect = fitz.Rect(50, y_start, page.rect.width - 50, y_end)
pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect)
pix.save(f"fig{fig_num}.png")
```

### 步骤5: 验证图片质量
检查清单：
- [ ] 包含所有子图(a,b,c,d...)
- [ ] 没有混入"Fig. X"开头的caption文字
- [ ] 没有混入正文段落
- [ ] 坐标轴和标签完整

## 常见PDF布局模板

### Nature/Science论文
- Fig.1: 通常caption在底部，图形y=350-660
- Fig.2+: caption位置不固定，需要先分析

### 会议论文
- 单栏布局: caption通常在图形下方
- 双栏布局: caption可能在图形上方或下方

## 错误处理

### 问题: 图片混入正文
**原因**: 裁剪范围太大
**解决**: 缩小y_end，确保在caption之前结束

### 问题: 子图缺失
**原因**: 裁剪范围太小
**解决**: 扩大y_start/y_end，包含完整图形

### 问题: caption未去除
**原因**: 裁剪范围包含了caption区域
**解决**: 根据caption的y坐标精确调整裁剪边界

## 最佳实践

1. **永远不要**凭感觉估计坐标
2. **始终先**分析PDF文本块结构
3. **高分辨率渲染**: 使用`matrix=fitz.Matrix(2, 2)`
4. **验证每张图片**: 确保干净无杂质
5. **记录坐标**: 为常见PDF类型建立坐标模板

## 触发关键词

"提取PDF图片", "从PDF提取Figure", "PDF图片裁剪", "学术论文图片提取"
