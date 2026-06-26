"""数据加载与预处理"""
import pandas as pd
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class StrategyData:
    """策略数据容器"""
    nav: pd.DataFrame           # 日期, 净值 (sorted by date asc)
    variety_nav: Optional[pd.DataFrame]  # 日期, 品种, 净值 (sorted by date asc)
    name: str = "策略"
    start_date: str = ""
    end_date: str = ""
    trading_days: int = 0


def load_strategy_data(
    nav_path: str,
    variety_path: Optional[str] = None,
    name: str = "策略",
) -> StrategyData:
    """加载策略数据"""
    # 加载策略净值
    nav = pd.read_excel(nav_path)
    nav.columns = ["日期", "净值"]
    nav["日期"] = pd.to_datetime(nav["日期"])
    nav = nav.sort_values("日期").reset_index(drop=True)
    nav = nav.dropna(subset=["净值"])

    # 计算日收益率
    nav["日收益率"] = nav["净值"].pct_change()

    # 加载品种净值
    variety_nav = None
    if variety_path and Path(variety_path).exists():
        variety_nav = pd.read_excel(variety_path)
        variety_nav.columns = ["日期", "品种", "净值"]
        variety_nav["日期"] = pd.to_datetime(variety_nav["日期"])
        variety_nav = variety_nav.sort_values(["品种", "日期"]).reset_index(drop=True)
        # 计算每品种日收益率
        variety_nav["日收益率"] = variety_nav.groupby("品种")["净值"].pct_change()

    return StrategyData(
        nav=nav,
        variety_nav=variety_nav,
        name=name,
        start_date=nav["日期"].min().strftime("%Y-%m-%d"),
        end_date=nav["日期"].max().strftime("%Y-%m-%d"),
        trading_days=len(nav),
    )


def auto_detect_data(data_dir: str = "data") -> tuple[str, Optional[str], str]:
    """自动检测 data 目录下的 Excel 文件，返回 (策略净值路径, 品种净值路径, 策略名)"""
    p = Path(data_dir)
    files = list(p.glob("*.xlsx")) + list(p.glob("*.xls"))

    nav_path = None
    variety_path = None
    name = "策略"

    for f in files:
        fname = f.stem
        if "品种" in fname:
            variety_path = str(f)
            # 提取策略名: 去掉 "品种净值" 后缀
            name_candidate = fname.replace("品种净值", "").replace("品种", "").strip()
            if name_candidate:
                name = name_candidate
        elif "策略" in fname or "净值" in fname:
            nav_path = str(f)
            name_candidate = fname.replace("策略净值", "").replace("净值", "").strip()
            if name_candidate:
                name = name_candidate

    if nav_path is None:
        # fallback: 选最小的文件作为策略净值
        files_sorted = sorted(files, key=lambda f: f.stat().st_size)
        if files_sorted:
            nav_path = str(files_sorted[0])
            if len(files_sorted) > 1:
                variety_path = str(files_sorted[1])

    return nav_path, variety_path, name
