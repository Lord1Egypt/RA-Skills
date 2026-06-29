---
name: "ppt-style-matcher"
description: "v4.1: 全局色板提取+智能采样颜色多样性+P0-P3验证+深色适配+sldIdLst重建法"
---

# PPT风格匹配技能 v4.1

> **核心思路**：分析原PPT风格 → 锁定配色/字体/布局参数 → 用python-pptx生成新页面 → 完全重建sldIdLst → P0-P3分级验证
>
> ⚠️ **v4.1关键改进**：色板提取用全局颜色频率（不再依赖采样页偏差）、智能采样增加颜色多样性、深色PPT文字色修正

---

## ⛔ 强制约束（7条，不可跳过）

| # | 规则 | 说明 |
|---|------|------|
| R1 | **颜色锁定** | 只允许使用从原PPT提取的5色+2文字色，禁止编造hex |
| R2 | **字体锁定** | 三级分工（标题/正文/注释），禁止换字体 |
| R3 | **布局计算先行** | 禁止凭感觉填坐标，所有位置必须从公式计算 |
| R4 | **只用形状+文本** | 禁止外部图片、禁止pptxgenjs（它会丢中文和关系） |
| R5 | **间距保护** | 分栏间距0.6-1.0cm，内容距底≥0.15cm |
| R6 | **每页≥20个shape** | 低于此数为简单文本页，需重设计 |
| R7 | **验证读回** | 生成完毕必须用python-pptx读回+validate_layout()检查 |

---

## 第一步：需求澄清（6问法，借鉴guizang）

在动手之前，先回答6个问题。**不回答完不开始。**

1. **目标页**：修改哪些页？（页码范围）
2. **修改类型**：新增页？替换页？还是美化已有页？
3. **内容来源**：内容是已存在的还是需要我搜索整理？
4. **风格参考**：是否有参考页？（如"像第8页那样的风格"）
5. **特殊要求**：有无特殊布局需求？（如"数据要突出""要有流程图"）
6. **输出路径**：修改后的文件保存到哪里？

---

## 第二步：风格分析

运行 `scripts/analyze_style.py` 提取风格参数：

```bash
python3 scripts/analyze_style.py <ppt路径> [--verbose]
```

**必须确认以下参数后再继续（防幻觉）**：

### 2.1 5色锁定色板

脚本自动提取，输出格式：
```
COLOR_PRIMARY: #22C55E   ← 主色，最高频非白非黑填充色
COLOR_SECONDARY: #374151  ← 辅色，中性色优先（深灰/深蓝/深绿）
COLOR_ACCENT: #C00000     ← 强调色，高饱和色优先（红/橙/蓝）
COLOR_BG: #FFFFFF          ← 背景色
COLOR_TEXT: #1F2937        ← 主文字色（浅色PPT选深色，深色PPT选浅色）
COLOR_TEXT_LIGHT: #4B5563  ← 辅文字色
IS_DARK_THEME: False       ← 是否深色主题
```

⚠️ **v4改进**：
- 深色PPT自动检测，TEXT色适配（选白色/浅灰而非红色）
- SECONDARY优先中性色，ACCENT优先高饱和色，不再角色倒挂
- 默认采样改为智能选择设计良好的页面（shape≥20优先）

### 2.2 字体三级分工

按字号范围推断：
- **标题字体**：≥20pt 的最高频字体
- **正文字体**：14-19pt 的最高频字体
- **注释字体**：<14pt 的最高频字体

⚠️ 如果三个级别是同一字体（常见于中文PPT），标题用加粗、正文用常规即可。

### 2.3 布局参数

从 `--verbose` 输出中提取：
- `MARGIN_L / MARGIN_R`：左右安全边距
- `HEADER_H`：标题区高度
- `FOOTER_H`：底部装饰条高度
- `CONTENT_X/Y/W/H`：内容区范围
- `has_left_right_split`：是否左右分栏及比例
- `is_simple_page`：是否简单页（shape<10，布局参数无参考价值）

⚠️ **v4改进**：简单页（shape<10）的布局参数自动清空，避免误导。参考页推荐在分析结果末尾输出。

### 2.4 节奏感

脚本自动检测节奏，根据PPT类型切换策略：
- **深色/混合PPT**：检测连续深/浅色页面，≥3页连续报视觉疲劳
- **浅色PPT**（>85%浅色页）：检测章节分隔页间距和连续稀疏页，不再误报"连续浅色"

