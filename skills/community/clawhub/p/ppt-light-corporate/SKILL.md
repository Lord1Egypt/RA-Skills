---
name: ppt-light-corporate
version: 1.1.0
description: |
  Generate polished corporate PPTs using a light-themed company template. Activate when:
  (1) User asks to create/make/generate a PPT/PowerPoint/幻灯片/演示文稿
  (2) User provides content and wants it turned into slides
  (3) User asks to improve or redo a PPT
  Uses a pre-analyzed H3C-style light corporate template (white bg + China red accent).
  NOT for: dark theme PPTs, creative/artistic decks, or Keynote files.
---

# PPT Light Corporate Skill

基于 python-pptx 的企业PPT自动生成引擎。H3C浅色企业模板，白底+中国红点缀，16:9画布。

## 核心文件

| 文件 | 作用 |
|------|------|
| `assets/template-light.pptx` | 模板文件（10" × 5.625"，9种Layout，5个母版） |
| `assets/icons-library.pptx` | 279个简洁矢量图标（设备相关） |
| `assets/icon-index.json` | 图标语义索引（中英文标签+场景分类） |
| `scripts/ppt_helpers.py` | 核心生成引擎（24种内容布局 + 工具方法） |
| `scripts/ppt_qa.py` | 自动QA审校（9项检查） |
| `scripts/ppt_scorer.py` | 评分系统（逐页6维 + 整体4维 + 学习循环） |
| `scripts/icon_library.py` | 图标搜索/复制/变色引擎 |

## Quick Start

```python
import sys
sys.path.insert(0, '<skill_dir>/scripts')
from ppt_helpers import TemplateBuilder

tb = TemplateBuilder()
s = tb.add_cover_slide()
tb.text(s, 0.8, 1.5, 8.4, 0.6, '标题', sz=32, color=tb.RED2, bold=True)

s = tb.add_content_slide('页面标题')
tb.three_col_icon_cards(s, [
    {'icon_text': '', 'title': '功能一', 'body': '说明'},
    {'icon_text': '', 'title': '功能二', 'body': '说明'},
    {'icon_text': '', 'title': '功能三', 'body': '说明'},
])

# 放置白色矢量图标到红色圆圈上（自动检测圆圈位置）
def find_circles(slide):
    circles = []
    for shape in slide.shapes:
        if 'Oval' in shape.name:
            x, y = shape.left / 914400, shape.top / 914400
            w, h = shape.width / 914400, shape.height / 914400
            circles.append({'cx': x + w/2, 'cy': y + h/2, 'w': w})
    return circles

for circle, query in zip(find_circles(s), ['server', 'wifi', 'database']):
    sz = circle['w'] * 0.55
    tb.place_icon(s, query, circle['cx'] - sz/2, circle['cy'] - sz/2, size=sz, color='FFFFFF')

tb.save('output.pptx')
```

## 设计系统

### 色板

| 名称 | 色值 | 用途 |
|------|------|------|
| RED | #C00000 | 页标题、强调 |
| RED2 | #EA0000 | 封面标题 |
| RED3 | #D8222A | 小节标题 |
| DARK | #343434 | 正文 |
| MID | #4B4948 | 次要文字 |
| LIGHT | #A0A0A0 | 辅助/淡化 |
| BG | #F1F1F1 | 卡片背景 |
| BORDER | #E7E7E7 | 边框/分隔线 |
| ACCENT_GREY | #6B6B6B | 交替强调（替代蓝色） |

### 配色法则
- 60% 白色(背景) / 30% 灰黑(正文) / 10% 红色(强调)
- 颜色只从色板里选，不引入新颜色

### 字体规范
- 字体：`微软雅黑`（latin + ea 同时设置）
- 页标题：20pt 粗体 RED
- 小节标题：12-14pt 粗体 RED/RED3
- 正文：10-11pt DARK/MID
- **最小字号：10pt**（确保投屏可读）

### 画布规则
- 画布：10" × 5.625"（16:9）
- 安全边距：≥ 0.4"
- 内容区起点：y = 1.0"（标题下方）
- 所有 body 文本启用 `shrink=True`（自动缩字防溢出）
- 多栏布局自动水平居中：`start_x = (10 - total_width) / 2`

## 24种内容布局

### 两栏/两行（5种）

