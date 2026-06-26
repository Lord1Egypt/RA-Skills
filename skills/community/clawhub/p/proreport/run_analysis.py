#!/usr/bin/env python3
"""分析引擎入口 - 输出结构化 JSON + 图表，供 AI skill 使用

用法:
    python quant_report/run_analysis.py [--data data/] [--output output/] [--name 策略名]

输出:
    output/analysis.json   - 所有计算结果（指标、年度、品种等）
    output/charts/         - 12+ 张 PNG 图表
"""
import argparse
import json
import sys
import time
from pathlib import Path

# 添加父目录到 path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from quant_report.config import setup_matplotlib
from quant_report.data_loader import load_strategy_data, auto_detect_data
from quant_report.analyzer import analyze
from quant_report.chart_generator import generate_all_charts


def _calc_dd_distribution(result):
    """计算回撤天数分布统计"""
    dd = result.drawdown_series
    if dd is None or len(dd) == 0:
        return []
    vals = dd.values
    total = len(vals)
    levels = [
        ("安全区", "0% ~ -5%", (vals >= -0.05).sum(), "净值接近前高，无需干预"),
        ("注意区", "-5% ~ -10%", ((vals < -0.05) & (vals >= -0.10)).sum(), "跟踪市场变化，关注止损信号"),
        ("重视区", "-10% ~ -15%", ((vals < -0.10) & (vals >= -0.15)).sum(), "核查持仓结构，控制新增仓位"),
        ("警惕区", "-15% ~ -18%", ((vals < -0.15) & (vals >= -0.18)).sum(), "启动风控预案，强制减仓至50%"),
        ("高危区", "< -18%", (vals < -0.18).sum(), "触发熔断机制，全部清仓转观察模式"),
    ]
    return [
        {"level": name, "range": rng, "days": int(days), "pct": round(days / total * 100, 1), "desc": desc}
        for name, rng, days, desc in levels
    ]