⚠️ **v4改进**：浅色PPT不再报"连续37页浅色=视觉疲劳"，改用结构节奏检测。

---

## 第三步：内容确定

1. 用python-pptx读取目标页的纯文本内容
2. 如需新增内容，搜索整理后写入
3. 按内容量选择合适的布局模式（见 design-patterns.md）

---

## 第四步：布局计算（核心！）

**所有坐标必须从公式算出，禁止硬编码。**

### 基础参数（从第二步提取）

```python
SLIDE_W = 33.87  # cm, 从分析结果
SLIDE_H = 19.05  # cm
MARGIN_L = 2.1
MARGIN_R = 1.8
HEADER_H = 3.5   # 标题区
FOOTER_H = 3.0   # 底部装饰条（如有）

CONTENT_X = MARGIN_L
CONTENT_Y = HEADER_H + 0.5  # 标题下方0.5cm
CONTENT_W = SLIDE_W - MARGIN_L - MARGIN_R
CONTENT_H = SLIDE_H - CONTENT_Y - FOOTER_H - 0.3
```

### 双栏布局公式

```python
GAP = 0.8  # 分栏间距，0.6-1.0cm范围

# 根据内容量选择比例
# 文字密集 → 0.58 | 适中 → 0.6 | 精简 → 0.5
ratio_left = 0.6

LEFT_W  = (CONTENT_W - GAP) * ratio_left
RIGHT_W = (CONTENT_W - GAP) * (1 - ratio_left)
LEFT_X  = CONTENT_X
RIGHT_X = CONTENT_X + LEFT_W + GAP

# ⚠️ 验证：LEFT_X + LEFT_W + GAP + RIGHT_W 应 ≈ CONTENT_X + CONTENT_W
```

### 三栏布局公式

```python
COL3_GAP = 0.6
COL3_W = (CONTENT_W - 2 * COL3_GAP) / 3
COL3_X = [CONTENT_X + i * (COL3_W + COL3_GAP) for i in range(3)]
```

### 卡片内部结构

```python
# 左装饰条
DECOR_W = 0.2  # cm
decor_x = card_x
decor_w = DECOR_W
decor_h = card_h

# 标题
title_x = card_x + DECOR_W + 0.2
title_w = card_w - DECOR_W - 0.4
title_pt = 14  # 三级标题

# 描述
desc_x = title_x
desc_w = title_w
desc_pt = 12  # 注释字号
```

---

## 第五步：节奏感规划

参考第二步的节奏感检测结果：
- 如果目标页前后都是浅色页，考虑给新页加一个深色强调元素
- 连续新增多页时，交替使用深色和浅色背景
- 深色页定义：深色面积占比 > 25%

---

## 第六步：python-pptx创建新页面

### 6.1 创建shape的标准代码

```python
from pptx import Presentation
from pptx.util import Cm, Pt, Emu
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT
from pptx.dml.color import RGBColor

# ⚠️ PP_PARAGRAPH_ALIGNMENT 用法：
# PP_PARAGRAPH_ALIGNMENT.LEFT    左对齐
# PP_PARAGRAPH_ALIGNMENT.CENTER  居中
# PP_PARAGRAPH_ALIGNMENT.RIGHT   右对齐
# PP_PARAGRAPH_ALIGNMENT.JUSTIFY 两端对齐
# 不要用 pp.ALIGN_LEFT 等旧写法！

def add_shape(slide, left, top, width, height, fill_color=None):
    """添加矩形shape"""
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE.RECTANGLE
        Cm(left), Cm(top), Cm(width), Cm(height)
    )
    shape.line.fill.background()  # 无边框
    
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor.from_string(fill_color)
    
    return shape

def add_textbox(slide, left, top, width, height, text, font_name='Noto Sans SC',
                font_size=14, bold=False, color='1F2937', align='left'):
    """添加文本框"""
    txBox = slide.shapes.add_textbox(
        Cm(left), Cm(top), Cm(width), Cm(height)
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = text
    
    # 对齐方式
    align_map = {
        'left': PP_PARAGRAPH_ALIGNMENT.LEFT,
        'center': PP_PARAGRAPH_ALIGNMENT.CENTER,
        'right': PP_PARAGRAPH_ALIGNMENT.RIGHT,
        'justify': PP_PARAGRAPH_ALIGNMENT.JUSTIFY,
    }
    p.alignment = align_map.get(align, PP_PARAGRAPH_ALIGNMENT.LEFT)
    
    run = p.runs[0]
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor.from_string(color)
    
    # ⚠️ 设置东亚字体（解决中文渲染问题）
    set_ea_font(run, font_name)
    
    return txBox
```

