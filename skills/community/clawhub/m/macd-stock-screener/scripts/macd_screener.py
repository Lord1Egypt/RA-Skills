#!/usr/bin/env python
"""
A股左右侧MACD选股 + 股吧舆情采集
===================================
选股 + 东方财富股吧舆情采集 + 报告生成。
不含回测。

策略说明:
  右侧MACD金叉 — DIF上穿DEA，趋势转多信号
  左侧MACD即将金叉 — DIF仍在DEA下方但差距在缩小，预判拐点

数据源: akshare
依赖: pip install akshare pandas numpy
"""

import argparse
import logging
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import akshare as ak
import pandas as pd
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("macd_screener")


# ════════════════════════════════════════════════════════════
#  MACD 指标计算
# ════════════════════════════════════════════════════════════

def calculate_macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    """
    计算 MACD 指标。

    Returns:
        (dif, dea, macd_hist) 三元组
    """
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    macd_hist = (dif - dea) * 2
    return dif, dea, macd_hist


# ════════════════════════════════════════════════════════════
#  数据获取
# ════════════════════════════════════════════════════════════

def get_all_a_stock_codes() -> List[Dict]:
    """获取全部A股股票列表（排除ST、*ST、退市、北交所）。"""
    logger.info("获取A股股票列表...")
    df = ak.stock_zh_a_spot_em()
    mask = ~df["名称"].str.contains(r"ST|\*ST|退", na=False)
    df = df[mask].copy()
    df = df[df["代码"].str.match(r"^(60|00|30)")]
    stocks = (
        df[["代码", "名称"]]
        .rename(columns={"代码": "stock_code", "名称": "stock_name"})
        .to_dict("records")
    )
    logger.info(f"A股可选股票数: {len(stocks)}")
    return stocks


def get_stock_hist(code: str, days: int = 120) -> Optional[pd.DataFrame]:
    """
    获取个股历史日线数据（前复权）。

    Returns:
        DataFrame with columns: date, close, open, high, low, volume
    """
    try:
        end = datetime.now().strftime("%Y%m%d")
        start = (datetime.now() - pd.Timedelta(days=days + 60)).strftime("%Y%m%d")
        df = ak.stock_zh_a_hist(
            symbol=code, period="daily",
            start_date=start, end_date=end, adjust="qfq",
        )
        if df is None or len(df) < 30:
            return None
        df = df.rename(columns={
            "日期": "date", "收盘": "close", "开盘": "open",
            "最高": "high", "最低": "low", "成交量": "volume",
        })
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)
        return df
    except Exception as e:
        logger.debug(f"获取 {code} 历史数据失败: {e}")
        return None


# ════════════════════════════════════════════════════════════
#  选股信号判断
# ════════════════════════════════════════════════════════════

def is_right_macd_golden_cross(df: pd.DataFrame) -> bool:
    """右侧MACD金叉：前一日 DIF < DEA，当日 DIF >= DEA。"""
    if len(df) < 30:
        return False
    close = df["close"]
    dif, dea, _ = calculate_macd(close)
    if len(dif) < 2:
        return False
    prev_diff = dif.iloc[-2] - dea.iloc[-2]
    curr_diff = dif.iloc[-1] - dea.iloc[-1]
    return prev_diff < 0 and curr_diff >= 0


def is_left_macd_approaching_cross(df: pd.DataFrame, lookback: int = 3) -> bool:
    """
    左侧MACD即将金叉判断：
    - DIF 仍在 DEA 下方（未金叉）
    - DIF-DEA 差距连续 lookback 日缩小
    - MACD柱状图负值在缩小
    """
    if len(df) < 30:
        return False
    close = df["close"]
    dif, dea, macd_hist = calculate_macd(close)
    if len(dif) < lookback + 1:
        return False
    if dif.iloc[-1] >= dea.iloc[-1]:
        return False
    gaps = [(dif.iloc[-i] - dea.iloc[-i]) for i in range(1, lookback + 1)]
    is_narrowing = all(gaps[i] > gaps[i + 1] for i in range(len(gaps) - 1))
    if not is_narrowing:
        return False
    if macd_hist.iloc[-1] < 0 and macd_hist.iloc[-1] > macd_hist.iloc[-2]:
        return True
    return False


# ════════════════════════════════════════════════════════════
#  选股主流程
# ════════════════════════════════════════════════════════════

