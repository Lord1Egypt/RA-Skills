#!/usr/bin/env python3
"""
KDP安全内页生成器 - 符合KDP边距要求
"""

from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
import random
import math

# 6x9英寸页面
PAGE_WIDTH = 6 * inch
PAGE_HEIGHT = 9 * inch

# KDP边距要求（6x9英寸书籍）
INNER_MARGIN = 0.7 * inch   # 内侧（书脊侧）0.7英寸
OUTER_MARGIN = 0.5 * inch   # 外侧 0.5英寸
TOP_MARGIN = 0.8 * inch     # 顶部 0.8英寸
BOTTOM_MARGIN = 0.5 * inch  # 底部 0.5英寸

# 计算内容区域
CONTENT_LEFT = INNER_MARGIN
CONTENT_RIGHT = PAGE_WIDTH - OUTER_MARGIN
CONTENT_TOP = PAGE_HEIGHT - TOP_MARGIN
CONTENT_BOTTOM = BOTTOM_MARGIN
CONTENT_WIDTH = CONTENT_RIGHT - CONTENT_LEFT
CONTENT_HEIGHT = CONTENT_TOP - CONTENT_BOTTOM

COLORS = {
    "bg_white": "#FFFFFF",
    "title": "#2C3E50",
    "text": "#34495E",
    "accent": "#E74C3C",
    "line": "#BDC3C7",
    "fun_yellow": "#FFE66D",
    "fun_blue": "#4ECDC4",
    "fun_pink": "#FF6B9D",
    "fun_green": "#95E1D3",
}

