<!-- FINGERPRINT: cd4d561cdde841cb -->
# Word 版式导出指引（GB/T 9704-2012）

成稿后如需导出为标准公文版式 Word 文档，按以下规范操作。

## 一、优先路径：用 AI 平台自带的文档生成能力

WorkBuddy / 腾讯 skill 等平台若支持生成 Word（.docx），直接要求按以下版式参数生成：

| 要素 | 参数 |
|------|------|
| 页面 | A4，上3.7cm 下3.5cm 左2.8cm 右2.6cm |
| 标题 | 方正小标宋（或小标宋_GBK）二号，居中 |
| 一级标题（一、） | 黑体 三号 |
| 二级标题（（一）） | 楷体_GB2312 三号加粗 |
| 正文 | 仿宋_GB2312 三号 |
| 行距 | 28磅固定值 |
| 段落 | 首行缩进2字符 |
| 发文字号/数字 | Times New Roman 三号 |
| 成文日期 | 右空四字，阿拉伯数字 |

## 二、备用路径：无 docx 能力时（Markdown → Word 手工设置）

1. AI 输出 Markdown 成稿（标题用 # 表示，正文段落用 ### 层级）
2. 复制到 Word 后按上表设置：页面 → 页边距；全选 → 字体仿宋_GB2312 三号、行距28磅固定；标题行单独设方正小标宋二号居中；一级标题设黑体三号；首行缩进2字符
3. 数字、金额统一 Times New Roman

## 三、脚本路径：本地 python-docx 生成（可选）

有 Python 环境的用户可用以下脚本：

```python
# 安装：pip install python-docx
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

doc = Document()
# 页面设置
sec = doc.sections[0]
sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
sec.top_margin, sec.bottom_margin = Cm(3.7), Cm(3.5)
sec.left_margin, sec.right_margin = Cm(2.8), Cm(2.6)

def set_font(p, name, size, bold=False):
    p.style.font.name = name
    p.style.font.size = Pt(size)
    p.style.font.bold = bold
    p.style.element.rPr.rFonts.set(qn('w:eastAsia'), name)

# 标题
p = doc.add_paragraph('关于××××的请示')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_font(p, '方正小标宋_GBK', 22)  # 二号=22pt

# 正文
for text in ['一、缘由段落……', '二、事项段落……']:
    p = doc.add_paragraph(text)
    p.paragraph_format.first_line_indent = Pt(32)  # 首行缩进2字符(16pt×2)
    p.paragraph_format.line_spacing = Pt(28)       # 28磅固定
    set_font(p, '仿宋_GB2312', 16)                 # 三号=16pt

doc.save('公文.docx')
```

## 四、注意

- 方正小标宋、仿宋_GB2312、楷体_GB2312 为公文字体，系统没有时显示会替换为默认字体——可先从本单位OA或字体网站获取安装
- 导出后检查：标题是否居中、正文是否首行缩进、行距是否28磅、数字是否为Times New Roman
