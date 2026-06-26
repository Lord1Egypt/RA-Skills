#!/usr/bin/env python3
"""
保险方案报告生成器
将客户KYC信息和保障方案生成为PDF报告
"""

import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
except ImportError:
    print("Error: reportlab not installed. Run: pip install reportlab")
    sys.exit(1)

# 注册中文字体（使用系统常见字体）
def register_chinese_fonts():
    font_paths = [
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/PingFang.ttc",  # macOS
        "C:/Windows/Fonts/simhei.ttf",  # Windows
        "C:/Windows/Fonts/simsun.ttc",
    ]
    
    for font_path in font_paths:
        if Path(font_path).exists():
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                return 'ChineseFont'
            except:
                continue
    
    # 如果都找不到，使用默认字体
    return 'Helvetica'

def create_styles(font_name):
    styles = getSampleStyleSheet()
    
    # 标题样式
    styles.add(ParagraphStyle(
        name='CustomTitle',
        fontName=font_name,
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=30,
        leading=24
    ))
    
    # 章节标题
    styles.add(ParagraphStyle(
        name='SectionTitle',
        fontName=font_name,
        fontSize=14,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=12,
        spaceBefore=20,
        leading=18
    ))
    
    # 子标题
    styles.add(ParagraphStyle(
        name='SubTitle',
        fontName=font_name,
        fontSize=12,
        textColor=colors.HexColor('#333333'),
        spaceAfter=8,
        spaceBefore=12,
        leading=16
    ))
    
    # 正文（覆盖默认样式）
    if 'BodyText' in styles:
        styles['BodyText'].fontName = font_name
        styles['BodyText'].fontSize = 10
        styles['BodyText'].alignment = TA_LEFT
        styles['BodyText'].spaceAfter = 6
        styles['BodyText'].leading = 14
    else:
        styles.add(ParagraphStyle(
            name='BodyText',
            fontName=font_name,
            fontSize=10,
            alignment=TA_LEFT,
            spaceAfter=6,
            leading=14
        ))
    
    # 高亮文本
    styles.add(ParagraphStyle(
        name='Highlight',
        fontName=font_name,
        fontSize=10,
        textColor=colors.HexColor('#d9534f'),
        spaceAfter=6,
        leading=14
    ))
    
    return styles

