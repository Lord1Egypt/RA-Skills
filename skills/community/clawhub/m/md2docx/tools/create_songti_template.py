#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""创建宋体模板"""

from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

# 创建新文档
doc = Document()

# 设置默认字体为宋体
style = doc.styles['Normal']
font = style.font
font.name = '宋体'
font.size = Pt(12)
style._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 设置标题样式
for i in range(1, 4):
    heading_style = doc.styles[f'Heading {i}']
    heading_font = heading_style.font
    heading_font.name = '黑体'
    heading_style._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    if i == 1:
        heading_font.size = Pt(16)
    elif i == 2:
        heading_font.size = Pt(14)
    else:
        heading_font.size = Pt(12)

# 保存模板
doc.save('C:/Users/GWF/.openclaw/workspace/skills/md2docx/tools/songti-template.docx')
print("宋体模板已创建: songti-template.docx")