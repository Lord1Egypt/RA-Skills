#!/usr/bin/env python3
"""
p-skill 综合使用示例
演示所有功能的使用方法
"""

import os
from PIL import Image
from p_skill import (
    load_image, save_image,
    resize_image, crop_image, convert_format,
    adjust_brightness, adjust_contrast, adjust_sharpness, smart_enhance,
    grayscale, sepia, blur, contour, invert, pixelate,
    stitch_horizontal, stitch_vertical, stitch_grid,
    remove_background_simple, remove_background_color,
    add_text
)


def create_sample_images():
    """创建示例图片用于演示"""
    print("创建示例图片...")
    
    # 创建简单的彩色测试图片
    img1 = Image.new('RGB', (200, 200), color='red')
    img2 = Image.new('RGB', (200, 200), color='green')
    img3 = Image.new('RGB', (200, 200), color='blue')
    img4 = Image.new('RGB', (200, 200), color='yellow')
    
    # 创建白色背景的测试图片（用于背景移除演示）
    img_white_bg = Image.new('RGB', (300, 300), color='white')
    draw = ImageDraw.Draw(img_white_bg)
    draw.ellipse([50, 50, 250, 250], fill='blue')
    
    # 保存示例图片
    os.makedirs('output', exist_ok=True)
    save_image(img1, 'output/sample_red.jpg')
    save_image(img2, 'output/sample_green.jpg')
    save_image(img3, 'output/sample_blue.jpg')
    save_image(img4, 'output/sample_yellow.jpg')
    save_image(img_white_bg, 'output/sample_white_bg.jpg')
    
    return img1, img2, img3, img4, img_white_bg


def demo_core_functions():
    """演示核心功能"""
    print("\n=== 核心功能演示 ===")
    
    # 创建测试图片
    test_img = Image.new('RGB', (400, 300), color='lightblue')
    draw = ImageDraw.Draw(test_img)
    draw.rectangle([50, 50, 350, 250], fill='orange')
    draw.text((100, 140), "Test Image", fill='black')
    
    save_image(test_img, 'output/core_original.jpg')
    
    # 调整尺寸
    resized = resize_image(test_img, scale=0.5)
    save_image(resized, 'output/core_resized.jpg')
    print("✓ 调整尺寸完成")
    
    # 裁剪
    cropped = crop_image(test_img, (50, 50, 350, 250))
    save_image(cropped, 'output/core_cropped.jpg')
    print("✓ 裁剪完成")
    
    # 格式转换
    converted_png = convert_format(test_img, 'PNG')
    save_image(converted_png, 'output/core_converted.png')
    print("✓ 格式转换完成")


def demo_enhance_functions():
    """演示增强功能"""
    print("\n=== 增强功能演示 ===")
    
    # 创建测试图片
    test_img = Image.new('RGB', (400, 300), color='gray')
    draw = ImageDraw.Draw(test_img)
    draw.rectangle([100, 100, 300, 200], fill='darkgray')
    
    # 亮度调整
    bright = adjust_brightness(test_img, 1.5)
    save_image(bright, 'output/enhance_bright.jpg')
    print("✓ 亮度调整完成")
    
    # 对比度调整
    contrast = adjust_contrast(test_img, 1.5)
    save_image(contrast, 'output/enhance_contrast.jpg')
    print("✓ 对比度调整完成")
    
    # 清晰度调整
    sharp = adjust_sharpness(test_img, 2.0)
    save_image(sharp, 'output/enhance_sharp.jpg')
    print("✓ 清晰度调整完成")
    
    # 智能增强
    enhanced = smart_enhance(test_img)
    save_image(enhanced, 'output/enhance_smart.jpg')
    print("✓ 智能增强完成")


def demo_filters():
    """演示滤镜功能"""
    print("\n=== 滤镜功能演示 ===")
    
    # 创建彩色测试图片
    test_img = Image.new('RGB', (400, 300), color='white')
    draw = ImageDraw.Draw(test_img)
    draw.rectangle([50, 50, 150, 250], fill='red')
    draw.rectangle([150, 50, 250, 250], fill='green')
    draw.rectangle([250, 50, 350, 250], fill='blue')
    
    # 黑白滤镜
    gray = grayscale(test_img)
    save_image(gray, 'output/filter_grayscale.jpg')
    print("✓ 黑白滤镜完成")
    
    # 复古滤镜
    sepia_img = sepia(test_img)
    save_image(sepia_img, 'output/filter_sepia.jpg')
    print("✓ 复古滤镜完成")
    
    # 模糊滤镜
    blurred = blur(test_img, radius=10)
    save_image(blurred, 'output/filter_blur.jpg')
    print("✓ 模糊滤镜完成")
    
    # 轮廓滤镜
    contour_img = contour(test_img)
    save_image(contour_img, 'output/filter_contour.jpg')
    print("✓ 轮廓滤镜完成")
    
    # 反色滤镜
    inverted = invert(test_img)
    save_image(inverted, 'output/filter_invert.jpg')
    print("✓ 反色滤镜完成")
    
    # 像素化滤镜
    pixelated = pixelate(test_img, pixel_size=20)
    save_image(pixelated, 'output/filter_pixelate.jpg')
    print("✓ 像素化滤镜完成")


