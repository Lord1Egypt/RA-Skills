#!/usr/bin/env python3
"""
payroll-data-audit: data_scan
SOP 第一步：数据扫描确认

职责：
  - 扫描工资数据的关键维度（发薪月、公司主体、计薪项、特殊人员）
  - 检测数据质量问题（工号重复、姓名为空）
  - 输出结构化 JSON + 人类可读确认摘要
  - 自动生成问题清单，无需人工确认

用法:
    python3 scripts/data_scan.py --data <工资数据.csv> --output /tmp/scan_result.json
    python3 scripts/data_scan.py --data <工资数据.csv> --preview  # 仅打印摘要
"""

import json
import argparse
from pathlib import Path
from decimal import Decimal

import pandas as pd

# 复用 rules_engine 的列名容错
import sys
sys.path.insert(0, str(Path(__file__).parent))
from rules_engine import normalize_columns, normalize_types, COLUMN_ALIAS

def _normalize_month(month_str: str) -> str:
    """将各种发薪月格式统一为 YYYY-MM（如 '2026年4月' → '2026-04'）。"""
    s = str(month_str).strip()
    # Handle '2026年4月' or '2026年04月'
    if '年' in s and '月' in s:
        parts = s.replace('年', '-').replace('月', '')
        year, month = parts.split('-', 1)
        return f"{year}-{int(month):02d}"
    # Handle ISO '2026-04' or '2026-04-01'
    if len(s) >= 7:
        return s[:7]
    return s


# 特殊字段别名
SPECIAL_FIELDS = {
    "实习生": ["实习生", "intern", "实习"],
    "保洁": ["保洁", "cleaner"],
    "入职日期": ["入职日期", "hire_date", "入职时间"],
    "离职日期": ["离职日期", "leave_date", "离职时间"],
    "转正薪资生效日期": ["转正薪资生效日期", "调薪生效日期"],
    "调薪生效日期": ["调薪生效日期"],
}


def scan_data(df: pd.DataFrame) -> dict:
    """执行数据扫描，返回结构化结果"""
    df = normalize_columns(df.copy())
    df = normalize_types(df)
    
    result = {
        "total_records": len(df),
        "pay_month_distribution": {},
        "company_distribution": {},
        "pay_items_summary": {},
        "special_personnel": {},
        "data_quality": {},
        "warnings": [],
    }
    
    # 1. 发薪月分布
    if "发薪月" in df.columns:
        month_dist = df["发薪月"].value_counts().to_dict()
        result["pay_month_distribution"] = {
            str(k): int(v) for k, v in sorted(month_dist.items(), reverse=True)
        }
        # 识别最新发薪月
        latest_month = max(str(k) for k in month_dist.keys())
        result["latest_pay_month"] = latest_month
    else:
        result["warnings"].append("缺少发薪月字段，无法按月分布")
        result["latest_pay_month"] = "unknown"
    
    # 2. 公司主体分布（最新发薪月）
    latest = result["latest_pay_month"]
    if "发薪月" in df.columns and "公司主体" in df.columns:
        latest_df = df[df["发薪月"].astype(str) == latest]
        company_dist = latest_df["公司主体"].value_counts().to_dict()
        result["company_distribution"] = {
            str(k): int(v) for k, v in sorted(company_dist.items(), key=lambda x: -x[1])
        }
    elif "公司主体" in df.columns:
        company_dist = df["公司主体"].value_counts().to_dict()
        result["company_distribution"] = {
            str(k): int(v) for k, v in sorted(company_dist.items(), key=lambda x: -x[1])
        }
    
    # 3. 主要计薪项汇总
    pay_item_cols = [
        "应发合计", "实发金额合计", "加班费小计",
        "个人社保", "个人公积金", "业务线奖金合计",
        "标准基本工资", "实际绩效工资", "提成&其他&奖金",
    ]
    for col in pay_item_cols:
        if col in df.columns:
            val = pd.to_numeric(df[col], errors="coerce").fillna(0).sum()
            # 使用 Decimal 保证精度
            val_dec = Decimal(str(val)).quantize(Decimal("0.01"))
            result["pay_items_summary"][col] = float(val_dec)
        else:
            result["pay_items_summary"][col] = None
            result["warnings"].append(f"缺少计薪项字段: {col}")
    
    # 4. 特殊人员统计（按最新发薪月筛选本月变动）
    if "入职日期" in df.columns and latest != "unknown":
        # Normalize latest to YYYY-MM format for ISO date matching
        latest_normalized = _normalize_month(latest)
        df_dates = pd.to_datetime(df["入职日期"], errors="coerce")
        new_hires = (df_dates.dt.strftime("%Y-%m") == latest_normalized).sum()
        result["special_personnel"]["新入职"] = int(new_hires)
    
    if "离职日期" in df.columns and latest != "unknown":
        latest_normalized = _normalize_month(latest)
        df_dates = pd.to_datetime(df["离职日期"], errors="coerce")
        leavers = (df_dates.dt.strftime("%Y-%m") == latest_normalized).sum()
        result["special_personnel"]["离职"] = int(leavers)
    
    if "转正薪资生效日期" in df.columns:
        probation_enders = df["转正薪资生效日期"].notna().sum()
        result["special_personnel"]["转正"] = int(probation_enders)
    
    if "调薪生效日期" in df.columns:
        salary_adjusters = df["调薪生效日期"].notna().sum()
        result["special_personnel"]["调薪"] = int(salary_adjusters)
    
    # 实习生/保洁检测
    for category, aliases in [("实习生", SPECIAL_FIELDS["实习生"]), ("保洁", SPECIAL_FIELDS["保洁"])]:
        for alias in aliases:
            if alias in df.columns:
                count = int((df[alias].astype(str).str.lower() == "是").sum())
                result["special_personnel"][category] = count
                break
    
    # 5. 数据质量检测
    # 工号重复
    if "工号" in df.columns:
        emp_ids = df["工号"].astype(str)
        duplicates = emp_ids[emp_ids.duplicated(keep=False)]
        if len(duplicates) > 0:
            dup_ids = duplicates.value_counts().to_dict()
            result["data_quality"]["工号重复"] = {
                "total_duplicate_records": int(len(duplicates)),
                "duplicate_ids": {str(k): int(v) for k, v in dup_ids.items()}
            }
            result["warnings"].append(f"发现 {len(duplicates)} 条工号重复记录")
        else:
            result["data_quality"]["工号重复"] = "无"
    
    # 姓名为空
    if "姓名代号" in df.columns:
        blank_names = (df["姓名代号"].astype(str).str.strip() == "").sum()
        if blank_names > 0:
            result["data_quality"]["姓名为空"] = int(blank_names)
            result["warnings"].append(f"发现 {blank_names} 条姓名为空的记录")
        else:
            result["data_quality"]["姓名为空"] = "无"
    
    return result