def generate_report(data: dict, output_path: str):
    """生成PDF报告"""
    
    font_name = register_chinese_fonts()
    styles = create_styles(font_name)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    story = []
    
    # 封面
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("健康保险方案建议书", styles['CustomTitle']))
    story.append(Spacer(1, 1*cm))
    
    # 客户信息摘要
    customer = data.get('customer', {})
    story.append(Paragraph(f"客户姓名：{customer.get('name', '未填写')}", styles['BodyText']))
    story.append(Paragraph(f"生成日期：{datetime.now().strftime('%Y年%m月%d日')}", styles['BodyText']))
    story.append(PageBreak())
    
    # 一、客户基本信息
    story.append(Paragraph("一、客户基本信息", styles['SectionTitle']))
    
    basic_info = [
        ['项目', '内容'],
        ['姓名', customer.get('name', '-')],
        ['性别', customer.get('gender', '-')],
        ['年龄', f"{customer.get('age', '-')}岁"],
        ['职业', customer.get('occupation', '-')],
        ['婚姻状况', customer.get('marital_status', '-')],
        ['家庭结构', customer.get('family_structure', '-')],
    ]
    
    t = Table(basic_info, colWidths=[4*cm, 10*cm])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    
    # 二、健康状况评估
    story.append(Paragraph("二、健康状况评估", styles['SectionTitle']))
    
    health = data.get('health', {})
    health_info = [
        ['项目', '内容'],
        ['身高/体重', f"{health.get('height', '-')}cm / {health.get('weight', '-')}kg"],
        ['BMI指数', health.get('bmi', '-')],
        ['吸烟史', health.get('smoking', '-')],
        ['既往病史', health.get('medical_history', '无')],
        ['家族病史', health.get('family_history', '无')],
        ['近期体检异常', health.get('checkup_issues', '无')],
    ]
    
    t = Table(health_info, colWidths=[4*cm, 10*cm])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    
    # 三、财务状况分析
    story.append(Paragraph("三、财务状况分析", styles['SectionTitle']))
    
    finance = data.get('finance', {})
    finance_info = [
        ['项目', '内容'],
        ['年收入', f"{finance.get('annual_income', '-')}万元"],
        ['现有负债', f"{finance.get('debt', '-')}万元"],
        ['现有保障', finance.get('existing_insurance', '无')],
        ['保险预算', f"{finance.get('budget', '-')}万元/年"],
    ]
    
    t = Table(finance_info, colWidths=[4*cm, 10*cm])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    
    # 四、风险评估与保障缺口
    story.append(Paragraph("四、风险评估与保障缺口分析", styles['SectionTitle']))
    
    risk = data.get('risk_analysis', {})
    story.append(Paragraph("4.1 风险识别", styles['SubTitle']))
    story.append(Paragraph(f"• 疾病风险等级：{risk.get('disease_risk', '中等')}", styles['BodyText']))
    story.append(Paragraph(f"• 意外风险等级：{risk.get('accident_risk', '中等')}", styles['BodyText']))
    story.append(Paragraph(f"• 收入损失风险：{risk.get('income_risk', '中等')}", styles['BodyText']))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("4.2 保障缺口计算", styles['SubTitle']))
    gaps = data.get('coverage_gaps', {})
    
    gap_data = [
        ['保障类型', '建议保额', '缺口分析'],
        ['重大疾病', f"{gaps.get('critical_illness_suggested', '-')}万", gaps.get('critical_illness_gap', '-')],
        ['医疗费用', f"{gaps.get('medical_suggested', '-')}万", gaps.get('medical_gap', '-')],
        ['意外身故', f"{gaps.get('accident_suggested', '-')}万", gaps.get('accident_gap', '-')],
        ['寿险保障', f"{gaps.get('life_suggested', '-')}万", gaps.get('life_gap', '-')],
    ]
    
    t = Table(gap_data, colWidths=[3*cm, 3*cm, 8*cm])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d9534f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff5f5')]),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    
    # 五、保险方案建议
    story.append(Paragraph("五、保险方案建议", styles['SectionTitle']))
    
    recommendation = data.get('recommendation', {})
    story.append(Paragraph("5.1 配置策略", styles['SubTitle']))
    story.append(Paragraph(recommendation.get('strategy', '根据客户实际情况，建议采用基础保障+重疾保障的组合方案。'), styles['BodyText']))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("5.2 产品类型推荐", styles['SubTitle']))
    products = recommendation.get('products', [])
    for i, prod in enumerate(products, 1):
        story.append(Paragraph(f"{i}. {prod.get('type', '')} - {prod.get('description', '')}", styles['BodyText']))
        story.append(Paragraph(f"   建议保额：{prod.get('coverage', '-')}，预估保费：{prod.get('premium', '-')}", styles['BodyText']))
        story.append(Spacer(1, 0.2*cm))
    
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("5.3 预算分配建议", styles['SubTitle']))
    story.append(Paragraph(recommendation.get('budget_allocation', '建议将预算的60%用于重疾险，30%用于医疗险，10%用于意外险。'), styles['BodyText']))
    
    # 六、重要提示
    story.append(PageBreak())
    story.append(Paragraph("六、重要提示", styles['SectionTitle']))
    
    notices = data.get('notices', [
        "1. 本方案基于客户提供的资料进行分析，如有信息变更请及时告知。",
        "2. 投保时请如实进行健康告知，避免影响后续理赔。",
        "3. 具体产品选择需结合市场在售产品及核保结果确定。",
        "4. 建议每年进行一次保单检视，根据家庭变化调整保障方案。",
    ])
    
    for notice in notices:
        story.append(Paragraph(notice, styles['BodyText']))
        story.append(Spacer(1, 0.2*cm))
    
    # 生成PDF
    doc.build(story)
    print(f"报告已生成: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 generate_report.py <input_json> <output_pdf>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    generate_report(data, output_file)
