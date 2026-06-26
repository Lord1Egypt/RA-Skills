"""
复杂形状PNG生成脚本
用于将PPT中无法直接还原的复杂形状（渐变填充/透明/自定义路径/custGeom）
绘制为精确的透明背景PNG，再嵌入PPT。

使用方法：
  python complex_shape.py --output OUTPUT.png --width 1200 --height 280 \
      --gradient-stops "0.0:#FFFFFF,1.0:#C00000" --gradient-angle 270 \
      --polygon "0.498,0.0 1.0,0.25 1.0,1.0 0.0,1.0 0.0,0.25"

依赖：pip install Pillow numpy
"""

import argparse
import sys
from PIL import Image, ImageDraw
import numpy as np
from typing import List, Tuple, Optional


def lerp_color(c1: Tuple[int, int, int], c2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    """线性插值两个颜色"""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """将十六进制颜色字符串转为RGB元组"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def gradient_color(y_ratio: float, stops: List[Tuple[float, Tuple[int, int, int]]]) -> Tuple[int, int, int]:
    """根据y比例在渐变停止点列表中插值颜色"""
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        if p0 <= y_ratio <= p1:
            t = (y_ratio - p0) / (p1 - p0)
            return lerp_color(c0, c1, t)
    return stops[-1][1]


def cubic_bezier(p0: Tuple[float, float], p1: Tuple[float, float],
                 p2: Tuple[float, float], p3: Tuple[float, float],
                 steps: int = 50) -> List[Tuple[float, float]]:
    """三次贝塞尔曲线采样，返回曲线上均匀分布的采样点"""
    points = []
    for i in range(steps + 1):
        t = i / steps
        x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
        y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
        points.append((x, y))
    return points


def parse_gradient_stops(stops_str: str) -> List[Tuple[float, Tuple[int, int, int]]]:
    """解析渐变停止点字符串，如 "0.0:#FFFFFF,1.0:#C00000" """
    stops = []
    for part in stops_str.split(','):
        pos_str, color_str = part.strip().split(':')
        stops.append((float(pos_str), hex_to_rgb(color_str.strip())))
    return stops


def parse_polygon(points_str: str) -> List[Tuple[float, float]]:
    """解析多边形顶点字符串，如 "0.5,0.0 1.0,0.25 1.0,1.0" """
    points = []
    for pair in points_str.split():
        x_str, y_str = pair.split(',')
        points.append((float(x_str), float(y_str)))
    return points


def draw_gradient_polygon(
    output_path: str,
    width: int,
    height: int,
    gradient_stops: List[Tuple[float, Tuple[int, int, int]]],
    polygon_points: List[Tuple[float, float]],
    bezier_paths: Optional[List[List[Tuple[float, float]]]] = None
) -> None:
    """
    绘制带渐变填充的多边形PNG（透明背景）

    Args:
        output_path: 输出PNG路径
        width, height: 画布尺寸（像素）
        gradient_stops: 渐变停止点列表，格式 [(pos, (r,g,b)), ...]，pos为0.0~1.0
        polygon_points: 多边形归一化顶点，格式 [(nx,ny), ...]
        bezier_paths: 可选的贝塞尔曲线采样点列表，用于复杂路径
    """
    # 创建透明画布
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = img.load()

    # 构建多边形蒙版
    mask = Image.new("L", (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    poly_pixels = [(int(x * width), int(y * height)) for x, y in polygon_points]
    mask_draw.polygon(poly_pixels, fill=255)

    mask_pixels = mask.load()

    # 如果有贝塞尔路径，合并到多边形中
    all_shape_pixels = set(poly_pixels)
    if bezier_paths:
        for path in bezier_paths:
            for x, y in path:
                all_shape_pixels.add((int(x * width), int(y * height)))

    # 逐行扫描，填充渐变色（y轴渐变从上到下）
    for row in range(height):
        y_ratio = row / height
        color = gradient_color(y_ratio, gradient_stops)
        alpha = 255

        for col in range(width):
            # 简单多边形边界检测：只填充蒙版非零区域
            if mask_pixels[col, row] > 0:
                pixels[col, row] = (*color, alpha)

    img.save(output_path, "PNG")
    print(f"已生成: {output_path} ({width}x{height})")


def main():
    parser = argparse.ArgumentParser(description="复杂形状PNG生成工具（用于PPT复杂形状降级）")
    parser.add_argument("--output", "-o", required=True, help="输出PNG路径")
    parser.add_argument("--width", type=int, default=1200, help="画布宽度（像素）")
    parser.add_argument("--height", type=int, default=280, help="画布高度（像素）")
    parser.add_argument("--gradient-stops", required=True,
                        help="渐变停止点，格式: pos0:color0,pos1:color1,... 如 0.0:#FFFFFF,1.0:#C00000")
    parser.add_argument("--polygon",
                        help="多边形顶点归一化坐标，格式: x0,y0 x1,y1 ... 如 0.498,0.0 1.0,0.25")
    parser.add_argument("--bezier", action="append",
                        help="贝塞尔曲线控制点，格式: x0,y0 x1,y1 x2,y2 x3,y3，可多次指定多条曲线")

    args = parser.parse_args()

    # 解析参数
    gradient_stops = parse_gradient_stops(args.gradient_stops)
    polygon_points = parse_polygon(args.polygon) if args.polygon else None

    bezier_paths = None
    if args.bezier:
        bezier_paths = []
        for curve_str in args.bezier:
            pts = []
            for pair in curve_str.split():
                x, y = pair.split(',')
                pts.append((float(x), float(y)))
            # 贝塞尔曲线需要4个控制点
            if len(pts) >= 4:
                sampled = cubic_bezier(pts[0], pts[1], pts[2], pts[3])
                bezier_paths.append(sampled)

    if polygon_points:
        draw_gradient_polygon(
            args.output, args.width, args.height,
            gradient_stops, polygon_points, bezier_paths
        )
    else:
        print("错误: 必须指定 --polygon 多边形顶点")
        sys.exit(1)


if __name__ == "__main__":
    main()
