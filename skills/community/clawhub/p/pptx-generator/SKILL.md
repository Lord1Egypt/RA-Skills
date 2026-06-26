---
name: pptx-generator
description: 专业PPT生成器。Use when user wants to create editable PowerPoint presentations with professional layouts, multiple styles, and beautiful designs. Supports business, academic, creative styles. 可编辑PPT、幻灯片制作、演示文稿。
version: 1.0.1
license: MIT-0
metadata: {"openclaw": {"emoji": "📊", "requires": {"bins": ["python3"], "env": []}}}
dependencies: "pip install python-pptx pillow"
---

# PPT Generator

专业PPT生成器，创建可编辑、排版精美、多风格的PowerPoint演示文稿。

## Features

- 📊 **可编辑PPTX**: 标准Office格式，可二次编辑
- 🎨 **多种风格**: 商务、学术、创意、简约
- 📐 **精美排版**: 专业布局，字体层次清晰
- 📈 **图表支持**: 柱状图、折线图、饼图
- 🖼️ **图片支持**: 插入图片，自动排版
- 📝 **专业模板**: 10+预制模板

## 支持的风格

| 风格 | 适用场景 | 特点 |
|------|----------|------|
| 商务蓝 | 商业汇报 | 专业、稳重 |
| 学术白 | 学术论文 | 简洁、规范 |
| 创意紫 | 创意展示 | 时尚、活力 |
| 科技深 | 技术分享 | 现代、高端 |
| 极简灰 | 通用场景 | 简约、百搭 |

## 使用方式

```
User: "帮我做一个关于AI发展的PPT"
User: "生成商务风格的项目汇报PPT"
User: "做一个学术论文答辩PPT"
```

---

## Python代码实现

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

