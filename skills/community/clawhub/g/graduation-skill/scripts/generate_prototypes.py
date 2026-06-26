# -*- coding: utf-8 -*-
"""
毕业设计PDF原型图生成器
用法: python generate_prototypes.py
"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体
pdfmetrics.registerFont(TTFont('STXIHEI', r'C:\Windows\Fonts\STXIHEI.TTF'))

# 学术风格配色
C_PRIMARY = colors.HexColor('#9B2335')    # 深红
C_SECONDARY = colors.HexColor('#C5963A') # 金褐
C_TEXT = colors.HexColor('#2D1F14')      # 深褐
C_BG = colors.HexColor('#FBF7F0')        # 暖白
C_BORDER = colors.HexColor('#E0D5C5')    # 浅棕

class PrototypeGenerator:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def draw_phone_frame(self, c, x, y, w, h):
        """绘制手机外框"""
        c.setFillColor(colors.HexColor('#ccc7c0'))
        c.roundRect(x-5, y-5, w+10, h+10, 12, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setStrokeColor(C_BORDER)
        c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
    
    def add_title(self, c, fig_num, title):
        """添加图标题"""
        c.setFont('STXIHEI', 14)
        c.setFillColor(C_TEXT)
        c.drawCentredString(105*mm, 280*mm, f'图{fig_num} {title}')
    
    def generate_mobile_prototype(self, fig_num, title, draw_func):
        """生成移动端原型图"""
        output_path = self.output_dir / f'图{fig_num}_{title}.pdf'
        c = canvas.Canvas(str(output_path), pagesize=A4)
        
        # 页面背景
        c.setFillColor(C_BG)
        c.rect(0, 0, 210*mm, 297*mm, fill=1, stroke=0)
        
        # 绘制手机外框
        phone_w, phone_h = 90*mm, 160*mm
        phone_x = (210*mm - phone_w) / 2
        phone_y = 50*mm
        self.draw_phone_frame(c, phone_x, phone_y, phone_w, phone_h)
        
        # 绘制内容
        draw_func(c, phone_x, phone_y, phone_w, phone_h)
        
        # 添加标题
        self.add_title(c, fig_num, title)
        
        c.save()
        print(f'✅ 生成: {output_path.name}')
        return output_path

def main():
    """生成示例原型图"""
    gen = PrototypeGenerator('docs')
    
    # 示例：启动页
    def draw_launch(c, x, y, w, h):
        # 背景色
        c.setFillColor(C_PRIMARY)
        c.rect(x, y, w, h, fill=1, stroke=0)
        # Logo文字
        c.setFillColor(colors.white)
        c.setFont('STXIHEI', 24)
        c.drawCentredString(x + w/2, y + h/2, 'APP')
    
    gen.generate_mobile_prototype('4-1', '启动页原型图', draw_launch)
    print('\n原型图生成完成！')

if __name__ == '__main__':
    main()
