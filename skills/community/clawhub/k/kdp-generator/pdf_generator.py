#!/usr/bin/env python3
"""
KDP PDF Interior Generator - 内页PDF生成器
生成符合KDP规格的日记/计划本内页PDF
"""

from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from typing import List, Dict, Tuple
import os

# 页面规格配置
PAGE_SIZES = {
    "6x9": (6 * inch, 9 * inch),
    "8.5x11": (8.5 * inch, 11 * inch),
    "A5": (148 * inch / 25.4, 210 * inch / 25.4)  # A5 in inches
}

# 颜色配置
COLORS = {
    "cream": "#FFFEF5",
    "white": "#FFFFFF",
    "dark_text": "#2C3E50",
    "medium_text": "#34495E",
    "light_text": "#7F8C8D",
    "accent": "#E74C3C",
    "line": "#BDC3C7"
}

class InteriorPDFGenerator:
    """KDP内页PDF生成器"""
    
    def __init__(self, title: str, subtitle: str, page_size: str = "6x9", 
                 paper_color: str = "cream", author: str = "Luna & Boss"):
        self.title = title
        self.subtitle = subtitle
        self.page_size = page_size
        self.paper_color = paper_color
        self.author = author
        
        self.width, self.height = PAGE_SIZES.get(page_size, PAGE_SIZES["6x9"])
        # KDP安全边距：内页边距（书脊侧）需要更大
        self.inner_margin = 0.7 * inch   # 书脊侧边距（更大）
        self.outer_margin = 0.5 * inch   # 外侧边距
        self.top_safe = 0.85 * inch      # 顶部安全区域
        self.bottom_margin = 0.5 * inch  # 底部边距
        self.content_width = self.width - self.inner_margin - self.outer_margin
        
    def create_guided_journal(self, days: int = 90, output_path: str = None) -> str:
        """创建引导日记PDF"""
        if output_path is None:
            output_path = f"{self.title.replace(' ', '_')}_interior.pdf"
        
        c = canvas.Canvas(output_path, pagesize=(self.width, self.height))
        page_count = 0
        
        # 1. 标题页
        self._draw_title_page(c)
        c.showPage()
        page_count += 1
        
        # 2. 版权页
        self._draw_copyright_page(c)
        c.showPage()
        page_count += 1
        
        # 3. 前言/欢迎页
        self._draw_welcome_page(c)
        c.showPage()
        page_count += 1
        
        # 4. 目标设定页 (2页)
        for _ in range(2):
            self._draw_goal_setting_page(c)
            c.showPage()
            page_count += 1
        
        # 5. 每日日志页
        print(f"   生成{days}天每日日志...")
        for day in range(1, days + 1):
            self._draw_daily_page(c, day)
            c.showPage()
            page_count += 1
            if day % 30 == 0:
                print(f"     已完成 {day}/{days} 天")
        
        # 6. 周复盘页 (12周)
        print(f"   生成12周复盘页...")
        for week in range(1, 13):
            self._draw_weekly_review_page(c, week)
            c.showPage()
            page_count += 1
        
        # 7. 月度总结页
        self._draw_monthly_summary_page(c)
        c.showPage()
        page_count += 1
        
        c.save()
        print(f"✅ PDF生成完成: {output_path}")
        print(f"   总页数: {page_count}")
        return output_path
    
    def _set_background(self, c):
        """设置页面背景色"""
        color = COLORS.get(self.paper_color, COLORS["cream"])
        c.setFillColor(HexColor(color))
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
    
    def _draw_title_page(self, c):
        """绘制标题页"""
        self._set_background(c)
        
        # 主标题 - 从顶部留出足够空间
        c.setFillColor(HexColor(COLORS["dark_text"]))
        c.setFont("Helvetica-Bold", 28)
        
        # 分行显示标题
        words = self.title.split()
        mid = len(words) // 2
        line1 = " ".join(words[:mid]) if mid > 0 else words[0]
        line2 = " ".join(words[mid:]) if mid > 0 else ""
        
        # 从顶部安全区域开始（28pt字体约28像素高）
        y_start = self.height - self.top_safe - 40
        c.drawCentredString(self.width/2, y_start, line1)
        if line2:
            c.drawCentredString(self.width/2, y_start - 45, line2)
        
        # 副标题
        c.setFont("Helvetica", 14)
        c.setFillColor(HexColor(COLORS["medium_text"]))
        c.drawCentredString(self.width/2, y_start - 90, self.subtitle)
        
        # 装饰线
        c.setStrokeColor(HexColor(COLORS["accent"]))
        c.setLineWidth(2)
        c.line(self.width*0.3, y_start - 125, self.width*0.7, y_start - 125)
        
        # 版权信息
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor(COLORS["light_text"]))
        c.drawCentredString(self.width/2, self.inner_margin + 20, f"© 2026 {self.author}")
    
    def _draw_copyright_page(self, c):
        """绘制版权页"""
        self._set_background(c)
        
        c.setFillColor(HexColor(COLORS["medium_text"]))
        c.setFont("Helvetica", 9)
        
        lines = [
            self.title,
            self.subtitle,
            "",
            "No part of this publication may be reproduced, distributed, or transmitted",
            "in any form or by any means without the prior written permission of the publisher.",
            "",
            "First Edition: 2026",
            "",
            "Published via Amazon KDP",
            "",
            "For personal use only."
        ]
        
        # 从顶部安全区域开始
        y = self.height - self.top_safe - 30
        for line in lines:
            c.drawCentredString(self.width/2, y, line)
            y -= 16
    
    def _draw_welcome_page(self, c):
        """绘制欢迎/前言页"""
        self._set_background(c)
        
        c.setFillColor(HexColor(COLORS["dark_text"]))
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(self.width/2, self.height - self.top_safe - 35, "Welcome")
        
        # 分隔线
        c.setStrokeColor(HexColor(COLORS["accent"]))
        c.setLineWidth(1.5)
        c.line(self.inner_margin, self.height - self.top_safe - 60, self.width - self.outer_margin, self.height - self.top_safe - 60)
        
        c.setFont("Helvetica", 11)
        c.setFillColor(HexColor(COLORS["medium_text"]))
        
        welcome_text = """Welcome to your 90-day entrepreneurial journey.

This journal is designed to help you build consistent habits,
track your progress, and maintain clarity as you grow your business.

Each day, you'll reflect on your priorities, celebrate your wins,
and plan for tomorrow. Over 90 days, these small daily actions
will compound into significant results.

Your business success starts with consistency.
Let's begin."""
        
        y = self.height - self.top_safe - 85
        for line in welcome_text.split('\n'):
            c.drawString(self.inner_margin, y, line)
            y -= 16
    
    def _draw_goal_setting_page(self, c):
        """绘制目标设定页"""
        self._set_background(c)
        
        c.setFillColor(HexColor(COLORS["dark_text"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.width/2, self.height - self.top_safe - 30, "My 90-Day Goals")
        
        # 分隔线
        c.setStrokeColor(HexColor(COLORS["accent"]))
        c.setLineWidth(1)
        c.line(self.inner_margin, self.height - self.top_safe - 55, self.width - self.outer_margin, self.height - self.top_safe - 55)
        
        goals = [
            ("Business Goal:", self.height - self.top_safe - 85),
            ("Revenue Target:", self.height - self.top_safe - 175),
            ("Personal Growth:", self.height - self.top_safe - 265),
        ]
        
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(HexColor(COLORS["medium_text"]))
        
        for label, y_pos in goals:
            c.drawString(self.inner_margin, y_pos, label)
            # 下划线
            c.setStrokeColor(HexColor(COLORS["line"]))
            c.line(self.inner_margin + 120, y_pos + 3, self.width - self.outer_margin, y_pos + 3)
            c.line(self.inner_margin, y_pos - 30, self.width - self.outer_margin, y_pos - 30)
            c.line(self.inner_margin, y_pos - 60, self.width - self.outer_margin, y_pos - 60)
            c.setStrokeColor(HexColor(COLORS["accent"]))
    
    def _draw_daily_page(self, c, day_num: int):
        """绘制每日日志页"""
        self._set_background(c)
        
        # 日期和天数标题 - 从顶部安全区域开始
        c.setFillColor(HexColor(COLORS["dark_text"]))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(self.inner_margin, self.height - self.top_safe - 25, f"Day {day_num}")
        
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor(COLORS["light_text"]))
        c.drawString(self.width - self.outer_margin - 100, self.height - self.top_safe - 25, "Date: _________")
        
        # 分隔线
        c.setStrokeColor(HexColor(COLORS["accent"]))
        c.setLineWidth(1.5)
        c.line(self.inner_margin, self.height - self.top_safe - 50, self.width - self.outer_margin, self.height - self.top_safe - 50)
        
        # 引导问题
        prompts = [
            "What are the 3 most important things today?",
            "What progress did I make?",
            "What will I improve tomorrow?",
            "Today's insight:"
        ]
        
        y_start = self.height - self.top_safe - 75
        line_spacing = 55
        
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(HexColor(COLORS["medium_text"]))
        
        for i, prompt in enumerate(prompts):
            y = y_start - i * line_spacing
            c.drawString(self.inner_margin, y, prompt)
            
            # 书写区域（下划线）
            c.setStrokeColor(HexColor(COLORS["line"]))
            for j in range(3):
                line_y = y - 20 - j * 18
                c.line(self.inner_margin, line_y, self.width - self.outer_margin, line_y)
    
    def _draw_weekly_review_page(self, c, week_num: int):
        """绘制周复盘页"""
        self._set_background(c)
        
        c.setFillColor(HexColor(COLORS["dark_text"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.width/2, self.height - self.top_safe - 30, f"Week {week_num} Review")
        
        # 分隔线
        c.setStrokeColor(HexColor(COLORS["accent"]))
        c.line(self.inner_margin, self.height - self.top_safe - 55, self.width - self.outer_margin, self.height - self.top_safe - 55)
        
        questions = [
            "Biggest win this week:",
            "What worked well?",
            "What needs improvement?",
            "Key lesson learned:",
            "Focus for next week:"
        ]
        
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(HexColor(COLORS["medium_text"]))
        
        y = self.height - self.top_safe - 85
        for question in questions:
            c.drawString(self.inner_margin, y, question)
            # 书写线
            c.setStrokeColor(HexColor(COLORS["line"]))
            for j in range(2):
                c.line(self.inner_margin + 20, y - 20 - j * 20, 
                       self.width - self.outer_margin, y - 20 - j * 20)
            y -= 75
    
    def _draw_monthly_summary_page(self, c):
        """绘制月度总结页"""
        self._set_background(c)
        
        c.setFillColor(HexColor(COLORS["dark_text"]))
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(self.width/2, self.height - self.top_safe - 30, "Monthly Summary")
        
        # 分隔线
        c.setStrokeColor(HexColor(COLORS["accent"]))
        c.setLineWidth(1.5)
        c.line(self.inner_margin, self.height - self.top_safe - 55, self.width - self.outer_margin, self.height - self.top_safe - 55)
        
        sections = [
            "Goals Achieved:",
            "Revenue/Metrics:",
            "Challenges Faced:",
            "Growth Areas:",
            "Goals for Next Month:"
        ]
        
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(HexColor(COLORS["medium_text"]))
        
        y = self.height - self.top_safe - 85
        for section in sections:
            c.drawString(self.inner_margin, y, section)
            # 书写线
            c.setStrokeColor(HexColor(COLORS["line"]))
            for j in range(2):
                c.line(self.inner_margin, y - 22 - j * 20, self.width - self.outer_margin, y - 22 - j * 20)
            y -= 75


# ============ 其他类型生成器 ============

class DailyPlannerGenerator(InteriorPDFGenerator):
    """每日计划本生成器"""
    
    def create_planner(self, days: int = 90, output_path: str = None) -> str:
        """创建计划本PDF"""
        if output_path is None:
            output_path = f"{self.title.replace(' ', '_')}_planner.pdf"
        
        c = canvas.Canvas(output_path, pagesize=(self.width, self.height))
        page_count = 0
        
        # 标题页
        self._draw_title_page(c)
        c.showPage()
        page_count += 1
        
        # 年度计划页
        for _ in range(12):
            self._draw_monthly_overview_page(c)
            c.showPage()
            page_count += 1
        
        # 每日计划页
        for day in range(1, days + 1):
            self._draw_daily_planner_page(c, day)
            c.showPage()
            page_count += 1
        
        c.save()
        return output_path
    
    def _draw_monthly_overview_page(self, c):
        """绘制月度概览页"""
        self._set_background(c)
        c.setFillColor(HexColor(COLORS["dark_text"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.width/2, self.height - self.outer_margin - 30, "Monthly Overview")
    
    def _draw_daily_planner_page(self, c, day_num: int):
        """绘制每日计划页"""
        self._set_background(c)
        
        c.setFillColor(HexColor(COLORS["dark_text"]))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(self.inner_margin, self.height - self.outer_margin - 20, f"Day {day_num}")
        
        # 计划区域
        sections = ["Top Priorities", "Schedule", "Tasks", "Notes"]
        y = self.height - self.outer_margin - 50
        
        c.setFont("Helvetica-Bold", 11)
        for section in sections:
            c.drawString(self.inner_margin, y, section)
            c.setStrokeColor(HexColor(COLORS["line"]))
            c.line(self.inner_margin, y - 5, self.width - self.outer_margin, y - 5)
            y -= 60


class GratitudeJournalGenerator(InteriorPDFGenerator):
    """感恩日记生成器"""
    
    def create_gratitude_journal(self, days: int = 90, output_path: str = None) -> str:
        """创建感恩日记PDF"""
        if output_path is None:
            output_path = f"{self.title.replace(' ', '_')}_gratitude.pdf"
        
        c = canvas.Canvas(output_path, pagesize=(self.width, self.height))
        page_count = 0
        
        # 标题页
        self._draw_title_page(c)
        c.showPage()
        page_count += 1
        
        # 每日感恩页
        for day in range(1, days + 1):
            self._draw_gratitude_page(c, day)
            c.showPage()
            page_count += 1
        
        c.save()
        return output_path
    
    def _draw_gratitude_page(self, c, day_num: int):
        """绘制感恩页"""
        self._set_background(c)
        
        c.setFillColor(HexColor(COLORS["dark_text"]))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(self.inner_margin, self.height - self.outer_margin - 20, f"Day {day_num}")
        
        prompts = [
            "3 things I'm grateful for today:",
            "The best moment of today was:",
            "I want to thank:",
            "Tomorrow I look forward to:"
        ]
        
        y = self.height - self.outer_margin - 50
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(HexColor(COLORS["medium_text"]))
        
        for prompt in prompts:
            c.drawString(self.inner_margin, y, prompt)
            c.setStrokeColor(HexColor(COLORS["line"]))
            for j in range(2):
                c.line(self.inner_margin, y - 15 - j * 15, self.width - self.outer_margin, y - 15 - j * 15)
            y -= 60


# ============ 导出函数 ============

def generate_interior_pdf(title: str, subtitle: str, book_type: str = "guided_journal",
                          days: int = 90, output_dir: str = "./output") -> str:
    """
    生成内页PDF的便捷函数
    
    Args:
        title: 书名
        subtitle: 副标题
        book_type: 书籍类型 (guided_journal/daily_planner/gratitude_journal)
        days: 天数
        output_dir: 输出目录
    
    Returns:
        生成的PDF文件路径
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{title.replace(' ', '_')}_interior.pdf")
    
    print(f"🚀 开始生成内页PDF...")
    print(f"   书名: {title}")
    print(f"   类型: {book_type}")
    print(f"   天数: {days}")
    
    if book_type == "guided_journal":
        generator = InteriorPDFGenerator(title, subtitle)
        generator.create_guided_journal(days, output_path)
    elif book_type == "daily_planner":
        generator = DailyPlannerGenerator(title, subtitle)
        generator.create_planner(days, output_path)
    elif book_type == "gratitude_journal":
        generator = GratitudeJournalGenerator(title, subtitle)
        generator.create_gratitude_journal(days, output_path)
    else:
        raise ValueError(f"不支持的书籍类型: {book_type}")
    
    return output_path


if __name__ == "__main__":
    # 测试生成
    generate_interior_pdf(
        title="Test Journal",
        subtitle="A 90-Day Guided Workbook",
        book_type="guided_journal",
        days=90
    )
