#!/usr/bin/env python3
"""
发票信息提取工具主程序（百度OCR版本）
使用百度OCR API从发票图片和PDF文件中提取信息并导出到Excel

支持多种输入方式：
- 单个文件：python main_baidu.py -f invoice.pdf
- 多个文件：python main_baidu.py -f invoice1.pdf -f invoice2.png
- 整个目录：python main_baidu.py -i ./fp
- 混合模式：python main_baidu.py -i ./fp -f extra_invoice.pdf
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import Config, setup_config
from baidu_ocr_extractor import BaiduInvoiceExtractor, extract_invoices_with_baidu
from excel_exporter import ExcelExporter


def collect_files(inputs: List[str]) -> List[Path]:
    """
    收集所有待处理的文件
    
    Args:
        inputs: 输入路径列表（文件或目录）
        
    Returns:
        所有发票文件的路径列表
    """
    supported_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.pdf'}
    files = []
    
    for input_path in inputs:
        path = Path(input_path)
        
        if not path.exists():
            print(f"[WARN] 路径不存在，跳过: {path}")
            continue
            
        if path.is_file():
            # 单个文件
            if path.suffix.lower() in supported_extensions:
                files.append(path)
            else:
                print(f"[WARN] 不支持的文件格式，跳过: {path}")
                
        elif path.is_dir():
            # 目录 - 递归收集所有支持的文件
            for ext in supported_extensions:
                files.extend(path.rglob(f"*{ext}"))
                files.extend(path.rglob(f"*{ext.upper()}"))
    
    # 去重并保持顺序
    seen = set()
    unique_files = []
    for f in files:
        resolved = f.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique_files.append(f)
    
    return unique_files


def process_files(files: List[Path], api_key: str, secret_key: str, output_dir: Path, output_name: str) -> bool:
    """
    处理文件并导出到Excel
    
    Args:
        files: 待处理的文件列表
        api_key: 百度API Key
        secret_key: 百度Secret Key
        output_dir: 输出目录
        output_name: 输出文件名前缀
        
    Returns:
        处理成功返回True
    """
    if not files:
        print("[FAIL] 没有找到可处理的发票文件")
        return False
    
    print(f"\n发现 {len(files)} 个待处理文件")
    print("-" * 60)
    for i, f in enumerate(files, 1):
        print(f"  {i}. {f.name}")
    print("-" * 60)
    
    # 初始化提取器
    extractor = BaiduInvoiceExtractor(api_key, secret_key)
    
    if not extractor.access_token:
        print("[FAIL] 百度OCR认证失败")
        return False
    
    # 处理所有文件
    invoices = []
    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] 处理: {file_path.name}")
        invoice = extractor.extract_from_file(str(file_path))
        
        if invoice:
            invoices.append(invoice)
            print(f"[OK] 成功提取: {invoice.invoice_number or '未识别号码'}")
        else:
            print(f"[FAIL] 提取失败")
    
    if not invoices:
        print("\n[FAIL] 未能提取到任何发票信息")
        return False
    
    print(f"\n[OK] 成功提取 {len(invoices)}/{len(files)} 张发票信息")
    
    # 显示提取结果摘要
    print("\n提取结果摘要:")
    print("-" * 60)
    for i, inv in enumerate(invoices, 1):
        print(f"{i}. 发票号码: {inv.invoice_number or '未识别'}")
        print(f"   开票日期: {inv.invoice_date or '未识别'}")
        print(f"   购买方: {inv.buyer_name or '未识别'}")
        print(f"   销售方: {inv.seller_name or '未识别'}")
        if inv.total_amount_with_tax:
            print(f"   金额: {inv.total_amount_with_tax:.2f}")
        else:
            print("   金额: 未识别")
        print()
    
    # 导出到Excel
    print("\n开始导出到Excel...")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"{output_name}_{timestamp}.xlsx"
    
    exporter = ExcelExporter()
    success = exporter.export_to_excel(
        invoices,
        str(output_file),
        include_items=True
    )
    
    if success:
        print("\n" + "=" * 60)
        print("处理完成!")
        print(f"输出文件: {output_file}")
        print("=" * 60)
        return True
    else:
        print("\n[FAIL] 导出失败")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='发票信息提取工具（百度OCR版）- 从图片和PDF中提取发票信息到Excel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 处理单个文件
  python main_baidu.py -f invoice.pdf
  
  # 处理多个文件
  python main_baidu.py -f invoice1.pdf -f invoice2.png
  
  # 处理整个目录
  python main_baidu.py -i ./fp
  
  # 目录 + 额外文件
  python main_baidu.py -i ./fp -f extra_invoice.pdf
  
  # 指定输出
  python main_baidu.py -i ./fp -o ./output -n "2024年3月发票"
  
  # 运行配置向导
  python main_baidu.py --setup
        """
    )

    # 输入选项
    input_group = parser.add_argument_group('输入选项')
    input_group.add_argument(
        '-f', '--file',
        action='append',
        dest='files',
        help='指定单个发票文件（可多次使用）'
    )
    input_group.add_argument(
        '-i', '--input',
        default='fp',
        help='输入目录路径（默认: fp）'
    )

    # 输出选项
    output_group = parser.add_argument_group('输出选项')
    output_group.add_argument(
        '-o', '--output',
        default='output',
        help='输出目录路径（默认: output）'
    )
    output_group.add_argument(
        '-n', '--name',
        default='发票信息',
        help='输出文件名前缀（默认: 发票信息）'
    )

    # 认证选项
    auth_group = parser.add_argument_group('认证选项')
    auth_group.add_argument(
        '--api-key',
        help='百度API Key（覆盖配置文件）'
    )
    auth_group.add_argument(
        '--secret-key',
        help='百度Secret Key（覆盖配置文件）'
    )

    # 其他选项
    parser.add_argument(
        '--setup',
        action='store_true',
        help='运行配置向导'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='只列出要处理的文件，不执行识别'
    )

    args = parser.parse_args()

    # 运行配置向导
    if args.setup:
        setup_config()
        return 0

    # 加载配置
    Config.load_from_file()

    # 检查是否有配置
    if not Config.BAIDU_API_KEY or not Config.BAIDU_SECRET_KEY:
        if not args.api_key or not args.secret_key:
            print("[WARN] 未找到百度OCR配置")
            choice = input("是否现在配置? (y/n): ").strip().lower()
            if choice == 'y':
                setup_config()
                Config.load_from_file()
            else:
                print("[FAIL] 无法继续，请配置百度OCR或提供API Key")
                return 1

    # 使用命令行参数或配置文件
    api_key = args.api_key or Config.BAIDU_API_KEY
    secret_key = args.secret_key or Config.BAIDU_SECRET_KEY

    # 收集输入路径
    inputs = []
    
    # 添加目录
    if args.input:
        inputs.append(args.input)
    
    # 添加单独指定的文件
    if args.files:
        inputs.extend(args.files)
    
    # 如果没有指定任何输入，使用默认目录
    if not inputs:
        inputs.append('fp')

    # 打印欢迎信息
    print("=" * 60)
    print("发票信息提取工具（百度OCR版）")
    print("=" * 60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 收集所有文件
    print("\n正在扫描文件...")
    files = collect_files(inputs)
    
    if not files:
        print("[FAIL] 没有找到可处理的发票文件")
        print("支持的格式: PDF, PNG, JPG, JPEG, BMP, TIFF")
        return 1
    
    # 如果只列出文件，不处理
    if args.list:
        print(f"\n共找到 {len(files)} 个文件:")
        for i, f in enumerate(files, 1):
            print(f"  {i}. {f}")
        return 0
    
    # 处理文件
    output_dir = Path(args.output)
    success = process_files(files, api_key, secret_key, output_dir, args.name)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