def result_to_dict(result, name, nav_path, variety_path, charts):
    """将 AnalysisResult 对象转为 v2 报告需要的 dict 格式"""
    import json as _json
    c = result.core
    d = result.data
    return {
        "strategy_name": name,
        "data_files": {"nav": nav_path, "variety": variety_path},
        "period": {"start": d.start_date, "end": d.end_date, "trading_days": c.trading_days, "years": round(c.years, 2)},
        "core_metrics": {
            "cumulative_return": round(c.cumulative_return, 4),
            "annualized_return": round(c.annualized_return, 4),
            "annualized_volatility": round(c.annualized_volatility, 4),
            "max_drawdown": round(c.max_drawdown, 4),
            "max_drawdown_date": c.max_drawdown_date,
            "sharpe_ratio": round(c.sharpe_ratio, 2),
            "calmar_ratio": round(c.calmar_ratio, 2),
            "sortino_ratio": round(c.sortino_ratio, 2),
            "daily_win_rate": round(c.daily_win_rate, 4),
            "daily_pnl_ratio": round(c.daily_pnl_ratio, 2),
            "max_consecutive_loss_days": int(c.max_consecutive_loss_days),
            "var_95": round(c.var_95, 4),
            "start_nav": round(c.start_nav, 4),
            "end_nav": round(c.end_nav, 4),
            "peak_nav": round(c.peak_nav, 4),
        },
        "yearly": [
            {"year": y.year, "return": round(y.return_pct, 4), "volatility": round(y.volatility, 4),
             "sharpe": round(y.sharpe, 2), "max_drawdown": round(y.max_drawdown, 4), "rating": y.rating}
            for y in result.yearly
        ],
        "monthly_returns": _json.loads(result.monthly_returns.round(4).to_json()) if result.monthly_returns is not None else None,
        "drawdown_events": [
            {"start": e.start_date, "end": e.end_date, "duration": e.duration_days,
             "depth": round(e.max_depth, 4), "level": e.risk_level, "suggestion": e.suggestion}
            for e in result.drawdown_events
        ],
        "drawdown_distribution": _calc_dd_distribution(result),
        "per_10k": {
            "daily_avg": round(result.per_10k_daily.mean(), 2) if result.per_10k_daily is not None else None,
            "annual": round(result.per_10k_daily.mean() * 252, 0) if result.per_10k_daily is not None else None,
            "cumulative": round(result.per_10k_daily.sum(), 0) if result.per_10k_daily is not None else None,
            "max_profit": round(result.per_10k_daily.max(), 0) if result.per_10k_daily is not None else None,
            "max_loss": round(result.per_10k_daily.min(), 0) if result.per_10k_daily is not None else None,
        },
        "rolling_sharpe_120": {
            "mean": round(result.rolling_sharpe_120.mean(), 2) if result.rolling_sharpe_120 is not None and len(result.rolling_sharpe_120) > 0 else None,
            "latest": round(result.rolling_sharpe_120.iloc[-1], 2) if result.rolling_sharpe_120 is not None and len(result.rolling_sharpe_120) > 0 else None,
            "positive_pct": round((result.rolling_sharpe_120 > 0).mean() * 100, 1) if result.rolling_sharpe_120 is not None and len(result.rolling_sharpe_120) > 0 else None,
            "gt1_pct": round((result.rolling_sharpe_120 > 1).mean() * 100, 1) if result.rolling_sharpe_120 is not None and len(result.rolling_sharpe_120) > 0 else None,
        },
        "variety_metrics": [
            {"name": v.name, "sector": v.sector, "cum_return": round(v.cumulative_return, 4),
             "ann_return": round(v.annualized_return, 4), "sharpe": round(v.sharpe, 2),
             "win_rate": round(v.win_rate, 4), "pnl_ratio": round(v.pnl_ratio, 2),
             "max_drawdown": round(v.max_drawdown, 4)}
            for v in result.variety_metrics
        ],
        "sector_metrics": [
            {"name": s.name, "varieties": s.varieties, "avg_return": round(s.avg_return, 4),
             "total_return": round(s.total_return, 4), "avg_sharpe": round(s.avg_sharpe, 2),
             "avg_win_rate": round(s.avg_win_rate, 4), "avg_pnl_ratio": round(s.avg_pnl_ratio, 2)}
            for s in result.sector_metrics
        ],
        "charts": {k: str(Path(v).resolve()) for k, v in charts.items()},
        "output_dir": "",
    }


