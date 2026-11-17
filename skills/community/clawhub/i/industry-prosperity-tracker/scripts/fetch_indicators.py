"""
fetch_indicators.py - 行业景气度指标数据拉取（通用版）

支持任意行业：内置已知行业预设，也接受用户自定义行业+龙头股列表。

架构：
  1. 通用宏观层（PMI、财新PMI、PPI、出口、进口）→ 所有行业共用，权重固定
  2. 动态选股层（用户/AI提供龙头股代码列表）→ 通用 stock_financial_abstract 拉取
  3. 自动权重分配 → 根据股票数量自动均分企业端权重

数据源（全部免费公开）:
  - 国家统计局 PMI/PPI  → ak.macro_china_pmi_yearly / macro_china_ppi_yearly
  - 财新 PMI           → ak.macro_china_cx_pmi_yearly
  - 海关总署 进出口     → ak.macro_china_exports_yoy / macro_china_imports_yoy
  - 交易所 财务摘要     → ak.stock_financial_abstract (任意股票代码)

用法:
    # 内置行业（预设龙头股）
    python fetch_indicators.py --sector semiconductor

    # 任意行业（AI/用户提供龙头股）
    python fetch_indicators.py --sector pharma --sector-name "医药" \
        --stocks "600276:恒瑞医药,603259:药明康德,600436:片仔癀"

    # 也支持 --industry 兼容旧参数名
    python fetch_indicators.py --industry semiconductor

输出:
    data/{sector}_latest.json
"""

import json
import argparse
import os
import math
from datetime import datetime

try:
    import akshare as ak
    AK_AVAILABLE = True
except ImportError:
    AK_AVAILABLE = False
    print("[ERROR] AKShare not installed. Run: pip install akshare")


# ============================================================
# 内置行业配置（已知行业的预设龙头股）
# 新增内置行业只需在此添加一行
# ============================================================

BUILTIN_SECTORS = {
    "semiconductor": {
        "name": "半导体",
        "stocks": [
            ("002371", "北方华创"),
            ("603501", "韦尔股份"),
        ],
    },
    "pharma": {
        "name": "医药",
        "stocks": [
            ("600276", "恒瑞医药"),
            ("603259", "药明康德"),
            ("600436", "片仔癀"),
        ],
    },
    "new_energy": {
        "name": "新能源",
        "stocks": [
            ("300750", "宁德时代"),
            ("002594", "比亚迪"),
        ],
    },
    "consumer": {
        "name": "消费品",
        "stocks": [
            ("600519", "贵州茅台"),
            ("000858", "五粮液"),
        ],
    },
}


# ============================================================
# 通用数据拉取函数（与行业无关）
# ============================================================

def fetch_macro_latest(func, indicator_name):
    """
    拉取宏观经济指标最新两期数据。
    AKShare 宏观数据统一格式: columns=[商品, 日期, 今值, 预测值, 前值]
    """
    if not AK_AVAILABLE:
        return None, None, None, None
    try:
        df = func()
        df = df.dropna(subset=["今值"])
        if len(df) < 2:
            return None, None, None, None
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        val = float(latest["今值"])
        prev_val = float(latest["前值"]) if not math.isnan(float(latest["前值"])) else float(prev["今值"])
        date_str = str(latest["日期"])[:10]
        prev_date_str = str(prev["日期"])[:10]
        return val, prev_val, date_str, prev_date_str
    except Exception as e:
        print(f"  [WARN] {indicator_name} 获取失败: {e}")
        return None, None, None, None


