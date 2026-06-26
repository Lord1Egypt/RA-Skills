#!/usr/bin/env python3
"""
儿童活动书生成器 - Kids Activity Book Generator
包含：迷宫、填色页、连点成线、找不同
"""

from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random
import math

# 页面规格
PAGE_SIZE = (6 * inch, 9 * inch)  # 6x9英寸
MARGIN = 0.5 * inch
SAFE_TOP = 0.8 * inch
SAFE_BOTTOM = 0.5 * inch

# 颜色
COLORS = {
    "bg_white": "#FFFFFF",
    "bg_cream": "#FFFEF5",
    "title_dark": "#2C3E50",
    "text": "#34495E",
    "accent": "#E74C3C",
    "line": "#BDC3C7",
    "fun_pink": "#FF6B9D",
    "fun_blue": "#4ECDC4",
    "fun_yellow": "#FFE66D",
    "fun_green": "#95E1D3"
}

class KidsActivityBookGenerator:
    """儿童活动书PDF生成器"""
    
    def __init__(self, title, subtitle="", age_range="4-8"):
        self.title = title
        self.subtitle = subtitle
        self.age_range = age_range
        self.width, self.height = PAGE_SIZE
        
    def create_activity_book(self, pages=50, output_path=None):
        """创建活动书PDF"""
        if output_path is None:
            output_path = f"{self.title.replace(' ', '_')}_activity.pdf"
        
        c = canvas.Canvas(output_path, pagesize=PAGE_SIZE)
        page_num = 0
        
        print(f"🚀 生成儿童活动书: {self.title}")
        print(f"   页数: {pages}")
        
        # 1. 封面页
        self._draw_cover(c)
        c.showPage()
        page_num += 1
        
        # 2. 欢迎/说明页
        self._draw_welcome_page(c)
        c.showPage()
        page_num += 1
        
        # 3. 版权页
        self._draw_copyright_page(c)
        c.showPage()
        page_num += 1
        
        # 4. 活动页面 (循环生成不同类型)
        activities = [
            ("maze", 8),      # 8个迷宫
            ("coloring", 8),  # 8个填色页
            ("connect_dots", 8),  # 8个连点成线
            ("spot_diff", 4),  # 4个找不同
            ("puzzle", 6),    # 6个简单谜题
            ("trace", 6),     # 6个描线练习
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
                    self._draw_spot_difference_page(c, i)
                elif activity_type == "puzzle":
                    self._draw_puzzle_page(c, i)
                elif activity_type == "trace":
                    self._draw_trace_page(c, i)
                
                c.showPage()
                page_num += 1
                print(f"   已生成: {activity_type} #{i} (总页数: {page_num})")
        
        # 5. 答案页
        if page_num < pages - 1:
            self._draw_answer_page(c)
            c.showPage()
            page_num += 1
        
        c.save()
        print(f"✅ 活动书生成完成!")
        print(f"   文件: {output_path}")
        print(f"   总页数: {page_num}")
        return output_path
    
    def _set_background(self, c, color="#FFFFFF"):
        """设置背景色"""
        c.setFillColor(HexColor(color))
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
    
    def _draw_cover(self, c):
        """绘制封面"""
        self._set_background(c, COLORS["bg_cream"])
        
        # 装饰边框
        c.setStrokeColor(HexColor(COLORS["fun_pink"]))
        c.setLineWidth(4)
        c.roundRect(MARGIN, MARGIN, 
                   self.width - 2*MARGIN, self.height - 2*MARGIN,
                   20, fill=0, stroke=1)
        
        # 标题
        c.setFillColor(HexColor(COLORS["title_dark"]))
        c.setFont("Helvetica-Bold", 32)
        
        # 分行标题
        words = self.title.split()
        if len(words) <= 2:
            c.drawCentredString(self.width/2, self.height * 0.65, self.title)
        else:
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])
            c.drawCentredString(self.width/2, self.height * 0.70, line1)
            c.drawCentredString(self.width/2, self.height * 0.60, line2)
        
        # 副标题
        if self.subtitle:
            c.setFont("Helvetica", 14)
            c.setFillColor(HexColor(COLORS["text"]))
            c.drawCentredString(self.width/2, self.height * 0.50, self.subtitle)
        
        # 年龄标识
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(HexColor(COLORS["fun_blue"]))
        c.drawCentredString(self.width/2, self.height * 0.35, f"Ages {self.age_range}")
        
        # 装饰图案 - 简单的星星
        self._draw_star(c, self.width * 0.2, self.height * 0.25, 15, COLORS["fun_yellow"])
        self._draw_star(c, self.width * 0.8, self.height * 0.25, 15, COLORS["fun_yellow"])
        self._draw_star(c, self.width * 0.15, self.height * 0.75, 12, COLORS["fun_green"])
        self._draw_star(c, self.width * 0.85, self.height * 0.75, 12, COLORS["fun_green"])
    
    def _draw_star(self, c, x, y, size, color):
        """绘制星星"""
        c.setFillColor(HexColor(color))
        points = []
        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            radius = size if i % 2 == 0 else size / 2
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)
            points.append((px, py))
        
        path = c.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for px, py in points[1:]:
            path.lineTo(px, py)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
    
    def _draw_welcome_page(self, c):
        """绘制欢迎页"""
        self._set_background(c)
        
        c.setFillColor(HexColor(COLORS["title_dark"]))
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(self.width/2, self.height - SAFE_TOP - 30, "Welcome!")
        
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor(COLORS["text"]))
        
        welcome_text = [
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
            "Get your crayons and pencils ready",
            "and let's have some fun!",
        ]
        
        y = self.height - SAFE_TOP - 70
        for line in welcome_text:
            c.drawString(MARGIN + 20, y, line)
            y -= 18
        
        # 装饰
        self._draw_star(c, self.width * 0.5, self.height * 0.2, 30, COLORS["fun_pink"])
    
    def _draw_copyright_page(self, c):
        """绘制版权页"""
        self._set_background(c)
        
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor(COLORS["text"]))
        
        text = [
            f"{self.title}",
            "",
            f"For ages {self.age_range}",
            "",
            "© 2026 All Rights Reserved",
            "",
            "Have fun and learn!"
        ]
        
        y = self.height / 2 + 50
        for line in text:
            c.drawCentredString(self.width/2, y, line)
            y -= 20
    
    def _draw_maze_page(self, c, num):
        """绘制迷宫页"""
        self._set_background(c)
        
        # 标题
        c.setFillColor(HexColor(COLORS["title_dark"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.width/2, self.height - SAFE_TOP, f"Maze Challenge #{num}")
        
        # 说明
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor(COLORS["text"]))
        c.drawCentredString(self.width/2, self.height - SAFE_TOP - 20, 
                           "Help the star find its way to the circle!")
        
        # 绘制简单迷宫
        maze_size = min(self.width - 2*MARGIN, self.height * 0.6) - 0.5*inch
        start_x = (self.width - maze_size) / 2
        start_y = (self.height - maze_size) / 2 - 0.3*inch
        
        cell_size = maze_size / 8
        
        # 绘制网格
        c.setStrokeColor(HexColor(COLORS["line"]))
        c.setLineWidth(1)
        
        for i in range(9):
            x = start_x + i * cell_size
            c.line(x, start_y, x, start_y + maze_size)
        
        for j in range(9):
            y = start_y + j * cell_size
            c.line(start_x, y, start_x + maze_size, y)
        
        # 绘制迷宫墙壁 (随机移除一些边)
        c.setStrokeColor(HexColor(COLORS["title_dark"]))
        c.setLineWidth(2)
        
        # 外墙
        c.rect(start_x, start_y, maze_size, maze_size, fill=0, stroke=1)
        
        # 随机内墙
        random.seed(num * 100)  # 使用页码作为种子，确保每页不同但可重复
        walls = [
            ((1, 0), (1, 1)), ((2, 1), (2, 2)), ((3, 0), (3, 1)),
            ((0, 2), (1, 2)), ((2, 2), (2, 3)), ((4, 1), (4, 2)),
            ((1, 3), (2, 3)), ((3, 2), (3, 3)), ((5, 2), (6, 2)),
            ((2, 4), (2, 5)), ((4, 3), (4, 4)), ((6, 3), (6, 4)),
        ]
        
        for wall in walls:
            if random.random() > 0.3:  # 70%概率画墙
                (x1, y1), (x2, y2) = wall
                x_start = start_x + x1 * cell_size
                y_start = start_y + y1 * cell_size
                x_end = start_x + x2 * cell_size
                y_end = start_y + y2 * cell_size
                c.line(x_start, y_start, x_end, y_end)
        
        # 起点 (星星)
        start_center_x = start_x + cell_size / 2
        start_center_y = start_y + cell_size / 2
        self._draw_star(c, start_center_x, start_center_y, cell_size/3, COLORS["fun_yellow"])
        
        # 终点 (圆圈)
        end_center_x = start_x + maze_size - cell_size / 2
        end_center_y = start_y + maze_size - cell_size / 2
        c.setFillColor(HexColor(COLORS["fun_blue"]))
        c.circle(end_center_x, end_center_y, cell_size/3, fill=1, stroke=0)
    
    def _draw_coloring_page(self, c, num):
        """绘制填色页"""
        self._set_background(c)
        
        c.setFillColor(HexColor(COLORS["title_dark"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.width/2, self.height - SAFE_TOP, f"Coloring Page #{num}")
        
        # 绘制可填色的简单图案
        shapes = ["sun", "flower", "house", "tree", "fish", "butterfly", "car", "balloon"]
        shape = shapes[(num - 1) % len(shapes)]
        
        center_x = self.width / 2
        center_y = self.height / 2 - 0.2*inch
        size = 1.5 * inch
        
        c.setStrokeColor(HexColor(COLORS["title_dark"]))
        c.setLineWidth(3)
        c.setFillColor(white)
        
        if shape == "sun":
            # 太阳
            c.circle(center_x, center_y, size/3, fill=0, stroke=1)
            for i in range(8):
                angle = i * math.pi / 4
                x1 = center_x + (size/3 + 10) * math.cos(angle)
                y1 = center_y + (size/3 + 10) * math.sin(angle)
                x2 = center_x + (size/2) * math.cos(angle)
                y2 = center_y + (size/2) * math.sin(angle)
                c.line(x1, y1, x2, y2)
        
        elif shape == "flower":
            # 花朵
            for i in range(6):
                angle = i * math.pi / 3
                petal_x = center_x + (size/4) * math.cos(angle)
                petal_y = center_y + (size/4) * math.sin(angle)
                c.circle(petal_x, petal_y, size/8, fill=0, stroke=1)
            c.circle(center_x, center_y, size/10, fill=0, stroke=1)
        
        elif shape == "house":
            # 房子
            base_y = center_y - size/4
            # 房子主体
            c.rect(center_x - size/4, base_y, size/2, size/2, fill=0, stroke=1)
            # 屋顶 (三角形)
            roof_y = base_y + size/2
            c.line(center_x - size/3, roof_y, center_x, roof_y + size/4)
            c.line(center_x, roof_y + size/4, center_x + size/3, roof_y)
            # 门
            c.rect(center_x - size/12, base_y, size/6, size/4, fill=0, stroke=1)
        
        elif shape == "tree":
            # 树
            # 树干
            c.rect(center_x - size/12, center_y - size/2, size/6, size/3, fill=0, stroke=1)
            # 树冠 (三个圆)
            c.circle(center_x, center_y + size/4, size/4, fill=0, stroke=1)
            c.circle(center_x - size/5, center_y, size/6, fill=0, stroke=1)
            c.circle(center_x + size/5, center_y, size/6, fill=0, stroke=1)
        
        else:
            # 默认形状
            c.circle(center_x, center_y, size/3, fill=0, stroke=1)
            c.setFont("Helvetica-Bold", 20)
            c.drawCentredString(center_x, center_y - 10, shape.upper())
    
    def _draw_connect_dots_page(self, c, num):
        """绘制连点成线页"""
        self._set_background(c)
        
        c.setFillColor(HexColor(COLORS["title_dark"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.width/2, self.height - SAFE_TOP, f"Connect the Dots #{num}")
        
        c.setFont("Helvetica", 10)
        c.drawCentredString(self.width/2, self.height - SAFE_TOP - 20, 
                           "Start at 1 and connect the numbers!")
        
        # 绘制点阵 (简单的图案)
        num_dots = 10 + num  # 递增难度
        center_x = self.width / 2
        center_y = self.height / 2 - 0.2*inch
        radius = 1.2 * inch
        
        dot_positions = []
        
        # 根据页码选择不同图案
        patterns = ["circle", "star", "heart", "square"]
        pattern = patterns[(num - 1) % len(patterns)]
        
        for i in range(num_dots):
            if pattern == "circle":
                angle = 2 * math.pi * i / num_dots
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
            elif pattern == "star":
                angle = 2 * math.pi * i / num_dots - math.pi / 2
                r = radius if i % 2 == 0 else radius / 2
                x = center_x + r * math.cos(angle)
                y = center_y + r * math.sin(angle)
            elif pattern == "square":
                # 方形排列
                side = i % 4
                pos = (i // 4) / (num_dots // 4 + 1)
                if side == 0:
                    x = center_x - radius + 2 * radius * pos
                    y = center_y - radius
                elif side == 1:
                    x = center_x + radius
                    y = center_y - radius + 2 * radius * pos
                elif side == 2:
                    x = center_x + radius - 2 * radius * pos
                    y = center_y + radius
                else:
                    x = center_x - radius
                    y = center_y + radius - 2 * radius * pos
            else:
                # 默认圆形
                angle = 2 * math.pi * i / num_dots
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
            
            dot_positions.append((x, y))
        
        # 绘制点
        for i, (x, y) in enumerate(dot_positions, 1):
            # 圆点
            c.setFillColor(HexColor(COLORS["fun_blue"]))
            c.circle(x, y, 6, fill=1, stroke=0)
            
            # 数字标签
            c.setFillColor(white)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(x, y - 3, str(i))
    
    def _draw_spot_difference_page(self, c, num):
        """绘制找不同页"""
        self._set_background(c)
        
        c.setFillColor(HexColor(COLORS["title_dark"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.width/2, self.height - SAFE_TOP, f"Spot the Difference #{num}")
        
        c.setFont("Helvetica", 10)
        c.drawCentredString(self.width/2, self.height - SAFE_TOP - 20, 
                           "Find 5 differences between the two pictures!")
        
        # 绘制两个相似的图案
        box_size = 1.8 * inch
        gap = 0.3 * inch
        
        left_x = self.width/2 - box_size - gap/2
        right_x = self.width/2 + gap/2
        y_pos = self.height/2 - box_size/2 - 0.1*inch
        
        # 绘制两个框
        c.setStrokeColor(HexColor(COLORS["line"]))
        c.setLineWidth(2)
        c.rect(left_x, y_pos, box_size, box_size, fill=0, stroke=1)
        c.rect(right_x, y_pos, box_size, box_size, fill=0, stroke=1)
        
        # 绘制基础图案 (太阳、云朵等)
        self._draw_weather_scene(c, left_x + box_size/2, y_pos + box_size/2, box_size * 0.35, False)
        self._draw_weather_scene(c, right_x + box_size/2, y_pos + box_size/2, box_size * 0.35, True)
        
        # 标注
        c.setFillColor(HexColor(COLORS["text"]))
        c.setFont("Helvetica", 10)
        c.drawCentredString(left_x + box_size/2, y_pos - 15, "Picture A")
        c.drawCentredString(right_x + box_size/2, y_pos - 15, "Picture B")
    
    def _draw_weather_scene(self, c, cx, cy, size, has_differences=False):
        """绘制天气场景"""
        # 太阳
        sun_x, sun_y = cx - size/3, cy + size/3
        c.setFillColor(HexColor(COLORS["fun_yellow"]))
        c.circle(sun_x, sun_y, size/5, fill=1, stroke=0)
        
        # 云朵
        cloud_x, cloud_y = cx + size/4, cy + size/4
        c.setFillColor(HexColor("#BDC3C7"))
        c.circle(cloud_x, cloud_y, size/8, fill=1, stroke=0)
        c.circle(cloud_x + 10, cloud_y, size/10, fill=1, stroke=0)
        c.circle(cloud_x - 10, cloud_y + 5, size/12, fill=1, stroke=0)
        
        # 如果有不同，改变一些元素
        if has_differences:
            # 添加或删除某些元素
            pass  # 简化版本
    
    def _draw_puzzle_page(self, c, num):
        """绘制简单谜题页"""
        self._set_background(c)
        
        c.setFillColor(HexColor(COLORS["title_dark"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.width/2, self.height - SAFE_TOP, f"Fun Puzzle #{num}")
        
        # 简单的数学谜题或逻辑题
        puzzles = [
            ("What comes next?", "2, 4, 6, 8, ___"),
            ("Count the shapes!", "How many circles can you draw?"),
            ("Matching game", "Draw a line to match:"),
            ("Simple addition", "3 + 5 = ___"),
            ("Pattern time", "Continue the pattern: ○ △ ○ △"),
        ]
        
        puzzle = puzzles[(num - 1) % len(puzzles)]
        
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(HexColor(COLORS["accent"]))
        c.drawString(MARGIN + 20, self.height - SAFE_TOP - 50, puzzle[0])
        
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor(COLORS["text"]))
        c.drawString(MARGIN + 20, self.height - SAFE_TOP - 80, puzzle[1])
        
        # 留出答题空间
        c.setStrokeColor(HexColor(COLORS["line"]))
        c.setLineWidth(1)
        for i in range(3):
            y = self.height - SAFE_TOP - 120 - i * 40
            c.line(MARGIN + 20, y, self.width - MARGIN - 20, y)
    
    def _draw_trace_page(self, c, num):
        """绘制描线练习页"""
        self._set_background(c)
        
        c.setFillColor(HexColor(COLORS["title_dark"]))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.width/2, self.height - SAFE_TOP, f"Trace the Lines #{num}")
        
        c.setFont("Helvetica", 10)
        c.drawCentredString(self.width/2, self.height - SAFE_TOP - 20, 
                           "Follow the dotted lines with your pencil!")
        
        # 绘制不同形状的线条供描摹
        shapes = ["straight", "curved", "zigzag", "wave", "spiral"]
        shape = shapes[(num - 1) % len(shapes)]
        
        c.setStrokeColor(HexColor(COLORS["line"]))
        c.setLineWidth(2)
        
        y_start = self.height - SAFE_TOP - 60
        line_length = self.width - 2*MARGIN - 40
        
        for row in range(4):
            y = y_start - row * 50
            x_start = MARGIN + 20
            
            if shape == "straight":
                # 虚线直线
                for i in range(0, int(line_length), 10):
                    c.line(x_start + i, y, x_start + i + 5, y)
            
            elif shape == "curved":
                # 弧线
                c.arc(x_start, y - 20, x_start + line_length, y + 20, 0, 180)
            
            elif shape == "zigzag":
                # 锯齿线
                path = c.beginPath()
                path.moveTo(x_start, y)
                for i in range(10):
                    x = x_start + (i + 1) * (line_length / 10)
                    y_offset = 10 if i % 2 == 0 else -10
                    path.lineTo(x - line_length/20, y + y_offset)
                c.drawPath(path, stroke=1, fill=0)
            
            elif shape == "wave":
                # 波浪线
                path = c.beginPath()
                path.moveTo(x_start, y)
                for i in range(20):
                    x = x_start + (i + 1) * (line_length / 20)
                    y_wave = y + 10 * math.sin(i * math.pi / 2)
                    path.lineTo(x, y_wave)
                c.drawPath(path, stroke=1, fill=0)
            
            else:
                # 简单的圆圈供描摹
                for i in range(5):
                    cx = x_start + 40 + i * 70
                    c.circle(cx, y, 15, fill=0, stroke=1)
    
    def _draw_answer_page(self, c):
        """绘制答案页"""
        self._set_background(c)
        
        c.setFillColor(HexColor(COLORS["title_dark"]))
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(self.width/2, self.height - SAFE_TOP - 30, "Answers")
        
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor(COLORS["text"]))
        
        text = [
            "",
            "Thank you for playing!",
            "",
            "Did you find all the answers?",
            "Great job!",
            "",
            "Keep practicing and having fun!"
        ]
        
        y = self.height - SAFE_TOP - 80
        for line in text:
            c.drawCentredString(self.width/2, y, line)
            y -= 25


def main():
    """测试生成"""
    import sys
    
    title = "My Fun Activity Book"
    if len(sys.argv) > 1:
        title = sys.argv[1]
    
    generator = KidsActivityBookGenerator(
        title=title,
        subtitle="Mazes, Coloring, Puzzles & More!",
        age_range="4-8"
    )
    
    output_path = generator.create_activity_book(pages=50)
    print(f"\n✅ 活动书已生成: {output_path}")


if __name__ == "__main__":
    main()
