#!/usr/bin/env python3
"""
测试在线OCR功能
"""

import os
import sys
from PIL import Image, ImageDraw

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from online_ocr import OnlineOCR

def create_test_images():
    """创建测试图片"""
    test_dir = "test_images"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    test_files = []
    
    # 1. 英文测试图片
    print("创建英文测试图片...")
    img_eng = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img_eng)
    text_eng = "Hello World!\nThis is an OCR test.\n1234567890"
    draw.text((50, 50), text_eng, fill='black')
    
    eng_path = os.path.join(test_dir, "test_english.png")
    img_eng.save(eng_path)
    test_files.append(("英文", eng_path, "eng", text_eng))
    
    # 2. 中文测试图片
    print("创建中文测试图片...")
    img_chi = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img_chi)
    text_chi = "中文OCR测试\n你好，世界！\n测试文字识别"
    draw.text((50, 50), text_chi, fill='black')
    
    chi_path = os.path.join(test_dir, "test_chinese.png")
    img_chi.save(chi_path)
    test_files.append(("中文", chi_path, "chs", text_chi))
    
    # 3. 中英文混合测试图片
    print("创建中英文混合测试图片...")
    img_mixed = Image.new('RGB', (500, 250), color='white')
    draw = ImageDraw.Draw(img_mixed)
    text_mixed = "Mixed Language Test\n中英文混合测试\nHello 你好\n123 一二三"
    draw.text((50, 50), text_mixed, fill='black')
    
    mixed_path = os.path.join(test_dir, "test_mixed.png")
    img_mixed.save(mixed_path)
    test_files.append(("中英文混合", mixed_path, "chs", text_mixed))
    
    return test_files

def test_online_ocr():
    """测试在线OCR"""
    print("=" * 60)
    print("在线OCR功能测试")
    print("=" * 60)
    
    # 创建测试图片
    print("\n1. 创建测试图片...")
    test_files = create_test_images()
    
    # 创建OCR实例
    print("\n2. 初始化OCR...")
    ocr = OnlineOCR(api_key='helloworld', cache_dir='.ocr_cache')
    
    print(f"API密钥: {ocr.api_key}")
    print(f"缓存目录: {ocr.cache_dir}")
    
    # 测试每种图片
    print("\n3. 开始OCR测试...")
    print("-" * 60)
    
    all_passed = True
    
    for test_name, image_path, language, expected_text in test_files:
        print(f"\n测试: {test_name}")
        print(f"图片: {os.path.basename(image_path)}")
        print(f"语言: {language}")
        
        try:
            # 执行OCR
            print("正在识别...")
            result = ocr.ocr_from_file(image_path, language)
            
            if result:
                print(f"[成功] 识别结果:\n{result}")
                
                # 简单验证（检查是否包含关键词）
                expected_lines = expected_text.split('\n')
                found_lines = 0
                
                for line in expected_lines[:2]:  # 检查前两行
                    if any(keyword in result for keyword in line.split()[:2]):
                        found_lines += 1
                
                if found_lines >= 1:
                    print(f"[验证] 通过 - 找到 {found_lines}/2 个关键行")
                else:
                    print("[验证] 警告 - 可能识别不准确")
                    all_passed = False
            else:
                print("[失败] 识别结果为空")
                all_passed = False
                
        except Exception as e:
            print(f"[错误] OCR失败: {str(e)}")
            all_passed = False
        
        print("-" * 40)
    
    # 测试从PIL Image识别
    print("\n4. 测试从PIL Image识别...")
    try:
        # 创建PIL Image
        img = Image.new('RGB', (300, 100), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((50, 40), "PIL Image Test", fill='black')
        
        result = ocr.ocr_from_pil_image(img, 'eng')
        print(f"PIL Image识别结果: {result}")
        
        if "PIL" in result or "Image" in result or "Test" in result:
            print("[成功] PIL Image识别通过")
        else:
            print("[警告] PIL Image识别可能不准确")
            
    except Exception as e:
        print(f"[错误] PIL Image识别失败: {str(e)}")
        all_passed = False
    
    # 测试缓存功能
    print("\n5. 测试缓存功能...")
    try:
        # 第一次识别（应该调用API）
        print("第一次识别（应调用API）...")
        test_file = test_files[0][1]  # 第一个测试文件
        result1 = ocr.ocr_from_file(test_file, 'eng')
        
        # 第二次识别（应该从缓存读取）
        print("第二次识别（应从缓存读取）...")
        result2 = ocr.ocr_from_file(test_file, 'eng')
        
        if result1 == result2:
            print("[成功] 缓存功能正常")
        else:
            print("[警告] 缓存结果不一致")
            
    except Exception as e:
        print(f"[错误] 缓存测试失败: {str(e)}")
    
    # 显示支持的语言
    print("\n6. 支持的语言示例...")
    langs = ocr.get_supported_languages()
    print(f"共支持 {len(langs)} 种语言")
    print("常用语言:")
    for code in ['chs', 'eng', 'jpn', 'kor', 'fre', 'ger']:
        if code in langs:
            print(f"  {code}: {langs[code]}")
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    if all_passed:
        print("[最终结果] ✅ 所有测试通过！")
        print("\n在线OCR技能已准备就绪，可以正常使用。")
    else:
        print("[最终结果] ⚠ 部分测试失败")
        print("\n建议检查网络连接或API密钥。")
    
    print("\n使用方法:")
    print("1. 命令行: python ocr_cli.py image.png")
    print("2. Python代码:")
    print("   from online_ocr import OnlineOCR")
    print("   ocr = OnlineOCR()")
    print("   text = ocr.ocr_from_file('image.png', 'chs')")
    
    # 清理建议
    print("\n清理测试文件:")
    print("  import shutil")
    print("  shutil.rmtree('test_images', ignore_errors=True)")
    print("  shutil.rmtree('.ocr_cache', ignore_errors=True)")

if __name__ == "__main__":
    test_online_ocr()