def run_right_macd_selection(stocks: List[Dict], top_n: int = 10) -> List[Dict]:
    """右侧MACD金叉选股。"""
    logger.info(f"右侧MACD金叉选股，扫描 {len(stocks)} 只...")
    candidates = []
    for i, stock in enumerate(stocks):
        code = stock["stock_code"]
        if (i + 1) % 100 == 0:
            logger.info(f"  扫描进度: {i+1}/{len(stocks)}")
        try:
            df = get_stock_hist(code, days=120)
            if df is None:
                continue
            if is_right_macd_golden_cross(df):
                candidates.append({
                    "stock_code": code,
                    "stock_name": stock["stock_name"],
                    "close_price": float(df["close"].iloc[-1]),
                    "date": df["date"].iloc[-1].strftime("%Y-%m-%d"),
                })
                logger.info(f"  [右侧金叉] {code} {stock['stock_name']}")
        except Exception as e:
            logger.debug(f"  扫描 {code} 出错: {e}")
            continue
        time.sleep(random.uniform(0.1, 0.3))
    candidates = candidates[:top_n]
    logger.info(f"右侧MACD金叉选股完成: {len(candidates)} 只")
    return candidates


def run_left_macd_selection(stocks: List[Dict], top_n: int = 10) -> List[Dict]:
    """左侧MACD即将金叉选股，按DIF-DEA差距升序排列。"""
    logger.info(f"左侧MACD即将金叉选股，扫描 {len(stocks)} 只...")
    candidates = []
    for i, stock in enumerate(stocks):
        code = stock["stock_code"]
        if (i + 1) % 100 == 0:
            logger.info(f"  扫描进度: {i+1}/{len(stocks)}")
        try:
            df = get_stock_hist(code, days=120)
            if df is None:
                continue
            if is_left_macd_approaching_cross(df):
                close = df["close"]
                dif, dea, _ = calculate_macd(close)
                gap = abs(dif.iloc[-1] - dea.iloc[-1])
                candidates.append({
                    "stock_code": code,
                    "stock_name": stock["stock_name"],
                    "close_price": float(df["close"].iloc[-1]),
                    "date": df["date"].iloc[-1].strftime("%Y-%m-%d"),
                    "dif_dea_gap": float(gap),
                })
                logger.info(f"  [左侧即将金叉] {code} {stock['stock_name']} gap={gap:.4f}")
        except Exception as e:
            logger.debug(f"  扫描 {code} 出错: {e}")
            continue
        time.sleep(random.uniform(0.1, 0.3))
    candidates.sort(key=lambda x: x.get("dif_dea_gap", 999))
    candidates = candidates[:top_n]
    logger.info(f"左侧MACD即将金叉选股完成: {len(candidates)} 只")
    return candidates


# ════════════════════════════════════════════════════════════
#  股吧舆情采集
# ════════════════════════════════════════════════════════════

def collect_guba_sentiment(stock_code: str, stock_name: str) -> Dict:
    """
    采集东方财富股吧舆情数据。

    注释:
    - 内置随机延时(2-5秒)放慢访问速度
    - 检测到验证码立即停止并留痕

    Returns:
        { posts: [...], captcha_detected: bool, error: str, comment_count: int }
    """
    result = {"posts": [], "captcha_detected": False, "error": None, "comment_count": 0}
    try:
        try:
            df = ak.stock_comment_em()
            if df is not None and not df.empty:
                row = df[df["代码"] == stock_code]
                if not row.empty:
                    r = row.iloc[0]
                    result["posts"] = [
                        f"最新: {r.get('最新动态', '')}",
                        f"相关: {r.get('相关资讯', '')}",
                    ]
                    result["comment_count"] = int(r.get("评论数", 0))
        except Exception:
            pass
        delay = random.uniform(2, 5)
        time.sleep(delay)
    except Exception as e:
        result["error"] = str(e)
        if "验证码" in str(e) or "captcha" in str(e).lower():
            result["captcha_detected"] = True
            logger.warning(f"检测到验证码! 停止采集 {stock_code}")
        else:
            logger.debug(f"采集 {stock_code} 股吧数据出错: {e}")
    return result


def collect_all_sentiment(
    candidates: List[Dict],
    selection_type: str,
) -> List[Dict]:
    """采集所有候选股票的股吧舆情。"""
    logger.info(f"采集 {selection_type} 候选股吧舆情，共 {len(candidates)} 只...")
    results = []
    for i, c in enumerate(candidates):
        logger.info(f"  采集 ({i+1}/{len(candidates)}): {c['stock_code']} {c['stock_name']}")
        sentiment = collect_guba_sentiment(c["stock_code"], c["stock_name"])
        if sentiment["captcha_detected"]:
            logger.warning("检测到验证码，停止全部采集！")
            break
        c_with_sentiment = c.copy()
        c_with_sentiment["sentiment"] = sentiment
        results.append(c_with_sentiment)
    logger.info(f"舆情采集完成，共采集 {len(results)} 只")
    return results