def main():
    parser = argparse.ArgumentParser(description="量化策略分析引擎")
    parser.add_argument("--data", default="data", help="数据目录")
    parser.add_argument("--output", default="output", help="输出目录")
    parser.add_argument("--name", default=None, help="策略名称")
    parser.add_argument("--nav", default=None, help="策略净值文件")
    parser.add_argument("--variety", default=None, help="品种净值文件")
    args = parser.parse_args()

    # 1. 加载数据
    if args.nav:
        nav_path, variety_path, name = args.nav, args.variety, args.name or "策略"
    else:
        nav_path, variety_path, name = auto_detect_data(args.data)
        if args.name:
            name = args.name

    if not nav_path:
        print(json.dumps({"error": "未找到策略净值文件"}, ensure_ascii=False))
        sys.exit(1)

    data = load_strategy_data(nav_path, variety_path, name)

    # 2. 分析
    result = analyze(data)
    c = result.core

    # 3. 生成图表
    chart_dir = f"{args.output}/charts"
    charts = generate_all_charts(result, chart_dir)

    # 4. 构建结构化输出
    output = {
        "strategy_name": name,
        "data_files": {"nav": nav_path, "variety": variety_path},
        "period": {"start": data.start_date, "end": data.end_date, "trading_days": c.trading_days, "years": round(c.years, 2)},
        "core_metrics": {
            "cumulative_return": round(c.cumulative_return, 4),
            "annualized_return": round(c.annualized_return, 4),
            "annualized_volatility": round(c.annualized_volatility, 4),
            "max_drawdown": round(c.max_drawdown, 4),
            "max_drawdown_date": c.max_drawdown_date,
            "sharpe_ratio": round(c.sharpe_ratio, 2),
            "calmar_ratio": round(c.calmar_ratio, 2),
            "sortino_ratio": round(c.sortino_ratio, 2),
            "daily_win_rate": round(c.daily_win_rate, 4),
            "daily_pnl_ratio": round(c.daily_pnl_ratio, 2),
            "max_consecutive_loss_days": int(c.max_consecutive_loss_days),
            "var_95": round(c.var_95, 4),
            "start_nav": round(c.start_nav, 4),
            "end_nav": round(c.end_nav, 4),
            "peak_nav": round(c.peak_nav, 4),
        },
        "yearly": [
            {"year": y.year, "return": round(y.return_pct, 4), "volatility": round(y.volatility, 4),
             "sharpe": round(y.sharpe, 2), "max_drawdown": round(y.max_drawdown, 4), "rating": y.rating}
            for y in result.yearly
        ],
        "monthly_returns": json.loads(result.monthly_returns.round(4).to_json()) if result.monthly_returns is not None else None,
        "drawdown_events": [
            {"start": e.start_date, "end": e.end_date, "duration": e.duration_days,
             "depth": round(e.max_depth, 4), "level": e.risk_level, "suggestion": e.suggestion}
            for e in result.drawdown_events
        ],
        "drawdown_distribution": _calc_dd_distribution(result),
        "per_10k": {
            "daily_avg": round(result.per_10k_daily.mean(), 2) if result.per_10k_daily is not None else None,
            "annual": round(result.per_10k_daily.mean() * 252, 0) if result.per_10k_daily is not None else None,
            "cumulative": round(result.per_10k_daily.sum(), 0) if result.per_10k_daily is not None else None,
            "max_profit": round(result.per_10k_daily.max(), 0) if result.per_10k_daily is not None else None,
            "max_loss": round(result.per_10k_daily.min(), 0) if result.per_10k_daily is not None else None,
        },
        "rolling_sharpe_120": {
            "mean": round(result.rolling_sharpe_120.mean(), 2) if result.rolling_sharpe_120 is not None and len(result.rolling_sharpe_120) > 0 else None,
            "latest": round(result.rolling_sharpe_120.iloc[-1], 2) if result.rolling_sharpe_120 is not None and len(result.rolling_sharpe_120) > 0 else None,
            "positive_pct": round((result.rolling_sharpe_120 > 0).mean() * 100, 1) if result.rolling_sharpe_120 is not None and len(result.rolling_sharpe_120) > 0 else None,
            "gt1_pct": round((result.rolling_sharpe_120 > 1).mean() * 100, 1) if result.rolling_sharpe_120 is not None and len(result.rolling_sharpe_120) > 0 else None,
        },
        "variety_metrics": [
            {"name": v.name, "sector": v.sector, "cum_return": round(v.cumulative_return, 4),
             "ann_return": round(v.annualized_return, 4), "sharpe": round(v.sharpe, 2),
             "win_rate": round(v.win_rate, 4), "pnl_ratio": round(v.pnl_ratio, 2),
             "max_drawdown": round(v.max_drawdown, 4)}
            for v in result.variety_metrics
        ],
        "sector_metrics": [
            {"name": s.name, "varieties": s.varieties, "avg_return": round(s.avg_return, 4),
             "total_return": round(s.total_return, 4), "avg_sharpe": round(s.avg_sharpe, 2),
             "avg_win_rate": round(s.avg_win_rate, 4), "avg_pnl_ratio": round(s.avg_pnl_ratio, 2)}
            for s in result.sector_metrics
        ],
        "charts": {k: str(Path(v).resolve()) for k, v in charts.items()},
        "output_dir": str(Path(args.output).resolve()),
    }

    # 5. 保存 JSON
    out_path = f"{args.output}/analysis.json"
    Path(args.output).mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