def demo_composite_functions():
    """演示拼接功能"""
    print("\n=== 拼接功能演示 ===")
    
    # 加载示例图片
    img1 = load_image('output/sample_red.jpg')
    img2 = load_image('output/sample_green.jpg')
    img3 = load_image('output/sample_blue.jpg')
    img4 = load_image('output/sample_yellow.jpg')
    
    # 水平拼接
    horizontal = stitch_horizontal([img1, img2, img3])
    save_image(horizontal, 'output/composite_horizontal.jpg')
    print("✓ 水平拼接完成")
    
    # 垂直拼接
    vertical = stitch_vertical([img1, img2, img3])
    save_image(vertical, 'output/composite_vertical.jpg')
    print("✓ 垂直拼接完成")
    
    # 网格拼接
    grid = stitch_grid([img1, img2, img3, img4], cols=2)
    save_image(grid, 'output/composite_grid.jpg')
    print("✓ 网格拼接完成")


def demo_background_functions():
    """演示背景移除功能"""
    print("\n=== 背景移除功能演示 ===")
    
    # 加载白色背景的测试图片
    img_white_bg = load_image('output/sample_white_bg.jpg')
    
    # 简单背景移除
    removed_simple = remove_background_simple(img_white_bg, threshold=240)
    save_image(removed_simple, 'output/background_removed_simple.png')
    print("✓ 简单背景移除完成")
    
    # 指定颜色背景移除
    removed_color = remove_background_color(img_white_bg, target_color=(255, 255, 255), tolerance=50)
    save_image(removed_color, 'output/background_removed_color.png')
    print("✓ 指定颜色背景移除完成")


def demo_text_functions():
    """演示文字添加功能"""
    print("\n=== 文字添加功能演示 ===")
    
    # 创建测试图片
    test_img = Image.new('RGB', (500, 400), color='lightblue')
    
    # 中心位置添加文字
    text_center = add_text(test_img, "Center Text", position="center", font_size=40, color=(0, 0, 128))
    save_image(text_center, 'output/text_center.jpg')
    print("✓ 中心文字添加完成")
    
    # 底部添加文字
    text_bottom = add_text(test_img, "Bottom Text", position="bottom-center", font_size=30, color=(128, 0, 0))
    save_image(text_bottom, 'output/text_bottom.jpg')
    print("✓ 底部文字添加完成")
    
    # 旋转文字
    text_rotated = add_text(test_img, "Rotated Text", position="center", font_size=40, color=(0, 100, 0), rotation=30)
    save_image(text_rotated, 'output/text_rotated.jpg')
    print("✓ 旋转文字添加完成")
    
    # 多个位置添加文字
    img_multi = test_img.copy()
    img_multi = add_text(img_multi, "Top-Left", position="top-left", font_size=20, color=(0, 0, 0))
    img_multi = add_text(img_multi, "Top-Right", position="top-right", font_size=20, color=(0, 0, 0))
    img_multi = add_text(img_multi, "Bottom-Left", position="bottom-left", font_size=20, color=(0, 0, 0))
    img_multi = add_text(img_multi, "Bottom-Right", position="bottom-right", font_size=20, color=(0, 0, 0))
    save_image(img_multi, 'output/text_multi.jpg')
    print("✓ 多位置文字添加完成")


def demo_complete_workflow():
    """演示完整工作流"""
    print("\n=== 完整工作流演示 ===")
    
    # 创建基础图片
    base_img = Image.new('RGB', (600, 400), color='white')
    draw = ImageDraw.Draw(base_img)
    draw.rectangle([100, 100, 500, 300], fill='skyblue')
    draw.ellipse([200, 150, 400, 250], fill='yellow')
    
    # 保存原图
    save_image(base_img, 'output/workflow_original.jpg')
    
    # 完整处理流程
    result = base_img
    result = smart_enhance(result)
    result = sepia(result)
    result = add_text(result, "p-skill Demo", position="top-center", font_size=36, color=(128, 64, 0))
    result = add_text(result, "Creative Image Processing", position="bottom-center", font_size=24, color=(128, 64, 0))
    
    save_image(result, 'output/workflow_final.jpg')
    print("✓ 完整工作流完成")


def main():
    """主函数"""
    print("=" * 50)
    print("p-skill 综合使用示例")
    print("=" * 50)
    
    try:
        # 导入 ImageDraw
        from PIL import ImageDraw
        
        # 创建示例图片
        create_sample_images()
        
        # 演示各个功能
        demo_core_functions()
        demo_enhance_functions()
        demo_filters()
        demo_composite_functions()
        demo_background_functions()
        demo_text_functions()
        demo_complete_workflow()
        
        print("\n" + "=" * 50)
        print("所有演示完成！")
        print("生成的图片保存在 'output' 目录中。")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