| # | 方法 | 适用场景 |
|---|------|----------|
| 1 | `two_col_numbered_cards` | A/B对比 |
| 2 | `two_row_numbered_bars` | 两要点堆叠 |
| 3 | `two_row_label_tabs` | 分类标签+详情 |
| 4 | `two_col_circle_cards` | 人物/角色 |
| 5 | `left_text_right_stacked_cards` | 论点+论据（支持2-3张卡片自适应） |

### 三栏/三行（5种）

| # | 方法 | 适用场景 |
|---|------|----------|
| 6 | `three_col_vertical_cards` | 三个并列特性 |
| 7 | `three_row_numbered_bars` | 三步编号 |
| 8 | `three_row_label_bars` | 三分类标签 |
| 9 | `three_col_icon_cards` | 图标+标题+说明 |
| 10 | `three_col_numbered_card_blocks` | 编号灰卡半嵌入 |

### 四栏/四行（6种）

| # | 方法 | 适用场景 |
|---|------|----------|
| 11 | `four_col_tall_cards` | 四个高卡片（标题高度自适应） |
| 12 | `four_row_badge_bars` | 四行徽章条 |
| 13 | `four_col_ascending_steps` | 四步阶梯递进 |
| 14 | `four_col_red_base_cards` | 红底白卡+圆环 |
| 15 | `four_col_numbered_dividers` | 竖分隔线四栏 |
| 16 | `four_col_parallelogram` | 倾斜平行四边形 |

### 时间轴/流程（5种）

| # | 方法 | 适用场景 |
|---|------|----------|
| 17 | `timeline_horizontal_ascending` | 水平时间轴+箭头 |
| 18 | `timeline_icon_flow` | 圆形图标流程（红/灰交替） |
| 19 | `timeline_zigzag` | **上下交替时间线**（3-5步） |
| 20 | `process_flow_arrows` | 流程箭头 |
| 21 | `process_three_stage` | 三阶段里程碑 |

### 特殊布局（3种）

| # | 方法 | 适用场景 |
|---|------|----------|
| 22 | `triple_overlap_circles` | 三圆交叠（倒三角） |
| 23 | `diamond_quadrants` | 菱形四象限 |
| 24 | `four_panel_on_platform` | 椭圆基座四面板 |

## 矢量图标系统

279个简洁矢量图标，支持搜索、复制和变色。

### 图标调用

```python
# 搜索并放置（自动变白色）
tb.place_icon(slide, 'server', x=2.0, y=1.5, size=0.5, color='FFFFFF')

# 搜索关键词（中英文均可）
results = tb.icons.search('数据库', limit=3)
```

### 图标使用原则
- 红色/灰色圆圈上放白色图标（`color='FFFFFF'`）
- 图标占圆圈直径的 55% 最佳
- 使用 `find_circles()` 自动检测圆圈位置，确保居中
- 每页最多4个图标
- 大小 0.4-0.8"

### 分类

| 分类 | 数量 |
|------|------|
| 电脑 | 50 |
| 硬件 | 36 |
| 网络 | 32 |
| 服务器 | 25 |
| 数据库 | 20 |
| 设备 | 12 |
| 组合 | 63 |

## 制作流程

```
需求理解 → 大纲(等确认) → 生成 → QA审校(修到0) → 评分 → 发送 → 迭代
```

### 关键规则
1. **先出大纲，等用户确认再生成**
2. 相邻页布局不能重复，同一布局全篇最多2次
3. 每页 60-220 字，填充率 40-75%
4. 红色只用于标题和重点强调，交替配色用红/灰
5. 所有 body 文本必须有 `shrink=True`
6. 多行标题自动调整高度，避免文字与装饰线重叠
7. **修改模板前必须先备份原文件**
8. 所有反馈记录到 `memory/ppt-feedback.md`

## v1.1.0 更新内容
- **新增布局**: `timeline_zigzag`（上下交替时间线）
- **图标系统重建**: 279个简洁矢量图标，支持搜索/复制/变色(copy_icon color参数)
- **图标居中机制**: bounding box 居中算法，配合 find_circles 自动检测
- **边距对称修复**: 多栏布局自动水平居中
- **标题高度自适应**: 多行标题自动扩大，下方元素跟随下移
- **字体统一**: text()/multi_text() 同时设置 latin + ea 为微软雅黑
- **最小字号**: 全局 10pt（从 8pt/9pt 升级）