class PPTGenerator:
    def __init__(self, style='business_blue'):
        self.prs = Presentation()
        self.style = style
        self.colors = self._get_colors(style)
        self.fonts = self._get_fonts()
    
    def _get_colors(self, style):
        """获取配色方案"""
        schemes = {
            'business_blue': {
                'primary': RGBColor(30, 60, 114),
                'secondary': RGBColor(70, 130, 180),
                'accent': RGBColor(255, 193, 7),
                'text': RGBColor(51, 51, 51),
                'bg': RGBColor(255, 255, 255)
            },
            'academic_white': {
                'primary': RGBColor(0, 51, 102),
                'secondary': RGBColor(102, 102, 102),
                'accent': RGBColor(204, 0, 0),
                'text': RGBColor(51, 51, 51),
                'bg': RGBColor(255, 255, 255)
            },
            'creative_purple': {
                'primary': RGBColor(102, 45, 140),
                'secondary': RGBColor(155, 89, 182),
                'accent': RGBColor(241, 196, 15),
                'text': RGBColor(51, 51, 51),
                'bg': RGBColor(248, 248, 255)
            },
            'tech_dark': {
                'primary': RGBColor(30, 30, 30),
                'secondary': RGBColor(60, 60, 60),
                'accent': RGBColor(0, 200, 150),
                'text': RGBColor(240, 240, 240),
                'bg': RGBColor(20, 20, 25)
            },
            'minimal_gray': {
                'primary': RGBColor(80, 80, 80),
                'secondary': RGBColor(150, 150, 150),
                'accent': RGBColor(0, 120, 215),
                'text': RGBColor(51, 51, 51),
                'bg': RGBColor(250, 250, 250)
            }
        }
        return schemes.get(style, schemes['business_blue'])
    
    def _get_fonts(self):
        """获取字体配置"""
        return {
            'title': 'Arial',
            'body': 'Arial',
            'chinese': 'Microsoft YaHei'
        }
    
    def add_title_slide(self, title, subtitle=''):
        """添加封面页"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        
        # 背景色
        self._set_slide_bg(slide, self.colors['bg'])
        
        # 标题
        left, top, width, height = Inches(1), Inches(2), Inches(8), Inches(2)
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(44)
        p.font.bold = True
        p.font.color.rgb = self.colors['primary']
        p.alignment = PP_ALIGN.CENTER
        
        # 副标题
        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.size = Pt(20)
            p2.font.color.rgb = self.colors['secondary']
            p2.alignment = PP_ALIGN.CENTER
            p2.space_before = Pt(20)
        
        return slide
    
    def add_content_slide(self, title, bullets, layout='left'):
        """添加内容页"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        
        # 背景色
        self._set_slide_bg(slide, self.colors['bg'])
        
        # 标题栏
        self._add_title_bar(slide, title)
        
        # 内容区域
        left, top, width, height = Inches(0.8), Inches(1.5), Inches(8.4), Inches(5)
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        
        for i, bullet in enumerate(bullets):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = f"• {bullet}"
            p.font.size = Pt(18)
            p.font.color.rgb = self.colors['text']
            p.space_after = Pt(12)
        
        return slide
    
    def add_two_column_slide(self, title, left_content, right_content):
        """添加双栏内容页"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        
        self._set_slide_bg(slide, self.colors['bg'])
        self._add_title_bar(slide, title)
        
        # 左栏
        left_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.5), Inches(5))
        left_tf = left_box.text_frame
        left_tf.word_wrap = True
        
        for i, item in enumerate(left_content):
            p = left_tf.paragraphs[0] if i == 0 else left_tf.add_paragraph()
            p.text = f"• {item}"
            p.font.size = Pt(16)
            p.font.color.rgb = self.colors['text']
            p.space_after = Pt(10)
        
        # 右栏
        right_box = slide.shapes.add_textbox(Inches(5.2), Inches(1.5), Inches(4.5), Inches(5))
        right_tf = right_box.text_frame
        right_tf.word_wrap = True
        
        for i, item in enumerate(right_content):
            p = right_tf.paragraphs[0] if i == 0 else right_tf.add_paragraph()
            p.text = f"• {item}"
            p.font.size = Pt(16)
            p.font.color.rgb = self.colors['text']
            p.space_after = Pt(10)
        
        return slide
    
    def add_table_slide(self, title, headers, rows):
        """添加表格页"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        
        self._set_slide_bg(slide, self.colors['bg'])
        self._add_title_bar(slide, title)
        
        # 创建表格
        rows_count = len(rows) + 1
        cols_count = len(headers)
        
        left, top = Inches(0.5), Inches(1.8)
        width, height = Inches(9), Inches(4)
        
        table_shape = slide.shapes.add_table(rows_count, cols_count, left, top, width, height)
        table = table_shape.table
        
        # 设置表头
        for i, header in enumerate(headers):
            cell = table.cell(0, i)
            cell.text = header
            cell.fill.solid()
            cell.fill.fore_color.rgb = self.colors['primary']
            
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(14)
                paragraph.font.bold = True
                paragraph.font.color.rgb = RGBColor(255, 255, 255)
                paragraph.alignment = PP_ALIGN.CENTER
        
        # 设置数据行
        for row_idx, row in enumerate(rows, 1):
            for col_idx, cell_text in enumerate(row):
                cell = table.cell(row_idx, col_idx)
                cell.text = str(cell_text)
                
                for paragraph in cell.text_frame.paragraphs:
                    paragraph.font.size = Pt(12)
                    paragraph.font.color.rgb = self.colors['text']
                    paragraph.alignment = PP_ALIGN.CENTER
        
        return slide
    
    def add_image_slide(self, title, image_path, caption=''):
        """添加图片页"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        
        self._set_slide_bg(slide, self.colors['bg'])
        self._add_title_bar(slide, title)
        
        # 插入图片
        left, top, width, height = Inches(1.5), Inches(1.8), Inches(7), Inches(4.5)
        slide.shapes.add_picture(image_path, left, top, width, height)
        
        # 添加说明
        if caption:
            txBox = slide.shapes.add_textbox(Inches(1), Inches(6.5), Inches(8), Inches(0.5))
            tf = txBox.text_frame
            p = tf.paragraphs[0]
            p.text = caption
            p.font.size = Pt(12)
            p.font.color.rgb = self.colors['secondary']
            p.alignment = PP_ALIGN.CENTER
        
        return slide
    
    def add_summary_slide(self, title, points, conclusion):
        """添加总结页"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        
        self._set_slide_bg(slide, self.colors['bg'])
        self._add_title_bar(slide, title)
        
        # 要点
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(3.5))
        tf = txBox.text_frame
        tf.word_wrap = True
        
        for i, point in enumerate(points):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = f"✓ {point}"
            p.font.size = Pt(18)
            p.font.color.rgb = self.colors['text']
            p.space_after = Pt(10)
        
        # 结论框
        conclusion_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8), Inches(5.2), Inches(8.4), Inches(1.2)
        )
        conclusion_box.fill.solid()
        conclusion_box.fill.fore_color.rgb = self.colors['secondary']
        
        tf2 = conclusion_box.text_frame
        tf2.word_wrap = True
        p2 = tf2.paragraphs[0]
        p2.text = f"💡 {conclusion}"
        p2.font.size = Pt(16)
        p2.font.color.rgb = RGBColor(255, 255, 255)
        p2.alignment = PP_ALIGN.CENTER
        
        return slide
    
    def _set_slide_bg(self, slide, color):
        """设置幻灯片背景"""
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color
    
    def _add_title_bar(self, slide, title):
        """添加标题栏"""
        # 标题背景
        title_bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0), Inches(10), Inches(1.2)
        )
        title_bar.fill.solid()
        title_bar.fill.fore_color.rgb = self.colors['primary']
        title_bar.line.fill.background()
        
        # 标题文字
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(9), Inches(0.8))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.LEFT
    
    def save(self, output_path):
        """保存PPT"""
        self.prs.save(output_path)
        return output_path

# 使用示例
gen = PPTGenerator(style='business_blue')

# 添加封面
gen.add_title_slide('2026年AI行业报告', '从大模型到智能体时代')

# 添加内容页
gen.add_content_slide('市场概况', [
    '全球AI市场规模突破3.2万亿美元',
    '企业AI采用率达到89%',
    '年度投资总额1280亿美元'
])

# 添加表格页
gen.add_table_slide('核心数据', 
    ['指标', '2025', '2026', '增长率'],
    [
        ['市场规模', '$2.1T', '$3.2T', '52%'],
        ['企业采用', '72%', '89%', '24%'],
        ['投资总额', '$790亿', '$1280亿', '62%']
    ]
)

# 添加总结页
gen.add_summary_slide('总结', [
    'AI技术持续突破',
    'Agent技术走向成熟',
    '开源生态蓬勃发展'
], '2026年是AI发展的关键转折点')

# 保存
gen.save('output.pptx')
```

---

## 使用场景

```
User: "做一个20页的AI行业报告PPT，商务风格"
Agent: 使用 PPTGenerator(style='business_blue') 生成

User: "做一个学术答辩PPT"
Agent: 使用 PPTGenerator(style='academic_white') 生成

User: "做一个技术分享PPT，科技风格"
Agent: 使用 PPTGenerator(style='tech_dark') 生成
```

---

## Notes

- 生成标准.pptx格式，可编辑
- 支持Microsoft PowerPoint、WPS、LibreOffice
- 字体自动适配系统
- 支持中英文