def format_preview(result: dict) -> str:
    """生成人类可读的确认摘要"""
    lines = []
    lines.append("=" * 60)
    lines.append("📊 工资数据扫描报告")
    lines.append("=" * 60)
    lines.append("")
    
    # 基本信息
    lines.append(f"📋 总记录数: {result['total_records']}")
    if result.get("latest_pay_month"):
        lines.append(f"📅 最新发薪月: {result['latest_pay_month']}")
    lines.append("")
    
    # 发薪月分布
    if result["pay_month_distribution"]:
        lines.append("📅 发薪月分布:")
        for month, count in result["pay_month_distribution"].items():
            marker = " ← 最新" if month == result.get("latest_pay_month") else ""
            lines.append(f"  {month}: {count} 人{marker}")
        lines.append("")
    
    # 公司主体分布
    if result["company_distribution"]:
        lines.append("🏢 公司主体分布:")
        for company, count in result["company_distribution"].items():
            lines.append(f"  {company}: {count} 人")
        lines.append("")
    
    # 计薪项汇总
    if result["pay_items_summary"]:
        lines.append("💰 主要计薪项汇总:")
        for item, val in result["pay_items_summary"].items():
            if val is not None:
                lines.append(f"  {item}: ¥{val:,.2f}")
            else:
                lines.append(f"  {item}: (缺失)")
        lines.append("")
    
    # 特殊人员
    if result["special_personnel"]:
        lines.append("👥 特殊人员:")
        for category, count in result["special_personnel"].items():
            if count > 0:
                lines.append(f"  {category}: {count} 人")
        lines.append("")
    
    # 数据质量
    if result["data_quality"]:
        lines.append("🔍 数据质量检测:")
        for item, val in result["data_quality"].items():
            if val == "无":
                lines.append(f"  {item}: ✅ 无异常")
            elif isinstance(val, dict):
                lines.append(f"  {item}: ⚠️ {val['total_duplicate_records']} 条重复")
            else:
                lines.append(f"  {item}: ⚠️ {val} 条")
        lines.append("")
    
    # 警告
    if result["warnings"]:
        lines.append("⚠️ 警告:")
        for w in result["warnings"]:
            lines.append(f"  - {w}")
        lines.append("")
    
    lines.append("=" * 60)
    lines.append("以下为数据扫描结果及潜在问题清单。问题已自动记录，请审核后处理。")
    lines.append("如有问题，请指出需要修正的地方。")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="工资数据扫描确认（SOP 第一步）")
    parser.add_argument("--data", required=True, help="工资数据文件路径 (CSV/Excel)")
    parser.add_argument("--output", help="输出 JSON 文件路径")
    parser.add_argument("--preview", action="store_true", help="仅打印人类可读摘要")
    
    args = parser.parse_args()
    
    # 读取数据
    data_path = Path(args.data)
    if data_path.suffix in (".xlsx", ".xls"):
        df = pd.read_excel(data_path)
    elif data_path.suffix == ".csv":
        df = pd.read_csv(data_path, encoding="utf-8-sig")
    else:
        print(f"❌ 不支持的文件格式: {data_path.suffix}")
        print("\n⚠️ 数据扫描完成，发现上述问题。继续执行后续审核。")
    
    # 执行扫描
    result = scan_data(df)
    
    # 输出
    if args.preview:
        print(format_preview(result))
    else:
        print(format_preview(result))
        
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2, default=str)
            print(f"\n✅ JSON 结果已保存至: {output_path}")
        else:
            print("\n" + json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
