#!/usr/bin/env python3
"""
恐龙主题活动书生成器
"""

from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
import math

PAGE_WIDTH = 6 * inch
PAGE_HEIGHT = 9 * inch
INNER_MARGIN = 0.7 * inch
OUTER_MARGIN = 0.5 * inch
TOP_MARGIN = 0.8 * inch
BOTTOM_MARGIN = 0.5 * inch

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
    "dino_green": "#7CB342",
    "dino_orange": "#FF8F00",
    "dino_blue": "#42A5F5",
    "dino_purple": "#AB47BC",
    "line": "#BDC3C7",
}

class DinosaurActivityBook:
    
    def __init__(self):
        pass
    
    def create_book(self, output_path="dinosaur_activity_book.pdf"):
        c = canvas.Canvas(output_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
        
        print("🦕 生成恐龙主题活动书...")
        
        page_num = 0
        
        # 直接从恐龙迷宫开始，没有封面页
        for i in range(1, 9):
            self._draw_dino_maze(c, i)
            c.showPage()
            page_num += 1
        
        # 4. 恐龙填色 (8个)
        dino_types = ["T-Rex", "Triceratops", "Stegosaurus", "Velociraptor",
                     "Brachiosaurus", "Pterodactyl", "Ankylosaurus", "Spinosaurus"]
        for i, dino in enumerate(dino_types, 1):
            self._draw_dino_coloring(c, i, dino)
            c.showPage()
            page_num += 1
        
        # 5. 恐龙连点 (8个)
        for i in range(1, 9):
            self._draw_dino_connect_dots(c, i)
            c.showPage()
            page_num += 1
        
        # 6. 恐龙找不同 (4个)
        for i in range(1, 5):
            self._draw_dino_spot_diff(c, i)
            c.showPage()
            page_num += 1
        
        # 7. 恐龙谜题 (6个)
        for i in range(1, 7):
            self._draw_dino_puzzle(c, i)
            c.showPage()
            page_num += 1
        
        # 8. 恐龙描线 (6个)
        for i in range(1, 7):
            self._draw_dino_trace(c, i)
            c.showPage()
            page_num += 1
        
        c.save()
        print(f"✅ 恐龙活动书完成: {output_path}")
        print(f"   总页数: {page_num}")
        return output_path
    
    def _draw_welcome_page(self, c):
        """欢迎页"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        
        c.setFillColor(HexColor(COLORS["dino_green"]))
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(center_x, CONTENT_TOP - 50, "ROAR! Welcome!")
        
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor(COLORS["text"]))
        
        lines = [
            "",
            "Get ready for a dino-mite adventure!",
            "",
            "Inside you'll find:",
            "  🦖 Dinosaur Mazes",
            "  🎨 Dino Coloring Pages",
            "  🔢 Connect-the-Dots",
            "  👀 Spot the Difference",
            "  🧩 Dino Puzzles",
            "  ✏️ Tracing Fun",
            "",
            "Grab your crayons and let's go!",
        ]
        
        y = CONTENT_TOP - 120
        for line in lines:
            c.drawCentredString(center_x, y, line)
            y -= 22
    
    def _draw_copyright_page(self, c):
        """版权页"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        y = (CONTENT_TOP + CONTENT_BOTTOM) / 2 + 50
        
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor(COLORS["text"]))
        c.drawCentredString(center_x, y, "Dinosaur Adventure Activity Book")
        c.drawCentredString(center_x, y - 30, "For ages 4-8")
        c.drawCentredString(center_x, y - 60, "© 2026 All Rights Reserved")
        c.drawCentredString(center_x, y - 90, "🦕 Have a roaring good time! 🦕")
    
    def _draw_dino_maze(self, c, num):
        """恐龙迷宫"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        
        c.setFillColor(HexColor(COLORS["dino_green"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(center_x, CONTENT_TOP, f"🦖 Dino Maze #{num}")
        
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor(COLORS["text"]))
        c.drawCentredString(center_x, CONTENT_TOP - 25, "Help the baby dino find its mom!")
        
        # 迷宫
        maze_size = min(CONTENT_WIDTH - 60, CONTENT_HEIGHT - 100)
        start_x = (CONTENT_LEFT + CONTENT_RIGHT - maze_size) / 2
        start_y = CONTENT_BOTTOM + 60
        
        cell = maze_size / 5
        
        c.setStrokeColor(HexColor(COLORS["line"]))
        for i in range(6):
            x = start_x + i * cell
            c.line(x, start_y, x, start_y + maze_size)
        for j in range(6):
            y = start_y + j * cell
            c.line(start_x, y, start_x + maze_size, y)
        
        c.setStrokeColor(HexColor(COLORS["dino_orange"]))
        c.setLineWidth(3)
        c.rect(start_x, start_y, maze_size, maze_size, fill=0, stroke=1)
        
        # 起点 - 小恐龙
        c.setFillColor(HexColor(COLORS["dino_green"]))
        c.circle(start_x + cell/2, start_y + cell/2, cell/2.5, fill=1, stroke=0)
        
        # 终点 - 大恐龙/蛋
        c.setFillColor(HexColor(COLORS["dino_orange"]))
        c.circle(start_x + maze_size - cell/2, start_y + maze_size - cell/2, cell/2.5, fill=1, stroke=0)
    
    def _draw_dino_coloring(self, c, num, dino_name):
        """恐龙填色"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        
        c.setFillColor(HexColor(COLORS["dino_green"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(center_x, CONTENT_TOP, f"🎨 Color the {dino_name}")
        
        # 简化的恐龙轮廓（圆形组合）
        shape_y = (CONTENT_TOP + CONTENT_BOTTOM) / 2
        
        c.setStrokeColor(HexColor(COLORS["dino_green"]))
        c.setLineWidth(4)
        c.setFillColor(white)
        
        # 身体
        c.circle(center_x, shape_y, 80, fill=0, stroke=1)
        # 头
        c.circle(center_x + 70, shape_y + 40, 50, fill=0, stroke=1)
        # 尾巴
        c.line(center_x - 80, shape_y, center_x - 140, shape_y - 30)
        c.line(center_x - 80, shape_y, center_x - 140, shape_y + 30)
        # 腿
        for dx in [-40, 0, 40]:
            c.line(center_x + dx, shape_y - 80, center_x + dx, shape_y - 130)
        
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor(COLORS["text"]))
        c.drawCentredString(center_x, CONTENT_BOTTOM + 30, f"This is a {dino_name}")
    
    def _draw_dino_connect_dots(self, c, num):
        """恐龙连点"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        
        c.setFillColor(HexColor(COLORS["dino_blue"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(center_x, CONTENT_TOP, f"🔢 Dino Dots #{num}")
        
        c.setFont("Helvetica", 10)
        c.drawCentredString(center_x, CONTENT_TOP - 25, "Connect to reveal a dinosaur!")
        
        # 恐龙形状的点阵
        num_dots = 10 + num
        points = [
            (0, 60), (30, 80), (60, 70), (80, 50), (90, 20),  # 背部
            (80, -10), (60, -30), (30, -40), (0, -35), (-30, -20),  # 腹部
            (-50, -10), (-60, 20), (-50, 50), (-20, 60),  # 尾巴
        ]
        
        scale = 2.5
        offset_y = (CONTENT_TOP + CONTENT_BOTTOM) / 2
        
        for i, (px, py) in enumerate(points[:num_dots], 1):
            x = center_x + px * scale
            y = offset_y + py * scale
            
            c.setFillColor(HexColor(COLORS["dino_green"]))
            c.circle(x, y, 8, fill=1, stroke=0)
            
            c.setFillColor(white)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(x, y - 3, str(i))
    
    def _draw_dino_spot_diff(self, c, num):
        """恐龙找不同"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        
        c.setFillColor(HexColor(COLORS["dino_purple"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(center_x, CONTENT_TOP, f"👀 Dino Differences #{num}")
        
        c.setFont("Helvetica", 10)
        c.drawCentredString(center_x, CONTENT_TOP - 25, "Find 3 differences between the dinos!")
        
        # 两个恐龙对比框
        box_size = (CONTENT_WIDTH - 60) / 2
        box_y = (CONTENT_TOP + CONTENT_BOTTOM) / 2 - box_size / 2
        
        c.setStrokeColor(HexColor(COLORS["line"]))
        c.setLineWidth(2)
        
        # 左框
        c.rect(CONTENT_LEFT + 20, box_y, box_size, box_size, fill=0, stroke=1)
        # 简化的恐龙
        c.setStrokeColor(HexColor(COLORS["dino_green"]))
        c.circle(CONTENT_LEFT + 20 + box_size/2, box_y + box_size/2 + 30, 40, fill=0, stroke=1)
        c.circle(CONTENT_LEFT + 20 + box_size/2 + 30, box_y + box_size/2 + 50, 25, fill=0, stroke=1)
        
        # 右框
        c.setStrokeColor(HexColor(COLORS["line"]))
        c.rect(CONTENT_RIGHT - 20 - box_size, box_y, box_size, box_size, fill=0, stroke=1)
        c.setStrokeColor(HexColor(COLORS["dino_green"]))
        c.circle(CONTENT_RIGHT - 20 - box_size/2, box_y + box_size/2 + 30, 40, fill=0, stroke=1)
        c.circle(CONTENT_RIGHT - 20 - box_size/2 + 30, box_y + box_size/2 + 50, 25, fill=0, stroke=1)
        
        c.setFont("Helvetica", 10)
        c.drawCentredString(CONTENT_LEFT + 20 + box_size/2, box_y - 20, "A")
        c.drawCentredString(CONTENT_RIGHT - 20 - box_size/2, box_y - 20, "B")
    
    def _draw_dino_puzzle(self, c, num):
        """恐龙谜题"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        
        c.setFillColor(HexColor(COLORS["dino_orange"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(center_x, CONTENT_TOP, f"🧩 Dino Puzzle #{num}")
        
        puzzles = [
            ("Count the spikes!", "How many spikes does Stegosaurus have?"),
            ("T-Rex Math", "If a T-Rex has 2 arms and 2 legs, how many limbs total?"),
            ("Dino Pattern", "Continue: 🦕 🦖 🦕 🦖 ___"),
            ("Long Neck", "Who has a longer neck: Brachiosaurus or T-Rex?"),
            ("Dino Eggs", "A dino laid 3 eggs, then 2 more. How many total?"),
            ("Herbivore or Carnivore?", "Does T-Rex eat plants or meat?"),
        ]
        
        puzzle = puzzles[(num - 1) % len(puzzles)]
        
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(HexColor(COLORS["dino_green"]))
        c.drawString(CONTENT_LEFT + 20, CONTENT_TOP - 70, puzzle[0])
        
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor(COLORS["text"]))
        c.drawString(CONTENT_LEFT + 20, CONTENT_TOP - 100, puzzle[1])
        
        # 答题线
        c.setStrokeColor(HexColor(COLORS["line"]))
        for i in range(3):
            y = CONTENT_TOP - 160 - i * 50
            c.line(CONTENT_LEFT + 20, y, CONTENT_RIGHT - 20, y)
    
    def _draw_dino_trace(self, c, num):
        """恐龙描线"""
        c.setFillColor(HexColor(COLORS["bg_white"]))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        center_x = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        
        c.setFillColor(HexColor(COLORS["dino_blue"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(center_x, CONTENT_TOP, f"✏️ Trace the Dino #{num}")
        
        c.setFont("Helvetica", 10)
        c.drawCentredString(center_x, CONTENT_TOP - 25, "Follow the dotted lines!")
        
        # 恐龙形状的虚线
        c.setStrokeColor(HexColor(COLORS["line"]))
        c.setLineWidth(2)
        
        # 简化的恐龙轮廓 - 虚线
        base_y = (CONTENT_TOP + CONTENT_BOTTOM) / 2
        
        # 身体轮廓（虚线椭圆）
        for angle in range(0, 360, 10):
            rad = math.radians(angle)
            x = center_x + 60 * math.cos(rad)
            y = base_y + 40 * math.sin(rad)
            if angle % 20 == 0:
                c.circle(x, y, 2, fill=1, stroke=0)
        
        # 头
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            x = center_x + 90 + 30 * math.cos(rad)
            y = base_y + 50 + 25 * math.sin(rad)
            if angle % 30 == 0:
                c.circle(x, y, 2, fill=1, stroke=0)


if __name__ == "__main__":
    book = DinosaurActivityBook()
    book.create_book()