# ════════════════════════════════════════════════════════════
#  报告生成
# ════════════════════════════════════════════════════════════

def generate_sentiment_report(
    right_candidates: List[Dict],
    left_candidates: List[Dict],
    output_dir: Path,
) -> Path:
    """生成股吧舆情情感分析报告。"""
    report_path = output_dir / "sentiment_report.md"
    lines = [
        "# 股吧舆情情感分析报告",
        "",
        f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        f"## 右侧MACD金叉候选 ({len(right_candidates)} 只)",
        "",
    ]
    for c in right_candidates:
        s = c.get("sentiment", {})
        lines.append(f"### {c['stock_code']} {c['stock_name']}")
        lines.append(f"- 收盘价: {c.get('close_price', 'N/A')}")
        if s.get("posts"):
            for p in s["posts"]:
                lines.append(f"- {p}")
        if s.get("error"):
            lines.append(f"- 采集异常: {s['error']}")
        if s.get("captcha_detected"):
            lines.append(f"- 检测到验证码，采集已中止")
        lines.append("")

    lines.extend([
        "---",
        "",
        f"## 左侧MACD即将金叉候选 ({len(left_candidates)} 只)",
        "",
    ])
    for c in left_candidates:
        s = c.get("sentiment", {})
        lines.append(f"### {c['stock_code']} {c['stock_name']}")
        lines.append(f"- 收盘价: {c.get('close_price', 'N/A')}")
        lines.append(f"- DIF-DEA差距: {c.get('dif_dea_gap', 'N/A')}")
        if s.get("posts"):
            for p in s["posts"]:
                lines.append(f"- {p}")
        if s.get("error"):
            lines.append(f"- 采集异常: {s['error']}")
        lines.append("")

    lines.extend([
        "---",
        "*本报告由MACD选股系统自动生成*",
    ])
    report_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info(f"情感分析报告已生成: {report_path}")
    return report_path


def generate_summary(
    trade_date: str,
    right_candidates: List[Dict],
    left_candidates: List[Dict],
    output_dir: Path,
) -> Path:
    """生成每日选股汇总 summary.md。"""
    summary_path = output_dir / "summary.md"
    lines = [
        "# A股MACD选股每日汇总",
        "",
        f"> 日期: {trade_date}",
        f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        "## 选股结果概览",
        "",
        "| 策略 | 候选数量 |",
        "|------|----------|",
        f"| 右侧MACD金叉 | {len(right_candidates)} 只 |",
        f"| 左侧MACD即将金叉 | {len(left_candidates)} 只 |",
        "",
        f"## 右侧MACD金叉候选 (Top {len(right_candidates)})",
        "",
    ]
    if right_candidates:
        lines.append("| 序号 | 代码 | 名称 | 收盘价 |")
        lines.append("|------|------|------|--------|")
        for i, c in enumerate(right_candidates, 1):
            lines.append(
                f"| {i} | {c['stock_code']} | {c['stock_name']} | "
                f"{c.get('close_price', 'N/A')} |"
            )
    else:
        lines.append("今日无符合条件的右侧金叉候选。")
    lines.append("")

    lines.extend([
        f"## 左侧MACD即将金叉候选 (Top {len(left_candidates)})",
        "",
    ])
    if left_candidates:
        lines.append("| 序号 | 代码 | 名称 | 收盘价 | DIF-DEA差距 |")
        lines.append("|------|------|------|--------|-------------|")
        for i, c in enumerate(left_candidates, 1):
            lines.append(
                f"| {i} | {c['stock_code']} | {c['stock_name']} | "
                f"{c.get('close_price', 'N/A')} | {c.get('dif_dea_gap', 'N/A')} |"
            )
    else:
        lines.append("今日无符合条件的左侧即将金叉候选。")
    lines.append("")

    lines.extend([
        "---",
        "",
        "## 文件清单",
        "",
        "- `right_macd_candidates.csv` — 右侧金叉候选列表",
        "- `left_macd_candidates.csv` — 左侧即将金叉候选列表",
        "- `sentiment_report.md` — 股吧舆情情感分析报告",
        "- `summary.md` — 本文件（每日汇总）",
        "",
        "---",
        "*由 macd_screener.py 自动生成*",
    ])
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info(f"每日汇总已生成: {summary_path}")
    return summary_path


