---
name: marketing-plan
description: Marketing plan generator with web research and Word output. Use when user needs to create marketing plans, promotional campaigns, social media strategies. Fetches latest market data via web search. Generates Word documents. 营销方案、推广计划、营销策划。
version: 1.0.2
license: MIT-0
metadata: {"openclaw": {"emoji": "📈", "requires": {"bins": ["python3"], "env": []}}}
dependencies: "pip install python-docx"
---

# Marketing Plan Generator

Professional marketing plan generator with web research and Word document output.

## Features

- 📋 **Marketing Plans**: Complete strategy documents
- 📢 **Campaign Plans**: Multi-channel strategies
- 🌐 **Web Research**: Fetch latest market data
- 📄 **Word Output**: Generate .docx files
- 🎯 **Target Analysis**: Audience segmentation
- 📊 **Budget Planning**: ROI-focused allocation

## How It Works

```
User request
    ↓
1. Web Search: Fetch latest market data
    ↓
2. AI Analysis: Generate strategy
    ↓
3. Python Code: Create Word document
    ↓
Output: Professional .docx file
```

## Step 1: Understand Requirements

```
User provides:
- Product/service name
- Target audience
- Budget
- Timeline
- Goals
```

## Step 2: Research Market Data

Agent searches for:
- Competitor information
- Market trends
- Industry benchmarks
- Best practices

## Step 3: Generate Word Document

```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime

class MarketingPlanGenerator:
    def __init__(self, product, company, budget):
        self.product = product
        self.company = company
        self.budget = budget
        self.channels = []
        self.timeline = []
        self.goals = []
        self.competitors = []
    
    def add_channel(self, name, budget_pct, description):
        self.channels.append({
            'name': name,
            'budget': self.budget * budget_pct / 100,
            'budget_pct': budget_pct,
            'description': description
        })
    
    def add_milestone(self, date, task, owner):
        self.timeline.append({'date': date, 'task': task, 'owner': owner})
    
    def add_goal(self, metric, target):
        self.goals.append({'metric': metric, 'target': target})
    
    def add_competitor(self, name, strengths, weaknesses):
        self.competitors.append({
            'name': name,
            'strengths': strengths,
            'weaknesses': weaknesses
        })
    
    def generate_docx(self, output_path, lang='en'):
        """Generate professional Word document with excellent formatting"""
        doc = Document()
        
        # Set page margins
        section = doc.sections[0]
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)
        
        # Title
        if lang == 'zh':
            title = doc.add_heading('营销推广方案', 0)
        else:
            title = doc.add_heading('Marketing Plan', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Subtitle
        if lang == 'zh':
            sub = doc.add_heading(f'{self.product}', 1)
        else:
            sub = doc.add_heading(f'{self.product}', 1)
        sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Date and company
        info = doc.add_paragraph()
        info.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = info.add_run(f'{self.company} | {datetime.now().strftime("%Y-%m-%d")}')
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(100, 100, 100)
        
        doc.add_paragraph()
        
        # 1. Executive Summary
        if lang == 'zh':
            doc.add_heading('一、项目概述', level=1)
            doc.add_paragraph(f'产品名称：{self.product}')
            doc.add_paragraph(f'所属公司：{self.company}')
            doc.add_paragraph(f'推广预算：¥{self.budget:,}')
            doc.add_paragraph(f'推广周期：8周')
        else:
            doc.add_heading('1. Executive Summary', level=1)
            doc.add_paragraph(f'Product: {self.product}')
            doc.add_paragraph(f'Company: {self.company}')
            doc.add_paragraph(f'Budget: ${self.budget:,}')
            doc.add_paragraph(f'Duration: 8 weeks')
        
        # 2. Budget Allocation
        if lang == 'zh':
            doc.add_heading('二、预算分配', level=1)
        else:
            doc.add_heading('2. Budget Allocation', level=1)
        
        table = doc.add_table(rows=len(self.channels)+1, cols=3)
        table.style = 'Table Grid'
        table.cell(0, 0).text = '渠道' if lang == 'zh' else 'Channel'
        table.cell(0, 1).text = '预算' if lang == 'zh' else 'Budget'
        table.cell(0, 2).text = '说明' if lang == 'zh' else 'Description'
        
        for i, ch in enumerate(self.channels, 1):
            table.cell(i, 0).text = ch['name']
            table.cell(i, 1).text = f"¥{ch['budget']:,.0f}" if lang == 'zh' else f"${ch['budget']:,.0f}"
            table.cell(i, 2).text = ch['description']
        
        doc.add_paragraph()
        
        # 3. Timeline
        if lang == 'zh':
            doc.add_heading('三、执行计划', level=1)
        else:
            doc.add_heading('3. Timeline', level=1)
        
        for m in self.timeline:
            doc.add_paragraph(f"{m['date']}: {m['task']}（{m['owner']}）")
        
        # 4. Goals
        if lang == 'zh':
            doc.add_heading('四、目标指标', level=1)
        else:
            doc.add_heading('4. Goals', level=1)
        
        for g in self.goals:
            doc.add_paragraph(f"{g['metric']}: {g['target']}")
        
        doc.save(output_path)
        return output_path

# Example
plan = MarketingPlanGenerator('Product X', 'Company Y', 10000)
plan.add_channel('Social Media', 40, 'WeChat, Xiaohongshu')
plan.add_milestone('Week 1', 'Launch campaign', 'Marketing')
plan.add_goal('Impressions', '1M')
plan.generate_docx('marketing_plan.docx')
```

## Usage Examples

```
User: "Create marketing plan for AI product, budget $50k"
Agent: 
1. Search for AI market trends
2. Generate plan with channels and timeline
3. Create Word document
4. Output: marketing_plan.docx

User: "帮我做一个产品推广方案，预算5万"
Agent:
1. 搜索相关市场数据
2. 生成营销方案
3. 创建Word文档
4. 输出：营销方案.docx
```

## Notes

- Fetches latest market data via web search
- Generates professional Word documents
- Supports Chinese and English
- Budget-focused approach

