#!/usr/bin/env python3
"""
批量处理助手
简化批量发票处理流程
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import Config
from baidu_ocr_extractor import extract_invoices_with_baidu
from excel_exporter import ExcelExporter


def main():
    parser = argparse.ArgumentParser(
        description='批量发票处理助手',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 处理目录中的所有发票
  python batch_process.py ./invoices
  
  # 处理并指定输出
  python batch_process.py ./invoices -o ./reports -n "3月发票"
        """
    )
    
    parser.add_argument(
        'directory',
        help='包含发票文件的目录'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='output',
        help='输出目录 (默认: output)'
    )
    
    parser.add_argument(
        '-n', '--name',
        default=None,
        help='输出文件名前缀 (默认: 自动根据目录名生成)'
    )
    
    parser.add_argument(
        '--no-items',
        action='store_true',
        help='不包含商品明细'
    )
    
    args = parser.parse_args()
    
    # 加载配置
    Config.load_from_file()
    
    if not Config.BAIDU_API_KEY or not Config.BAIDU_SECRET_KEY:
        print("[FAIL] 未配置百度OCR，请先运行: python src/main_baidu.py --setup")
        return 1
    
    # 检查目录
    input_dir = Path(args.directory)
    if not input_dir.exists():
        print(f"[FAIL] 目录不存在: {input_dir}")
        return 1
    
    # 自动生成文件名
    if args.name is None:
        args.name = f"发票信息_{input_dir.name}"
    
    print("=" * 60)
    print("批量发票处理")
    print("=" * 60)
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {args.output}")
    print(f"文件名: {args.name}")
    print("=" * 60)
    
    # 提取发票
    print("\n开始处理...")
    invoices = extract_invoices_with_baidu(
        str(input_dir),
        api_key=Config.BAIDU_API_KEY,
        secret_key=Config.BAIDU_SECRET_KEY
    )
    
    if not invoices:
        print("[FAIL] 未能提取到任何发票")
        return 1
    
    # 导出
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
        print(f"\n[OK] 成功处理 {len(invoices)} 张发票")
        print(f"[OK] 输出文件: {output_file}")
        return 0
    else:
        print("[FAIL] 导出失败")
        return 1


if __name__ == '__main__':
    sys.exit(main())