### 6.2 中文字体处理方案（必做！）

```python
from scripts.analyze_style import set_ea_font, set_line_spacing, clean_shape

# 每个文字run都必须设置东亚字体
run.font.name = "Noto Sans SC"  # 西文字体
set_ea_font(run, "Noto Sans SC")  # 东亚字体（必做！）

# 显式设置行距
p = tf.paragraphs[0]
set_line_spacing(p, font_size_pt=14, ratio=1.35)

# 创建shape后清理自动样式
shape = add_shape(...)
clean_shape(shape)
```

⚠️ **踩坑记录**：`PP_PARAGRAPH_ALIGNMENT` 是枚举类，不是模块常量。正确写法是 `PP_PARAGRAPH_ALIGNMENT.LEFT`，不是 `PP_PARAGRAPH_ALIGNMENT.LEFT` 从 `pptx.enum` 直接导入。

---

## 第七步：替换、排序、残留修复

### 7.1 sldIdLst操作（⚠️ 最大坑！必须用完全重建法）

python-pptx 的 slide 顺序由 `presentation.xml` 中的 `<p:sldIdLst>` 控制。
**不能用** `addprevious`/`addnext` 连续操作（索引会变导致顺序错乱）。
**唯一可靠方法：清空sldIdLst → 按新顺序append。**

```python
from lxml import etree

# ✅ 正确的API（python-pptx没有 prs.presentation.sldIdLst 属性！）
ns = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
sldIdLst = prs.part._element.find(f'{ns}sldIdLst')

# 1. 创建新slide（python-pptx会自动追加到末尾）
for i in range(4):  # 4页新slide
    prs.slides.add_slide(prs.slide_layouts[6])

# 2. 记录当前sldIdLst的所有元素
all_ids = list(sldIdLst)

# 3. 确定新的页面顺序
# 假设：原PPT有63页，新4页在末尾（-4），要替换第2-5页（index 1-4）
new_ids = all_ids[-4:]          # 新页面
keep_ids = [all_ids[0]] + all_ids[5:-4]  # 第1页 + 第6-63页

desired_order = keep_ids[:1] + new_ids + keep_ids[1:]
# 结果：[原1, 新1, 新2, 新3, 新4, 原6, 原7, ..., 原63]

# 4. 完全重建sldIdLst（⚠️ 不要用addprevious/addnext！）
for sid in list(sldIdLst):
    sldIdLst.remove(sid)
for sid in desired_order:
    sldIdLst.append(sid)

# 5. 保存
prs.save(output_path)
```

⚠️ **常见错误**：
- `prs.presentation.sldIdLst` → API不存在，必须用 `prs.part._element.find()`
- `sldIdLst.insert(idx, elem)` → lxml虽然支持，但连续insert索引会变
- 只删除sldId但不删除底层slide part → 文件会膨胀（目前未自动清理）

### 7.2 模板残留修复

扫描所有页文字，替换模板残留关键词：
```python
RESIDUAL_KEYWORDS = ['OPPO', 'Tony', 'Alen', '逍遥子', '逍遥子班']
REPLACEMENTS = {
    'OPPO': '国药太极',
    'Tony': '导师A',
    'Alen': '导师B',
    '逍遥子班': '领航班',
    '逍遥子': '领航',
}

for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    for old, new in REPLACEMENTS.items():
                        if old in run.text:
                            run.text = run.text.replace(old, new)
```

---

## 第八步：P0-P3分级质检

### 8.1 自动验证（脚本）

```python
from scripts.analyze_style import validate_layout

result = validate_layout(
    prs,
    slide_indices=[1, 2, 3, 4],  # 新增/修改的页索引（0-based）
    palette=palette,              # 5色色板
    residual_keywords=['OPPO', 'Tony', 'Alen'],  # 残留关键词
)

print(f"P0通过: {result['passed']}")
for level in ['P0', 'P1', 'P2', 'P3']:
    if result[level]:
        print(f"\n{level}问题:")
        for issue in result[level]:
            print(f"  - {issue}")
```

### 8.2 分级标准

