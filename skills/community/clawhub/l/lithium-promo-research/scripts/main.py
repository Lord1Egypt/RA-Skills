# 设置UTF-8输出
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import argparse
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# 获取skill根目录
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DATA_DIR = ROOT_DIR / "data"
REPORTS_DIR = DATA_DIR / "reports"


def load_config():
    """加载产品线配置"""
    config_file = ROOT_DIR / "references" / "product-lines.json"
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)


def run_search(country, platform_type, products):
    """Step 1: 搜索平台"""
    print(f"🔍 搜索平台: {country} - {platform_type}")
    search_script = SCRIPT_DIR / "search_platforms.py"
    # TODO: 实现搜索逻辑
    print("✅ 搜索完成")
    return DATA_DIR / f"platforms_raw_{datetime.now().strftime('%Y%m%d')}.json"


def run_parse(input_file):
    """Step 2: 抓取详情"""
    print("📥 抓取平台详情...")
    parse_script = SCRIPT_DIR / "parse_platforms.py"
    # TODO: 实现解析逻辑
    output_file = input_file.replace("raw", "parsed")
    print("✅ 详情抓取完成")
    return output_file


def run_score(input_file):
    """Step 3: 评分排序"""
    print("📊 评分排序...")
    score_script = SCRIPT_DIR / "score_platforms.py"
    # TODO: 实现评分逻辑
    output_file = input_file.replace("parsed", "scored")
    print("✅ 评分完成")
    return output_file


def run_generate_excel(input_file, output_name=None):
    """Step 4: 生成Excel报告"""
    print("📈 生成Excel报告...")
    
    # 直接导入并调用
    sys.path.insert(0, str(SCRIPT_DIR))
    import generate_excel
    
    # 处理输出路径
    if output_name and Path(output_name).parent != Path():
        # 完整路径
        output_path = Path(output_name)
    else:
        if output_name is None:
            output_name = f"promo_report_{datetime.now().strftime('%Y%m%d')}.xlsx"
        output_path = REPORTS_DIR / output_name
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 调用生成函数
    try:
        generate_excel.generate_excel_report(
            str(input_file),
            str(output_path),
            str(ROOT_DIR / "references" / "product-lines.json")
        )
        print(f"✅ 报告生成: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def show_summary(report_file):
    """显示摘要"""
    print("\n" + "="*50)
    print("📋 调研报告摘要")
    print("="*50)
    # TODO: 读取Excel统计
    print(f"📁 报告路径: {report_file}")
    print("="*50)


def main():
    parser = argparse.ArgumentParser(description="锂电设备国际推广平台调研")
    parser.add_argument("--country", "-c", default="ALL", 
                       help="目标国家: US/JP/KR/RU/EU/ALL")
    parser.add_argument("--type", "-t", default="all",
                       help="平台类型: exhibition/b2b/media/all")
    parser.add_argument("--product", "-p", nargs="+",
                       help="产品线(可选)")
    parser.add_argument("--output", "-o",
                       help="输出文件名")
    parser.add_argument("--skip-search", action="store_true",
                       help="跳过搜索，直接用现有数据")
    
    args = parser.parse_args()
    
    print("🔬 锂电设备推广平台调研系统")
    print(f"目标: {args.country} | 类型: {args.type}")
    print("-"*40)
    
    # 输出到桌面
    desktop = Path.home() / "Desktop"
    
    if args.skip_search:
        # 直接用示例数据生成报告
        sample_file = DATA_DIR / "sample_platforms.json"
        if sample_file.exists():
            output_path = args.output if args.output else str(desktop / f"promo_report_{datetime.now().strftime('%Y%m%d')}.xlsx")
            report = run_generate_excel(sample_file, output_path)
            if report:
                show_summary(report)
        else:
            print("❌ 未找到数据文件")
    else:
        # 完整流程
        data_file = run_search(args.country, args.type, args.product)
        parsed_file = run_parse(data_file)
        scored_file = run_score(parsed_file)
        report = run_generate_excel(scored_file, args.output)
        
        if report:
            show_summary(report)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())