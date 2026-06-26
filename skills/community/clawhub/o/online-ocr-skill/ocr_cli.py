#!/usr/bin/env python3
"""
在线OCR命令行工具
"""

import argparse
import os
import sys
import json
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from online_ocr import OnlineOCR

def main():
    parser = argparse.ArgumentParser(
        description='在线OCR图片识别工具 - 使用OCR.space API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s image.png                    # 识别中文简体
  %(prog)s image.png -l eng             # 识别英文
  %(prog)s image.png -l chs             # 识别中文简体
  %(prog)s image.png -o result.txt      # 保存结果到文件
  %(prog)s image.png --json             # 输出JSON格式
  %(prog)s --list-langs                 # 列出支持的语言
  
支持的语言代码 (常用):
  chs - 中文简体      eng - 英文        jpn - 日文
  cht - 中文繁体      kor - 韩文        fre - 法文
  使用 --list-langs 查看完整列表
  
API密钥:
  默认使用免费密钥 'helloworld' (每月1000次请求)
  如需更多请求，请注册: https://ocr.space/ocrapi
        """
    )
    
    parser.add_argument('image', nargs='?', help='图片文件路径或URL (以http/https开头)')
    parser.add_argument('-l', '--lang', default='chs', 
                       help='语言代码 (默认: chs)')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--api-key', default='helloworld',
                       help='OCR.space API密钥 (默认: helloworld)')
    parser.add_argument('--engine', type=int, default=2, choices=[1, 2, 3],
                       help='OCR引擎 (1-3，默认: 2)')
    parser.add_argument('--json', action='store_true',
                       help='输出JSON格式的详细结果')
    parser.add_argument('--cache-dir', help='缓存目录路径')
    parser.add_argument('--no-cache', action='store_true',
                       help='禁用缓存')
    parser.add_argument('--list-langs', action='store_true',
                       help='列出所有支持的语言')
    parser.add_argument('--version', action='store_true',
                       help='显示版本信息')
    
    args = parser.parse_args()
    
    # 显示版本
    if args.version:
        print("在线OCR工具 v1.0.0")
        print("使用OCR.space API")
        return
    
    # 列出支持的语言
    if args.list_langs:
        ocr = OnlineOCR()
        langs = ocr.get_supported_languages()
        
        print("支持的语言代码:")
        print("=" * 40)
        
        # 按字母顺序排序
        sorted_langs = sorted(langs.items(), key=lambda x: x[0])
        
        for i, (code, name) in enumerate(sorted_langs, 1):
            print(f"{code:8} - {name}")
            
            # 每10个换一行
            if i % 5 == 0:
                print()
        
        print("=" * 40)
        print(f"共 {len(langs)} 种语言")
        return
    
    # 如果没有提供图片文件，显示帮助
    if not args.image:
        parser.print_help()
        return
    
    # 创建OCR实例
    cache_dir = None if args.no_cache else (args.cache_dir or '.ocr_cache')
    ocr = OnlineOCR(api_key=args.api_key, cache_dir=cache_dir)
    
    # 检查文件是否存在（如果是本地文件）
    is_url = args.image.startswith('http://') or args.image.startswith('https://')
    
    if not is_url and not os.path.exists(args.image):
        print(f"[错误] 文件不存在: {args.image}")
        sys.exit(1)
    
    # 验证文件格式（如果是本地文件）
    if not is_url:
        valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif', '.pdf'}
        file_ext = os.path.splitext(args.image)[1].lower()
        if file_ext not in valid_extensions:
            print(f"[警告] 文件扩展名 {file_ext} 可能不受支持")
            print(f"支持的格式: {', '.join(valid_extensions)}")
    
    # 显示处理信息
    print(f"[信息] 开始处理: {args.image}")
    print(f"[信息] 使用语言: {args.lang}")
    print(f"[信息] OCR引擎: {args.engine}")
    if cache_dir and not args.no_cache:
        print(f"[信息] 缓存目录: {cache_dir}")
    
    start_time = datetime.now()
    
    try:
        # 执行OCR
        if is_url:
            text = ocr.ocr_from_url(args.image, args.lang, args.engine)
        else:
            text = ocr.ocr_from_file(args.image, args.lang, args.engine)
        
        # 计算处理时间
        process_time = (datetime.now() - start_time).total_seconds()
        
        # 准备结果
        result_data = {
            "success": True,
            "text": text,
            "language": args.lang,
            "engine": args.engine,
            "source": "OCR.space API",
            "process_time_seconds": round(process_time, 2),
            "character_count": len(text),
            "line_count": len(text.splitlines()),
            "input": args.image,
            "timestamp": datetime.now().isoformat()
        }
        
        # 输出结果
        if args.json or (args.output and args.output.endswith('.json')):
            # JSON格式输出
            output_text = json.dumps(result_data, ensure_ascii=False, indent=2)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output_text)
                print(f"[成功] JSON结果已保存到: {args.output}")
            else:
                print(output_text)
        else:
            # 纯文本输出
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"[成功] 文本结果已保存到: {args.output}")
            else:
                print("\n" + "=" * 60)
                print("OCR识别结果:")
                print("=" * 60)
                print(text)
                print("=" * 60)
            
            # 显示统计信息
            print(f"\n[统计] 字符数: {len(text)}")
            print(f"[统计] 行数: {len(text.splitlines())}")
            print(f"[统计] 处理时间: {process_time:.2f}秒")
        
        print(f"[成功] OCR识别完成")
        
    except Exception as e:
        error_data = {
            "success": False,
            "error": str(e),
            "language": args.lang,
            "engine": args.engine,
            "input": args.image,
            "timestamp": datetime.now().isoformat()
        }
        
        if args.json:
            print(json.dumps(error_data, ensure_ascii=False, indent=2))
        else:
            print(f"\n[错误] OCR识别失败: {str(e)}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()