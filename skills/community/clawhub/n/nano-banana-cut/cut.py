#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
from PIL import Image

def main():
    parser = argparse.ArgumentParser(description='图片N宫格裁剪工具')
    parser.add_argument('-path', required=True, type=str, help='输入图片的完整路径')
    parser.add_argument('-num', required=True, type=int, choices=[2,4,6,9], help='宫格数量，支持2/4/6/9')
    parser.add_argument('-out', type=str, default=None, help='可选：输出目录，不填则默认保存到原图片目录')
    args = parser.parse_args()

    # 检查文件是否存在
    if not os.path.exists(args.path):
        print(f"错误：图片文件 {args.path} 不存在")
        return

    # 打开图片
    try:
        img = Image.open(args.path)
    except Exception as e:
        print(f"打开图片失败：{str(e)}")
        return

    width, height = img.size
    # 宫格配置：(行数, 列数)
    grid_map = {
        2: (1, 2),   # 1行2列 左右两格
        4: (2, 2),   # 2行2列 四宫格
        6: (2, 3),   # 2行3列 六宫格
        9: (3, 3)    # 3行3列 九宫格
    }
    rows, cols = grid_map[args.num]

    # 计算每格尺寸
    cell_width = width // cols
    cell_height = height // rows

    # 获取文件信息
    file_base, file_ext = os.path.splitext(os.path.basename(args.path))
    # 处理输出目录
    if args.out:
        # 创建输出目录如果不存在
        os.makedirs(args.out, exist_ok=True)
        save_dir = args.out
        # 指定输出目录时，文件名为 1.ext, 2.ext...
        name_format = "{}{}"
    else:
        save_dir = os.path.dirname(args.path)
        # 不指定输出目录时，保留原文件名前缀
        name_format = f"{file_base}_{{}}{{}}"

    # 裁剪并保存
    index = 1
    for r in range(rows):
        for c in range(cols):
            # 计算裁剪坐标
            left = c * cell_width
            top = r * cell_height
            right = left + cell_width
            bottom = top + cell_height

            # 裁剪
            cropped_img = img.crop((left, top, right, bottom))
            # 生成保存路径
            filename = name_format.format(index, file_ext)
            save_path = os.path.join(save_dir, filename)
            # 保存
            cropped_img.save(save_path)
            print(f"成功生成：{save_path}")
            index += 1

    print(f"\n裁剪完成，共生成 {args.num} 张图片，保存目录：{save_dir}")

if __name__ == "__main__":
    main()