class KDPSafeActivityBook:
    
    def __init__(self, title, subtitle="", age_range="4-8"):
        self.title = title
        self.subtitle = subtitle
        self.age_range = age_range
    
    def create_book(self, pages=44, output_path=None):
        if output_path is None:
            output_path = f"{self.title.replace(' ', '_')}_kdp_interior.pdf"
        
        c = canvas.Canvas(output_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
        
        print(f"🚀 生成KDP安全内页: {self.title}")
        print(f"   页面: {PAGE_WIDTH/inch}\" x {PAGE_HEIGHT/inch}\"")
        print(f"   内侧边距: {INNER_MARGIN/inch}\"")
        print(f"   外侧边距: {OUTER_MARGIN/inch}\"")
        
        page_num = 0
        
        # 1. 欢迎页（作为第一页）
        self._draw_welcome_page(c)
        c.showPage()
        page_num += 1
        
        # 2. 版权页
        self._draw_copyright_page(c)
        c.showPage()
        page_num += 1
        
        # 4. 活动页面
        activities = [
            ("maze", 8),
            ("coloring", 8),
            ("connect_dots", 8),
            ("spot_diff", 4),
            ("puzzle", 6),
            ("trace", 6),
        ]
        
        for activity_type, count in activities:
            for i in range(1, count + 1):
                if page_num >= pages:
                    break
                
                if activity_type == "maze":
                    self._draw_maze_page(c, i)
                elif activity_type == "coloring":
                    self._draw_coloring_page(c, i)
                elif activity_type == "connect_dots":
                    self._draw_connect_dots_page(c, i)
                elif activity_type == "spot_diff":
                    self._draw_spot_diff_page(c, i)
                elif activity_type == "puzzle":
                    self._draw_puzzle_page(c, i)
                elif activity_type == "trace":
                    self._draw_trace_page(c, i)
                
                c.showPage()
                page_num += 1
                print(f"   生成: {activity_type} #{i}")
        
        c.save()
        print(f"✅ 内页PDF完成: {output_path}")
        print(f"   总页数: {page_num}")
        return output_path
    
    def _draw_title_page(self, c):
        """标题页 - 严格在安全区域内"""
        # 白色背景
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        
        # 标题
        c.setFillColor(HexColor(COLORS["title"]))
        c.setFont("Helvetica-Bold", 28)
        
        words = self.title.split()
        if len(words) <= 2:
            c.drawCentredString(center_x, CONTENT_TOP - 100, self.title)
        else:
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])
            c.drawCentredString(center_x, CONTENT_TOP - 100, line1)
            c.drawCentredString(center_x, CONTENT_TOP - 150, line2)
        
        # 副标题
        if self.subtitle:
            c.setFont("Helvetica", 14)
            c.setFillColor(HexColor(COLORS["text"]))
            c.drawCentredString(center_x, CONTENT_TOP - 200, self.subtitle)
        
        # 装饰线
        c.setStrokeColor(HexColor(COLORS["accent"]))
        c.setLineWidth(2)
        line_y = CONTENT_TOP - 250
        c.line(CONTENT_LEFT + 50, line_y, CONTENT_RIGHT - 50, line_y)
        
        # 年龄标识
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(HexColor(COLORS["fun_blue"]))
        c.drawCentredString(center_x, CONTENT_BOTTOM + 100, f"Ages {self.age_range}")
    
    def _draw_welcome_page(self, c):
        """欢迎页"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        c.setFillColor(HexColor(COLORS["title"]))
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString((CONTENT_LEFT + CONTENT_RIGHT)/2, CONTENT_TOP - 50, "Welcome!")
        
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor(COLORS["text"]))
        
        text_lines = [
            "",
            "This activity book is full of fun games",
            "and puzzles just for you!",
            "",
            "Inside you'll find:",
            "  • Mazes to solve",
            "  • Pictures to color",
            "  • Dots to connect",
            "  • Differences to spot",
            "",
            "Get your crayons ready!",
        ]
        
        y = CONTENT_TOP - 100
        for line in text_lines:
            c.drawString(CONTENT_LEFT + 20, y, line)
            y -= 20
    
    def _draw_copyright_page(self, c):
        """版权页"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor(COLORS["text"]))
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        y = (CONTENT_TOP + CONTENT_BOTTOM) / 2 + 50
        
        c.drawCentredString(center_x, y, self.title)
        c.drawCentredString(center_x, y - 30, f"For ages {self.age_range}")
        c.drawCentredString(center_x, y - 60, "© 2026 All Rights Reserved")
    
    def _draw_maze_page(self, c, num):
        """迷宫页"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        
        # 标题
        c.setFillColor(HexColor(COLORS["title"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(center_x, CONTENT_TOP, f"Maze Challenge #{num}")
        
        # 说明
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor(COLORS["text"]))
        c.drawCentredString(center_x, CONTENT_TOP - 20, 
                           "Help the star find its way to the circle!")
        
        # 迷宫区域（在安全区域内）
        maze_size = min(CONTENT_WIDTH - 40, CONTENT_HEIGHT - 80)
        start_x = (CONTENT_LEFT + CONTENT_RIGHT - maze_size) / 2
        start_y = CONTENT_BOTTOM + 50
        
        cell_size = maze_size / 6
        
        # 绘制网格
        c.setStrokeColor(HexColor(COLORS["line"]))
        c.setLineWidth(1)
        
        for i in range(7):
            x = start_x + i * cell_size
            c.line(x, start_y, x, start_y + maze_size)
        
        for j in range(7):
            y = start_y + j * cell_size
            c.line(start_x, y, start_x + maze_size, y)
        
        # 外墙
        c.setStrokeColor(HexColor(COLORS["title"]))
        c.setLineWidth(2)
        c.rect(start_x, start_y, maze_size, maze_size, fill=0, stroke=1)
        
        # 起点
        c.setFillColor(HexColor(COLORS["fun_yellow"]))
        c.circle(start_x + cell_size/2, start_y + cell_size/2, cell_size/3, fill=1, stroke=0)
        
        # 终点
        c.setFillColor(HexColor(COLORS["fun_blue"]))
        c.circle(start_x + maze_size - cell_size/2, start_y + maze_size - cell_size/2, 
                cell_size/3, fill=1, stroke=0)
    
    def _draw_coloring_page(self, c, num):
        """填色页"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        
        c.setFillColor(HexColor(COLORS["title"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(center_x, CONTENT_TOP, f"Coloring Page #{num}")
        
        # 简单的可填色形状（在安全区域内居中）
        shape_size = min(CONTENT_WIDTH - 100, CONTENT_HEIGHT - 150) / 2
        shape_x = center_x
        shape_y = (CONTENT_TOP + CONTENT_BOTTOM) / 2
        
        c.setStrokeColor(HexColor(COLORS["title"]))
        c.setLineWidth(3)
        c.setFillColor(white)
        
        shapes = ["circle", "square", "triangle", "star"]
        shape = shapes[(num - 1) % len(shapes)]
        
        if shape == "circle":
            c.circle(shape_x, shape_y, shape_size, fill=0, stroke=1)
        elif shape == "square":
            c.rect(shape_x - shape_size, shape_y - shape_size, 
                  shape_size * 2, shape_size * 2, fill=0, stroke=1)
        elif shape == "triangle":
            c.drawCentredString(shape_x, shape_y, shape.upper())
        else:
            c.circle(shape_x, shape_y, shape_size, fill=0, stroke=1)
            c.drawCentredString(shape_x, shape_y - 10, shape.upper())
    
    def _draw_connect_dots_page(self, c, num):
        """连点成线"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        
        c.setFillColor(HexColor(COLORS["title"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(center_x, CONTENT_TOP, f"Connect the Dots #{num}")
        
        c.setFont("Helvetica", 10)
        c.drawCentredString(center_x, CONTENT_TOP - 20, "Start at 1 and connect the numbers!")
        
        # 点阵（在安全区域内）
        num_dots = 8 + num
        radius = min(CONTENT_WIDTH, CONTENT_HEIGHT - 100) / 2 - 50
        
        for i in range(1, num_dots + 1):
            angle = 2 * math.pi * (i - 1) / num_dots - math.pi / 2
            x = center_x + radius * math.cos(angle)
            y = (CONTENT_TOP + CONTENT_BOTTOM) / 2 + radius * math.sin(angle)
            
            c.setFillColor(HexColor(COLORS["fun_blue"]))
            c.circle(x, y, 8, fill=1, stroke=0)
            
            c.setFillColor(white)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(x, y - 3, str(i))
    
    def _draw_spot_diff_page(self, c, num):
        """找不同"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        
        c.setFillColor(HexColor(COLORS["title"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(center_x, CONTENT_TOP, f"Spot the Difference #{num}")
        
        c.setFont("Helvetica", 10)
        c.drawCentredString(center_x, CONTENT_TOP - 20, "Find 3 differences!")
        
        # 两个对比框（在安全区域内）
        box_size = (CONTENT_WIDTH - 60) / 2
        box_y = (CONTENT_TOP + CONTENT_BOTTOM) / 2 - box_size / 2
        
        c.setStrokeColor(HexColor(COLORS["line"]))
        c.setLineWidth(2)
        
        # 左框
        c.rect(CONTENT_LEFT + 20, box_y, box_size, box_size, fill=0, stroke=1)
        # 右框
        c.rect(CONTENT_RIGHT - 20 - box_size, box_y, box_size, box_size, fill=0, stroke=1)
        
        # 标注
        c.setFont("Helvetica", 10)
        c.drawCentredString(CONTENT_LEFT + 20 + box_size/2, box_y - 15, "A")
        c.drawCentredString(CONTENT_RIGHT - 20 - box_size/2, box_y - 15, "B")
    
    def _draw_puzzle_page(self, c, num):
        """谜题页"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        
        c.setFillColor(HexColor(COLORS["title"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(center_x, CONTENT_TOP, f"Fun Puzzle #{num}")
        
        puzzles = [
            ("Count the shapes!", "How many circles can you see?"),
            ("Simple addition", "3 + 4 = ___"),
            ("Pattern time", "Continue: ○ △ ○ △ ___"),
        ]
        
        puzzle = puzzles[(num - 1) % len(puzzles)]
        
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(HexColor(COLORS["accent"]))
        c.drawString(CONTENT_LEFT + 20, CONTENT_TOP - 60, puzzle[0])
        
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor(COLORS["text"]))
        c.drawString(CONTENT_LEFT + 20, CONTENT_TOP - 90, puzzle[1])
        
        # 答题线
        c.setStrokeColor(HexColor(COLORS["line"]))
        c.setLineWidth(1)
        for i in range(3):
            y = CONTENT_TOP - 140 - i * 40
            c.line(CONTENT_LEFT + 20, y, CONTENT_RIGHT - 20, y)
    
    def _draw_trace_page(self, c, num):
        """描线练习"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        
        c.setFillColor(HexColor(COLORS["title"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(center_x, CONTENT_TOP, f"Trace the Lines #{num}")
        
        c.setFont("Helvetica", 10)
        c.drawCentredString(center_x, CONTENT_TOP - 20, "Follow the dotted lines!")
        
        # 描线（在安全区域内）
        line_y_start = CONTENT_TOP - 80
        line_width = CONTENT_WIDTH - 40
        
        c.setStrokeColor(HexColor(COLORS["line"]))
        c.setLineWidth(2)
        
        for row in range(4):
            y = line_y_start - row * 60
            # 虚线
            for i in range(0, int(line_width), 10):
                x_start = CONTENT_LEFT + 20 + i
                c.line(x_start, y, x_start + 5, y)


if __name__ == "__main__":
    generator = KDPSafeActivityBook(
        title="My Fun Activity Book",
        subtitle="Mazes, Coloring, Puzzles & More!",
        age_range="4-8"
    )
    generator.create_book(pages=44)