| 级别 | 类型 | 检查项 | 不通过后果 |
|------|------|--------|-----------|
| P0 | 阻断级 | 越界/图片shape/shape<20/残留关键词 | **不交付** |
| P1 | 功能级 | 颜色一致性/底部留白/文字溢出 | 需修复 |
| P2 | 品质级 | 间距均匀/对齐/标题统一 | 建议修复 |
| P3 | 润色级 | 节奏感/信息密度/装饰元素 | 可选 |

---

## v4.1 修复/改进清单

| 问题 | 修复 | 影响 |
|------|------|------|
| 智能采样只看shape数量，选出的页颜色偏红 | 新增颜色多样性加分+贪心算法确保颜色覆盖 | 色板无偏差 |
| 色板提取只用采样页频率（采样偏差） | PRIMARY等核心角色改用全局颜色频率 | 色板准确 |
| validate_color_usage缩进bug（只检查最后一个slide） | for循环体修正缩进 | P1颜色验证生效 |
| SKILL.md sldIdLst API过时 | 改为完全重建法 + prs.part._element.find() | 代码可运行 |
| 深色PPT TEXT色被识别为强调色 | 检测深色主题后TEXT优先选浅色 | 色板正确 |
| SECONDARY/ACCENT角色倒挂 | SECONDARY优先中性色，ACCENT优先高饱和色 | 角色语义正确 |
| 默认采样4页中3页是简单页 | 智能采样：优先shape≥20的设计良好页+颜色多样性 | 色板质量提升 |
| 简单页布局参数误导 | shape<10标记为简单页，清空布局参数 | 避免误导 |
| 浅色PPT报"连续37页浅色=视觉疲劳" | 浅色PPT切换为结构节奏检测 | 不误报 |
| 缺少参考页推荐 | analyze_ppt自动输出参考页 | 免手动选择 |
| validate_layout坐标计算bug | 改为Emu(left + width) | 越界检测准确 |
| design-patterns.md缺sldIdLst操作指南 | 新增第十节：清空+按序重建法 | 最少踩坑 |

## v3.1 修复清单（已包含在v4中）

| 问题 | 修复 | 影响 |
|------|------|------|
| 全屏背景色块被误判为"顶部装饰条" | 新增 `_is_fullscreen_shape()` 过滤 | 布局参数准确 |
| 节奏感警告重复 | 滑动窗口找最长连续区间 | 输出简洁 |
| 5色色板PRIMARY和TEXT重复 | 区分填充色和文字色角色 | 色板可用 |
| ACCENT提取到极浅色 | bg_colors排除 + 亮度>240跳过 | 强调色有意义 |
| 字体三级分工只有1个字体 | 按字号范围推断三级 | 信息完整 |
| 底部装饰条全部0.0 | 降低检测阈值 | 可检测到 |
| validate_layout不存在 | 新增完整函数 | 可用 |
| PP_PARAGRAPH_ALIGNMENT用法未说明 | 新增代码模板 | 避免枚举错误 |
| shape位置为None时崩溃 | 统一过滤None位置shape | 稳定 |

---

## 文件结构

```
ppt-style-matcher/
├── SKILL.md                      # 本文件 (v4)
├── scripts/
│   └── analyze_style.py          # 风格分析工具 v4
└── references/
    └── design-patterns.md        # 设计模式参考
```

### analyze_style.py 导出函数

| 函数 | 用途 |
|------|------|
| `analyze_ppt(path, pages, verbose)` | 完整风格分析（入口函数，含参考页推荐） |
| `extract_color_palette(prs, pages)` | 5色锁定色板提取（v4：深色适配+角色修正） |
| `analyze_layout_ratios(slide, prs)` | 单页布局比例参数（v4：简单页跳过） |
| `analyze_rhythm(prs, pages)` | 节奏感检测（v4：浅色PPT结构节奏） |
| `validate_color_usage(prs, palette, indices)` | 颜色一致性验证（v4：修复缩进bug） |
| `validate_layout(prs, indices, palette, keywords)` | P0-P3分级质检 |
| `_is_dark_ppt(prs, pages)` | 判断深色主题 |
| `_pick_best_sample_pages(prs, count)` | 智能采样（优先设计良好页） |
| `set_ea_font(run, font_name)` | 设置东亚字体（辅助） |
| `set_line_spacing(paragraph, pt, ratio)` | 设置行距（辅助） |
| `clean_shape(shape)` | 清理自动样式（辅助） |
