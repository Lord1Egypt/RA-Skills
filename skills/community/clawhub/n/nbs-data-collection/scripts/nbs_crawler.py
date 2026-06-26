#!/usr/bin/env python3
"""
国家统计局数据采集脚本
NBS Data Collection Script

用法:
    python3 nbs_crawler.py --indicator gdp --start 2003 --end 2025
    python3 nbs_crawler.py --indicator cpi --start 2020 --end 2025
    python3 nbs_crawler.py --indicator all --resume  # 断点续采
"""

import argparse
import json
import csv
import time
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 配置
OUTPUT_DIR = Path("output")
RAW_DATA_DIR = OUTPUT_DIR / "raw_data"
CHECKPOINT_DIR = OUTPUT_DIR

# API配置（NBS新API - 如有变动请更新）
NBS_API_BASE = "https://data.stats.gov.cn"
NBS_API_QUERY = f"{NBS_API_BASE}/easyquery.htm"

# 指标ID映射
INDICATOR_IDS = {
    "gdp_quarterly": "A0B01",      # 季度GDP
    "gdp_annual": "A0B02",          # 年度GDP
    "cpi_monthly": "A01",           # 月度CPI
    "ppi_monthly": "A01",           # 月度PPI (可能需要调整)
}

# 数据源URL（用于记录）
DATA_SOURCES = {
    "gdp_quarterly": "国家统计局季度初步核算/统计年鉴",
    "cpi_monthly": "国家统计局data.stats.gov.cn",
    "ppi_monthly": "国家统计局data.stats.gov.cn",
}


def save_checkpoint(indicator: str, data: List[Dict], last_period: str):
    """保存checkpoint，支持断点续采"""
    checkpoint_file = CHECKPOINT_DIR / f"checkpoint_{indicator}.csv"
    with open(checkpoint_file, 'w', newline='', encoding='utf-8') as f:
        if data:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    print(f"Checkpoint saved: {checkpoint_file} (last: {last_period})")


def load_checkpoint(indicator: str) -> Optional[List[Dict]]:
    """加载checkpoint"""
    checkpoint_file = CHECKPOINT_DIR / f"checkpoint_{indicator}.csv"
    if checkpoint_file.exists():
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    return None


def save_raw_data(indicator: str, data: Dict):
    """保存原始数据JSON"""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    json_file = RAW_DATA_DIR / f"{indicator}.json"
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Raw data saved: {json_file}")


def fetch_gdp_quarterly(start_year: int, end_year: int) -> List[Dict]:
    """
    获取季度GDP数据
    
    注意: 由于NBS API变更，可能需要从统计公报获取数据
    """
    data = []
    
    # 尝试从API获取
    # 如果API失败，从统计公报获取
    
    for year in range(start_year, end_year + 1):
        for quarter in range(1, 5):
            period = f"{year}Q{quarter}"
            
            # TODO: 实现实际的数据获取逻辑
            # 目前返回示例数据
            record = {
                "period": period,
                "year": year,
                "quarter": quarter,
                "gdp": None,  # 待填充
                "source": "nbs_api",
                "fetch_time": datetime.now().isoformat()
            }
            data.append(record)
            
            # 模拟请求延迟
            time.sleep(0.1)
    
    return data


def fetch_cpi_monthly(start_year: int, end_year: int) -> List[Dict]:
    """获取月度CPI数据"""
    data = []
    
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            period = f"{year}-{month:02d}"
            
            record = {
                "period": period,
                "year": year,
                "month": month,
                "cpi": None,  # 待填充
                "cpi_yoy": None,  # 同比
                "source": "nbs_api",
                "fetch_time": datetime.now().isoformat()
            }
            data.append(record)
            time.sleep(0.1)
    
    return data


def calculate_quarterly_mean(monthly_data: List[Dict]) -> List[Dict]:
    """月度数据转季度均值"""
    from collections import defaultdict
    
    quarterly = defaultdict(list)
    for record in monthly_data:
        year = record['year']
        month = record['month']
        quarter = (month - 1) // 3 + 1
        key = f"{year}Q{quarter}"
        if 'cpi' in record and record['cpi']:
            quarterly[key].append(record['cpi'])
    
    result = []
    for period, values in sorted(quarterly.items()):
        if values:
            result.append({
                "period": period,
                "cpi_mean": sum(values) / len(values),
                "source": "calculated_from_monthly"
            })
    
    return result


def main():
    parser = argparse.ArgumentParser(description="国家统计局数据采集")
    parser.add_argument("--indicator", "-i", choices=["gdp", "cpi", "ppi", "all"],
                        default="all", help="指标类型")
    parser.add_argument("--start", "-s", type=int, help="起始年份")
    parser.add_argument("--end", "-e", type=int, help="结束年份")
    parser.add_argument("--resume", "-r", action="store_true", help="从checkpoint恢复")
    
    args = parser.parse_args()
    
    # 默认时间范围
    if not args.start:
        args.start = 2003
    if not args.end:
        args.end = 2025
    
    print(f"=== 国家统计局数据采集 ===")
    print(f"指标: {args.indicator}")
    print(f"时间范围: {args.start} - {args.end}")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if args.indicator in ["gdp", "all"]:
        print("\n[1/3] 采集GDP数据...")
        gdp_data = fetch_gdp_quarterly(args.start, args.end)
        save_raw_data("gdp_quarterly", {"records": {r['period']: r for r in gdp_data}})
        if gdp_data:
            save_checkpoint("gdp", gdp_data, gdp_data[-1]['period'])
        print(f"GDP数据: {len(gdp_data)} 条")
    
    if args.indicator in ["cpi", "all"]:
        print("\n[2/3] 采集CPI数据...")
        cpi_data = fetch_cpi_monthly(args.start, args.end)
        save_raw_data("cpi_monthly", {"records": {r['period']: r for r in cpi_data}})
        if cpi_data:
            save_checkpoint("cpi", cpi_data, cpi_data[-1]['period'])
        print(f"CPI数据: {len(cpi_data)} 条")
    
    if args.indicator in ["ppi", "all"]:
        print("\n[3/3] 采集PPI数据...")
        ppi_data = fetch_cpi_monthly(args.start, args.end)  # 类似逻辑
        save_raw_data("ppi_monthly", {"records": {r['period']: r for r in ppi_data}})
        if ppi_data:
            save_checkpoint("ppi", ppi_data, ppi_data[-1]['period'])
        print(f"PPI数据: {len(ppi_data)} 条")
    
    print("\n=== 采集完成 ===")


if __name__ == "__main__":
    main()
