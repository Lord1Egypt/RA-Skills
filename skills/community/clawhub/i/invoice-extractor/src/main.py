#!/usr/bin/env python3
"""
发票信息提取工具主程序
从fp目录下的发票图片和PDF文件中提取信息并导出到Excel
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from invoice_extractor import extract_invoices_from_directory
from excel_exporter import export_invoices, ExcelExporter


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='发票信息提取工具 - 从图片和PDF中提取发票信息到Excel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py                    # 使用默认设置，从fp目录提取
  python main.py -i ./fp -o ./output  # 指定输入输出目录
  python main.py -v                 # 显示详细处理信息
        """
    )

    parser.add_argument(
        '-i', '--input',
        default='fp',
        help='输入目录路径，包含发票图片和PDF文件 (默认: fp)'
    )

    parser.add_argument(
        '-o', '--output',
        default='output',
        help='输出目录路径 (默认: output)'
    )

    parser.add_argument(
        '-n', '--name',
        default='发票信息',
        help='输出文件名前缀 (默认: 发票信息)'
    )

    parser.add_argument(
        '--no-items',
        action='store_true',
        help='不包含商品明细工作表'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细处理信息'
    )

    args = parser.parse_args()

    # 打印欢迎信息
    print("=" * 60)
    print("发票信息提取工具")
    print("=" * 60)
    print(f"输入目录: {args.input}")
    print(f"输出目录: {args.output}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 检查输入目录
    input_dir = Path(args.input)
    if not input_dir.exists():
        print(f"\n[FAIL] 错误: 输入目录不存在: {input_dir}")
        print("请确保fp目录存在，并将发票文件放入该目录")
        return 1

    # 提取发票信息
    print("\n开始提取发票信息...")
    invoices = extract_invoices_from_directory(str(input_dir))

    if not invoices:
        print("\n[FAIL] 未能提取到任何发票信息")
        return 1

    print(f"\n[OK] 成功提取 {len(invoices)} 张发票信息")

    # 显示提取结果摘要
    print("\n提取结果摘要:")
    print("-" * 60)
    for i, inv in enumerate(invoices, 1):
        print(f"{i}. 发票号码: {inv.invoice_number or '未识别'}")
        print(f"   开票日期: {inv.invoice_date or '未识别'}")
        print(f"   销售方: {inv.seller_name or '未识别'}")
        print(f"   金额: 元{inv.total_amount_with_tax:.2f}" if inv.total_amount_with_tax else "   金额: 未识别")
        print()

    # 导出到Excel
    print("\n开始导出到Excel...")
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"{args.name}_{timestamp}.xlsx"

    exporter = ExcelExporter()
    success = exporter.export_to_excel(
        invoices,
        str(output_file),
        include_items=not args.no_items
    )

    if success:
        print("\n" + "=" * 60)
        print("处理完成!")
        print(f"输出文件: {output_file}")
        print("=" * 60)
        return 0
    else:
        print("\n[FAIL] 导出失败")
        return 1


if __name__ == '__main__':
    sys.exit(main())