# ════════════════════════════════════════════════════════════
#  结果保存
# ════════════════════════════════════════════════════════════

def save_candidates_csv(
    candidates: List[Dict],
    selection_type: str,
    output_dir: Path,
) -> Path:
    """保存候选股票列表为 CSV（含舆情字段）。"""
    csv_path = output_dir / f"{selection_type}_candidates.csv"
    if not candidates:
        csv_path.write_text("stock_code,stock_name,close_price\n", encoding="utf-8")
        return csv_path
    flat = []
    for c in candidates:
        row = {
            "stock_code": c.get("stock_code", ""),
            "stock_name": c.get("stock_name", ""),
            "close_price": c.get("close_price", ""),
        }
        if "dif_dea_gap" in c:
            row["dif_dea_gap"] = c["dif_dea_gap"]
        s = c.get("sentiment", {})
        row["comment_count"] = s.get("comment_count", "")
        row["captcha_detected"] = s.get("captcha_detected", False)
        flat.append(row)
    df = pd.DataFrame(flat)
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    logger.info(f"候选列表已保存: {csv_path}")
    return csv_path


# ════════════════════════════════════════════════════════════
#  CLI 入口
# ════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="A股左右侧MACD选股 + 股吧舆情采集",
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="输出目录（默认: outputs/YYYY-MM-DD/）",
    )
    parser.add_argument(
        "--top-n", "-n", type=int, default=10,
        help="每种策略筛选数量（默认: 10）",
    )
    parser.add_argument(
        "--right-only", action="store_true",
        help="仅运行右侧金叉选股",
    )
    parser.add_argument(
        "--left-only", action="store_true",
        help="仅运行左侧即将金叉选股",
    )
    parser.add_argument(
        "--skip-sentiment", action="store_true",
        help="跳过舆情采集",
    )
    parser.add_argument(
        "--scan-only", action="store_true",
        help="仅选股，不采集舆情",
    )
    args = parser.parse_args()

    trade_date = datetime.now().strftime("%Y-%m-%d")
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = Path.cwd() / "outputs" / trade_date
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  A股左右侧MACD选股 + 股吧舆情")
    print(f"  日期: {trade_date}")
    print(f"  输出: {output_dir}")
    print(f"{'='*60}\n")

    # Step 1-2: 选股
    stocks = get_all_a_stock_codes()
    right_candidates = []
    left_candidates = []

    if not args.left_only:
        right_candidates = run_right_macd_selection(stocks, top_n=args.top_n)
    if not args.right_only:
        left_candidates = run_left_macd_selection(stocks, top_n=args.top_n)

    # Step 3: 股吧舆情采集
    if not args.skip_sentiment and not args.scan_only:
        right_candidates = collect_all_sentiment(right_candidates, "right_macd")
        left_candidates = collect_all_sentiment(left_candidates, "left_macd")

    # Step 4: 保存结果 + 生成报告
    save_candidates_csv(right_candidates, "right_macd", output_dir)
    save_candidates_csv(left_candidates, "left_macd", output_dir)
    generate_sentiment_report(right_candidates, left_candidates, output_dir)
    summary_path = generate_summary(trade_date, right_candidates, left_candidates, output_dir)

    # 终端摘要
    print(f"\n{'='*60}")
    print(f"  任务完成!")
    print(f"  右侧MACD金叉: {len(right_candidates)} 只")
    print(f"  左侧MACD即将金叉: {len(left_candidates)} 只")
    if right_candidates:
        print(f"\n  右侧候选:")
        for i, c in enumerate(right_candidates, 1):
            print(f"    {i}. {c['stock_code']} {c['stock_name']} ¥{c['close_price']}")
    if left_candidates:
        print(f"\n  左侧候选:")
        for i, c in enumerate(left_candidates, 1):
            print(
                f"    {i}. {c['stock_code']} {c['stock_name']} "
                f"¥{c['close_price']} gap={c.get('dif_dea_gap', 0):.4f}"
            )
    print(f"  汇总文件: {summary_path}")
    print(f"{'='*60}\n")

    return {
        "trade_date": trade_date,
        "right_candidates": right_candidates,
        "left_candidates": left_candidates,
        "output_dir": str(output_dir),
    }


if __name__ == "__main__":
    main()