def fetch_stock_single_quarter(stock_code, indicator_name="营业总收入"):
    """
    从财务摘要计算最近两个单季度的指标值。
    财务摘要是累计值（Q1=单季, H1=上半年累计, 9M=前三季累计, FY=全年累计），
    需要差分得到单季度值。适用于任意股票代码。
    """
    if not AK_AVAILABLE:
        return None, None, None, None
    try:
        df = ak.stock_financial_abstract(symbol=stock_code)
        row = df[df["指标"] == indicator_name]
        if row.empty:
            print(f"  [WARN] {stock_code} 未找到指标: {indicator_name}")
            return None, None, None, None
        row = row.iloc[0]
        period_cols = [c for c in df.columns if c not in ["选项", "指标"]]

        quarters = []
        for col in period_cols:
            try:
                val = float(row[col])
            except (ValueError, TypeError):
                continue
            yyyymmdd = col
            year = int(yyyymmdd[:4])
            month = int(yyyymmdd[4:6])

            if month == 3:
                q_val = val
            elif month == 6:
                q1_col = f"{year}0331"
                if q1_col in period_cols:
                    try:
                        q1_val = float(row[q1_col])
                        q_val = val - q1_val
                    except (ValueError, TypeError):
                        continue
                else:
                    continue
            elif month == 9:
                h1_col = f"{year}0630"
                if h1_col in period_cols:
                    try:
                        h1_val = float(row[h1_col])
                        q_val = val - h1_val
                    except (ValueError, TypeError):
                        continue
                else:
                    continue
            elif month == 12:
                q3_col = f"{year}0930"
                if q3_col in period_cols:
                    try:
                        q3_val = float(row[q3_col])
                        q_val = val - q3_val
                    except (ValueError, TypeError):
                        continue
                else:
                    continue
            else:
                continue

            if math.isnan(q_val) or q_val == 0:
                continue
            quarters.append((col, q_val, year, (month // 3)))

        if len(quarters) < 2:
            print(f"  [WARN] {stock_code} 有效季度数据不足: {indicator_name}")
            return None, None, None, None

        latest = quarters[0]
        prev = quarters[1]
        return latest[1], prev[1], latest[0], prev[0]
    except Exception as e:
        print(f"  [WARN] {stock_code} 财务数据获取失败: {e}")
        return None, None, None, None


def calc_gross_margin_single_quarter(stock_code):
    """
    计算最近两个单季度的毛利率。适用于任意股票代码。
    毛利率 = (营业收入 - 营业成本) / 营业收入 * 100
    """
    if not AK_AVAILABLE:
        return None, None, None, None
    try:
        df = ak.stock_financial_abstract(symbol=stock_code)
        rev_row = df[df["指标"] == "营业总收入"]
        cost_row = df[df["指标"] == "营业成本"]
        if rev_row.empty or cost_row.empty:
            return None, None, None, None
        rev = rev_row.iloc[0]
        cost = cost_row.iloc[0]
        period_cols = [c for c in df.columns if c not in ["选项", "指标"]]

        quarters = []
        for col in period_cols:
            try:
                rev_val = float(rev[col])
                cost_val = float(cost[col])
            except (ValueError, TypeError):
                continue
            yyyymmdd = col
            year = int(yyyymmdd[:4])
            month = int(yyyymmdd[4:6])

            if month == 3:
                q_rev = rev_val
                q_cost = cost_val
            elif month == 6:
                q1_col = f"{year}0331"
                if q1_col in period_cols:
                    try:
                        q1_rev = float(rev[q1_col])
                        q1_cost = float(cost[q1_col])
                        q_rev = rev_val - q1_rev
                        q_cost = cost_val - q1_cost
                    except (ValueError, TypeError):
                        continue
                else:
                    continue
            elif month == 9:
                h1_col = f"{year}0630"
                if h1_col in period_cols:
                    try:
                        h1_rev = float(rev[h1_col])
                        h1_cost = float(cost[h1_col])
                        q_rev = rev_val - h1_rev
                        q_cost = cost_val - h1_cost
                    except (ValueError, TypeError):
                        continue
                else:
                    continue
            elif month == 12:
                q3_col = f"{year}0930"
                if q3_col in period_cols:
                    try:
                        q3_rev = float(rev[q3_col])
                        q3_cost = float(cost[q3_col])
                        q_rev = rev_val - q3_rev
                        q_cost = cost_val - q3_cost
                    except (ValueError, TypeError):
                        continue
                else:
                    continue
            else:
                continue

            if math.isnan(q_rev) or q_rev == 0:
                continue
            margin = (q_rev - q_cost) / q_rev * 100
            quarters.append((col, margin, year, (month // 3)))

        if len(quarters) < 2:
            return None, None, None, None
        return quarters[0][1], quarters[1][1], quarters[0][0], quarters[1][0]
    except Exception as e:
        print(f"  [WARN] {stock_code} 毛利率计算失败: {e}")
        return None, None, None, None


def _placeholder(id, name, tier, weight, inverted=False):
    """创建占位指标（数据获取失败时使用）"""
    return {
        "id": id, "name": name, "tier": tier, "weight": weight,
        "value": None, "value_unit": "", "prev_value": None,
        "mom_change": None, "data_source": "获取失败",
        "data_date": "", "inverted": inverted,
        "note": "数据获取失败，需检查网络或API", "needs_manual_input": True
    }


# ============================================================
# 通用行业景气度指标拉取（核心函数）
# ============================================================

def fetch_sector_indicators(sector_id, sector_name, stock_list):
    """
    通用行业景气度指标拉取引擎。

    参数:
        sector_id:   行业ID (如 "semiconductor", "pharma", "custom_医药")
        sector_name: 行业中文名 (如 "半导体", "医药")
        stock_list:  [(stock_code, stock_name), ...] 龙头股列表

    指标体系（通用框架）:

    领先指标 (40%):
      L1: 中国官方制造业PMI MoM   → 制造业整体景气方向 (15%)
      L2: 财新制造业PMI MoM       → 独立口径交叉验证 (15%)
      L3: 中国PPI年率 MoM         → 工业品价格压力 (10%)

    同步指标 (40%):
      C1: 中国出口同比 MoM        → 外需景气 (15%)
      C2: 中国进口同比 MoM        → 内需/原材料 (10%)
      C3~Cn: 龙头股单季营收 QoQ  → 企业端景气 (共15%, 按股票数均分)

    滞后指标 (20%):
      T1~Tn: 龙头股单季毛利率 QoQ → 企业端盈利 (共20%, 按股票数均分)

    所有权重自动分配，无需手动配置。
    """
    indicators = []
    fetch_date = datetime.now().strftime("%Y-%m-%d")
    n_stocks = len(stock_list)
    coincident_stock_weight = 0.15 / n_stocks if n_stocks > 0 else 0
    lagging_stock_weight = 0.20 / n_stocks if n_stocks > 0 else 0

    # ========== 领先指标（通用宏观，所有行业相同） ==========

    # L1: 中国官方制造业PMI
    print("[FETCH] L1: 中国官方制造业PMI...")
    val, prev_val, date, prev_date = fetch_macro_latest(
        ak.macro_china_pmi_yearly, "官方PMI"
    )
    if val is not None:
        mom = round(val - prev_val, 2)
        indicators.append({
            "id": "L1", "name": "中国官方制造业PMI MoM",
            "tier": "leading", "weight": 0.15,
            "value": val, "value_unit": "",
            "prev_value": prev_val, "mom_change": mom,
            "data_source": "AKShare macro_china_pmi_yearly (国家统计局)",
            "data_date": date, "inverted": False,
            "note": f"PMI值{val}（前值{prev_val}），{'扩张区间' if val > 50 else '收缩区间'}"
        })
        print(f"  -> {val} (前值 {prev_val}), MoM {mom:+}")
    else:
        indicators.append(_placeholder("L1", "中国官方制造业PMI MoM", "leading", 0.15))

    # L2: 财新制造业PMI
    print("[FETCH] L2: 财新制造业PMI...")
    val, prev_val, date, prev_date = fetch_macro_latest(
        ak.macro_china_cx_pmi_yearly, "财新PMI"
    )
    if val is not None:
        mom = round(val - prev_val, 2)
        indicators.append({
            "id": "L2", "name": "财新制造业PMI MoM",
            "tier": "leading", "weight": 0.15,
            "value": val, "value_unit": "",
            "prev_value": prev_val, "mom_change": mom,
            "data_source": "AKShare macro_china_cx_pmi_yearly (财新/Markit)",
            "data_date": date, "inverted": False,
            "note": f"PMI值{val}（前值{prev_val}），{'扩张区间' if val > 50 else '收缩区间'}"
        })
        print(f"  -> {val} (前值 {prev_val}), MoM {mom:+}")
    else:
        indicators.append(_placeholder("L2", "财新制造业PMI MoM", "leading", 0.15))

    # L3: 中国PPI年率
    print("[FETCH] L3: 中国PPI年率...")
    val, prev_val, date, prev_date = fetch_macro_latest(
        ak.macro_china_ppi_yearly, "PPI"
    )
    if val is not None:
        mom = round(val - prev_val, 2)
        indicators.append({
            "id": "L3", "name": "中国PPI年率 MoM",
            "tier": "leading", "weight": 0.10,
            "value": val, "value_unit": "%",
            "prev_value": prev_val, "mom_change": mom,
            "data_source": "AKShare macro_china_ppi_yearly (国家统计局)",
            "data_date": date, "inverted": False,
            "note": f"PPI {val}%（前值{prev_val}%），{'工业品通缩' if val < 0 else '价格回升'}，PPI回升=景气改善"
        })
        print(f"  -> {val}% (前值 {prev_val}%), MoM {mom:+}")
    else:
        indicators.append(_placeholder("L3", "中国PPI年率 MoM", "leading", 0.10))

    # ========== 同步指标 ==========

    # C1: 中国出口同比
    print("[FETCH] C1: 中国出口同比...")
    val, prev_val, date, prev_date = fetch_macro_latest(
        ak.macro_china_exports_yoy, "出口同比"
    )
    if val is not None:
        mom = round(val - prev_val, 2)
        indicators.append({
            "id": "C1", "name": "中国出口同比 MoM",
            "tier": "coincident", "weight": 0.15,
            "value": val, "value_unit": "%",
            "prev_value": prev_val, "mom_change": mom,
            "data_source": "AKShare macro_china_exports_yoy (海关总署)",
            "data_date": date, "inverted": False,
            "note": f"出口增长{val}%（前值{prev_val}%）"
        })
        print(f"  -> {val}% (前值 {prev_val}%), MoM {mom:+}")
    else:
        indicators.append(_placeholder("C1", "中国出口同比 MoM", "coincident", 0.15))

    # C2: 中国进口同比
    print("[FETCH] C2: 中国进口同比...")
    val, prev_val, date, prev_date = fetch_macro_latest(
        ak.macro_china_imports_yoy, "进口同比"
    )
    if val is not None:
        mom = round(val - prev_val, 2)
        indicators.append({
            "id": "C2", "name": "中国进口同比 MoM",
            "tier": "coincident", "weight": 0.10,
            "value": val, "value_unit": "%",
            "prev_value": prev_val, "mom_change": mom,
            "data_source": "AKShare macro_china_imports_yoy (海关总署)",
            "data_date": date, "inverted": False,
            "note": f"进口增长{val}%（前值{prev_val}%）"
        })
        print(f"  -> {val}% (前值 {prev_val}%), MoM {mom:+}")
    else:
        indicators.append(_placeholder("C2", "中国进口同比 MoM", "coincident", 0.10))

    # C3~Cn: 龙头股单季营收 QoQ（动态）
    for i, (code, name) in enumerate(stock_list):
        idx = i + 3
        ind_id = f"C{idx}"
        ind_name = f"{name}单季营收 QoQ"
        print(f"[FETCH] {ind_id}: {name}({code}) 单季营收...")
        val, prev_val, date, prev_date = fetch_stock_single_quarter(code, "营业总收入")
        if val is not None and prev_val is not None and prev_val != 0:
            qoq = round((val - prev_val) / abs(prev_val) * 100, 2)
            indicators.append({
                "id": ind_id, "name": ind_name,
                "tier": "coincident", "weight": round(coincident_stock_weight, 4),
                "value": round(val / 1e8, 2), "value_unit": "亿元",
                "prev_value": round(prev_val / 1e8, 2), "mom_change": qoq,
                "data_source": f"AKShare stock_financial_abstract ({code} {name})",
                "data_date": date, "inverted": False,
                "note": f"单季营收{round(val/1e8,2)}亿（前季{round(prev_val/1e8,2)}亿）"
            })
            print(f"  -> {round(val/1e8,2)}亿 (前季 {round(prev_val/1e8,2)}亿), QoQ {qoq:+}%")
        else:
            indicators.append(_placeholder(ind_id, ind_name, "coincident", round(coincident_stock_weight, 4)))

    # ========== 滞后指标 ==========

    # T1~Tn: 龙头股单季毛利率 QoQ（动态）
    for i, (code, name) in enumerate(stock_list):
        idx = i + 1
        ind_id = f"T{idx}"
        ind_name = f"{name}单季毛利率 QoQ"
        print(f"[FETCH] {ind_id}: {name}({code}) 单季毛利率...")
        val, prev_val, date, prev_date = calc_gross_margin_single_quarter(code)
        if val is not None and prev_val is not None:
            qoq = round(val - prev_val, 2)
            indicators.append({
                "id": ind_id, "name": ind_name,
                "tier": "lagging", "weight": round(lagging_stock_weight, 4),
                "value": round(val, 2), "value_unit": "%",
                "prev_value": round(prev_val, 2), "mom_change": qoq,
                "data_source": f"AKShare stock_financial_abstract ({code}, 营收&成本推算)",
                "data_date": date, "inverted": False,
                "note": f"毛利率{round(val,2)}%（前季{round(prev_val,2)}%）"
            })
            print(f"  -> {round(val,2)}% (前季 {round(prev_val,2)}%), QoQ {qoq:+}pp")
        else:
            indicators.append(_placeholder(ind_id, ind_name, "lagging", round(lagging_stock_weight, 4)))

    return {
        "industry": sector_id,
        "industry_name": sector_name,
        "fetch_date": fetch_date,
        "data_source_note": "所有数据来自 AKShare 开源库，对应国家统计局/海关总署/交易所公开披露数据",
        "indicators": indicators,
        "compliance_note": "数据来源均为免费公开数据，不使用付费终端数据。本工具仅提供数据整理和指标计算，不构成投资建议。"
    }


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="行业景气度指标数据拉取（通用版，支持任意行业）"
    )
    parser.add_argument("--sector", type=str, default=None,
                        help="行业ID (如: semiconductor, pharma, 或自定义ID)")
    parser.add_argument("--industry", type=str, default=None,
                        help="（兼容旧参数）等同于 --sector")
    parser.add_argument("--sector-name", type=str, default=None,
                        help="行业中文名 (如: 半导体, 医药)")
    parser.add_argument("--stocks", type=str, default=None,
                        help="龙头股列表，格式: '002371:北方华创,603501:韦尔股份'")
    parser.add_argument("--list-sectors", action="store_true",
                        help="列出所有内置行业")
    args = parser.parse_args()

    # 处理兼容参数
    sector_id = args.sector or args.industry

    if args.list_sectors:
        print("内置行业列表:")
        for sid, config in BUILTIN_SECTORS.items():
            stocks_str = ", ".join(f"{c}({n})" for c, n in config["stocks"])
            print(f"  {sid:20s} {config['name']:6s}  龙头股: {stocks_str}")
        return

    if not sector_id:
        parser.error("请提供 --sector 参数，或使用 --list-sectors 查看内置行业")
        return

    # 确定行业配置
    if sector_id in BUILTIN_SECTORS:
        config = BUILTIN_SECTORS[sector_id]
        sector_name = args.sector_name or config["name"]
        stock_list = config["stocks"]
        print(f"[INFO] 使用内置行业: {sector_name} (龙头股: {len(stock_list)} 只)")
    else:
        # 自定义行业：必须提供 --stocks
        if not args.stocks:
            print(f"[ERROR] 行业 '{sector_id}' 不在内置配置中。")
            print(f"请通过 --stocks 参数提供龙头股列表:")
            print(f"  --stocks '600276:恒瑞医药,603259:药明康德,600436:片仔癀'")
            print(f"\n内置行业: {', '.join(BUILTIN_SECTORS.keys())}")
            print(f"或使用 --list-sectors 查看详情")
            return
        sector_name = args.sector_name or sector_id
        stock_list = []
        for item in args.stocks.split(","):
            parts = item.strip().split(":")
            if len(parts) == 2:
                stock_list.append((parts[0].strip(), parts[1].strip()))
            else:
                print(f"[ERROR] 股票格式错误: '{item}'，应为 '代码:名称'")
                return
        print(f"[INFO] 自定义行业: {sector_name} (龙头股: {len(stock_list)} 只)")

    # 拉取数据
    data = fetch_sector_indicators(sector_id, sector_name, stock_list)

    # 保存
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    output_path = os.path.join(data_dir, f"{sector_id}_latest.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] 数据已保存: {output_path}")
    print(f"     行业: {data['industry_name']}")
    print(f"     指标数: {len(data['indicators'])}")
    success = sum(1 for i in data["indicators"] if i.get("value") is not None)
    failed = sum(1 for i in data["indicators"] if i.get("value") is None)
    print(f"     成功拉取: {success} 个 | 失败: {failed} 个")


if __name__ == "__main__":
    main()
