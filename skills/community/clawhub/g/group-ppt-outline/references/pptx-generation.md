# 用 python-pptx 生成可打开 PPT（成功经验）

本技能**默认**在文字方案后执行本节。参考会话：电商用户分析 · 10 分钟 · 3 人 → 桌面 `.pptx` 可直接打开。

## 1. 安装（每次先确认）

```bash
python -m pip install python-pptx -q
python -c "from pptx import Presentation; from pptx.dml.color import RGBColor; print('ok')"
```

注意：`RGBColor` 正确；**不要**写 `RgbColor`（会 ImportError）。

## 2. 画布与版式

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree
import os

prs = Presentation()
prs.slide_width = Inches(13.333)   # 16:9
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]        # 空白
```

## 3. 中文字体（必做）

```python
def set_run_font(run, size=18, bold=False, color=None, name="Microsoft YaHei"):
    run.font.size = Pt(size)
    run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color
    run.font.name = name
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = etree.SubElement(rPr, qn("a:ea"))
    ea.set("typeface", name)
```

## 4. 推荐配色（非紫白风）

```python
NAVY   = RGBColor(0x1B, 0x2A, 0x4A)
TEAL   = RGBColor(0x0D, 0x94, 0x88)
ORANGE = RGBColor(0xE8, 0x6A, 0x17)
LIGHT  = RGBColor(0xF5, 0xF7, 0xFA)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
GRAY   = RGBColor(0x5A, 0x6A, 0x7A)
```

## 5. 每页结构

1. 底色（封面/致谢用 NAVY；内容页用 LIGHT）
2. 顶栏：标题 + `负责人` + `P0X / N`
3. 左侧细条或卡片区分层级
4. 正文：圆角卡片 + 短 bullet（每页 ≤5 条）
5. 页脚：主题 · 场景 · 时长
6. **备注讲稿**（必须）：

```python
slide.notes_slide.notes_text_frame.text = "【讲稿 · 约Xs · 成员X】\n1. …\n2. …"
```

## 6. 配图占位（无真实数据时）

| 需求 | 实现 |
|------|------|
| 目录 | 4 张竖向圆角卡片 |
| 分层对比 | 三根圆角矩形当柱状示意 |
| 漏斗 | 宽度递减的圆角条 + 步骤名 |
| 建议 | 左结论深色卡 + 右 3 张建议卡 |

数据一律 `〔待填〕`，不编造。

## 7. 保存（防中文路径难找）

```python
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
docs = os.path.join(os.path.expanduser("~"), "Documents")
base = desktop if os.path.isdir(desktop) else docs
zh = os.path.join(base, "主题_小组汇报.pptx")
en = os.path.join(base, "topic-slug-ppt.pptx")
prs.save(zh)
prs.save(en)   # 或 copy；方便用户搜索
print(zh)
print(en)
```

脚本可用临时 `.py` + `python script.py` 运行；Windows 下用 UTF-8 写入脚本文件。

## 8. 交付话术（固定）

- 文件路径（绝对路径）
- 打开方式：PowerPoint / WPS → **视图 → 备注**
- 提醒替换姓名、日期、〔待填〕数据
- 可选：提供改姓名/填数后的定稿

## 9. 何时不生成文件

仅当用户明确说：只要大纲、不要 pptx、只要 Markdown 目录。此时跳过本节，只出文字方案。
