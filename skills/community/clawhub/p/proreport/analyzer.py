"""核心分析引擎 - 计算所有量化指标"""
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Optional
from .data_loader import StrategyData
from .config import get_sector, star_rating


@dataclass
class CoreMetrics:
    """核心指标"""
    cumulative_return: float = 0.0
    annualized_return: float = 0.0
    annualized_volatility: float = 0.0
    max_drawdown: float = 0.0
    max_drawdown_date: str = ""
    sharpe_ratio: float = 0.0
    calmar_ratio: float = 0.0
    sortino_ratio: float = 0.0
    daily_win_rate: float = 0.0
    daily_pnl_ratio: float = 0.0
    max_consecutive_loss_days: int = 0
    var_95: float = 0.0
    start_nav: float = 1.0
    end_nav: float = 1.0
    peak_nav: float = 1.0
    trading_days: int = 0
    years: float = 0.0


@dataclass
class PeriodReturn:
    """周期收益"""
    period: str
    return_pct: float
    volatility: float
    sharpe: float
    max_drawdown: float


@dataclass
class YearlyMetrics:
    """年度指标"""
    year: int
    return_pct: float
    volatility: float
    sharpe: float
    max_drawdown: float
    rating: str = ""


@dataclass
class DrawdownEvent:
    """回撤事件"""
    start_date: str
    end_date: str
    duration_days: int
    max_depth: float
    risk_level: str
    suggestion: str


@dataclass
class VarietyMetrics:
    """品种指标"""
    name: str
    sector: str
    cumulative_return: float
    annualized_return: float
    volatility: float
    sharpe: float
    win_rate: float
    pnl_ratio: float
    max_drawdown: float
    trading_days: int


@dataclass
class SectorMetrics:
    """板块指标"""
    name: str
    varieties: list
    avg_return: float
    total_return: float
    avg_sharpe: float
    avg_win_rate: float
    avg_pnl_ratio: float


@dataclass
class AnalysisResult:
    """完整分析结果"""
    data: StrategyData = None
    core: CoreMetrics = None
    yearly: list = field(default_factory=list)
    monthly_returns: pd.DataFrame = None    # pivot: year x month
    weekly_returns: pd.Series = None
    drawdown_series: pd.Series = None
    drawdown_events: list = field(default_factory=list)
    rolling_sharpe_20: pd.Series = None
    rolling_sharpe_60: pd.Series = None
    rolling_sharpe_120: pd.Series = None
    variety_metrics: list = field(default_factory=list)
    sector_metrics: list = field(default_factory=list)
    per_10k_daily: pd.Series = None


def analyze(data: StrategyData) -> AnalysisResult:
    """执行完整分析"""
    result = AnalysisResult(data=data)
    nav = data.nav.copy()

    # === 核心指标 ===
    result.core = _compute_core_metrics(nav)

    # === 回撤序列 ===
    result.drawdown_series = _compute_drawdown_series(nav)

    # === 年度指标 ===
    result.yearly = _compute_yearly_metrics(nav)

    # === 月度收益矩阵 ===
    result.monthly_returns = _compute_monthly_returns(nav)

    # === 周度收益 ===
    result.weekly_returns = _compute_weekly_returns(nav)

    # === 滚动夏普 ===
    result.rolling_sharpe_20 = _rolling_sharpe(nav, 20)
    result.rolling_sharpe_60 = _rolling_sharpe(nav, 60)
    result.rolling_sharpe_120 = _rolling_sharpe(nav, 120)

    # === 回撤事件 ===
    result.drawdown_events = _find_drawdown_events(nav, result.drawdown_series)

    # === 每万元每日收益 ===
    result.per_10k_daily = nav["日收益率"].dropna() * 10000

    # === 品种分析 ===
    if data.variety_nav is not None:
        result.variety_metrics = _compute_variety_metrics(data.variety_nav)
        result.sector_metrics = _compute_sector_metrics(result.variety_metrics)

    return result


def _compute_core_metrics(nav: pd.DataFrame) -> CoreMetrics:
    m = CoreMetrics()
    m.start_nav = nav["净值"].iloc[0]
    m.end_nav = nav["净值"].iloc[-1]
    m.peak_nav = nav["净值"].max()
    m.trading_days = len(nav)
    m.years = m.trading_days / 252

    # 收益
    m.cumulative_return = m.end_nav / m.start_nav - 1
    m.annualized_return = (1 + m.cumulative_return) ** (1 / m.years) - 1 if m.years > 0 else 0

    # 波动率
    daily_ret = nav["日收益率"].dropna()
    m.annualized_volatility = daily_ret.std() * np.sqrt(252)

    # 回撤
    rolling_max = nav["净值"].cummax()
    drawdown = (nav["净值"] - rolling_max) / rolling_max
    m.max_drawdown = drawdown.min()
    m.max_drawdown_date = nav.loc[drawdown.idxmin(), "日期"].strftime("%Y-%m-%d")

    # 夏普 (无风险利率 2%)
    rf_daily = 0.02 / 252
    excess = daily_ret - rf_daily
    m.sharpe_ratio = excess.mean() / daily_ret.std() * np.sqrt(252) if daily_ret.std() > 0 else 0

    # 卡玛
    m.calmar_ratio = m.annualized_return / abs(m.max_drawdown) if m.max_drawdown != 0 else 0

    # 索提诺
    downside = daily_ret[daily_ret < 0]
    downside_std = downside.std() * np.sqrt(252)
    m.sortino_ratio = (m.annualized_return - 0.02) / downside_std if downside_std > 0 else 0

    # 胜率
    m.daily_win_rate = (daily_ret > 0).sum() / len(daily_ret) if len(daily_ret) > 0 else 0

    # 盈亏比
    avg_win = daily_ret[daily_ret > 0].mean() if (daily_ret > 0).any() else 0
    avg_loss = abs(daily_ret[daily_ret < 0].mean()) if (daily_ret < 0).any() else 1
    m.daily_pnl_ratio = avg_win / avg_loss if avg_loss > 0 else 0

    # 最大连续亏损天数
    is_loss = (daily_ret < 0).astype(int)
    groups = is_loss.ne(is_loss.shift()).cumsum()
    m.max_consecutive_loss_days = is_loss.groupby(groups).sum().max() if len(is_loss) > 0 else 0

    # VaR 95%
    m.var_95 = daily_ret.quantile(0.05)

    return m


def _compute_drawdown_series(nav: pd.DataFrame) -> pd.Series:
    rolling_max = nav["净值"].cummax()
    dd = (nav["净值"] - rolling_max) / rolling_max
    dd.index = nav["日期"]
    return dd


def _compute_yearly_metrics(nav: pd.DataFrame) -> list[YearlyMetrics]:
    nav = nav.copy()
    nav["year"] = nav["日期"].dt.year
    results = []
    for year, grp in nav.groupby("year"):
        if len(grp) < 5:
            continue
        ret = grp["净值"].iloc[-1] / grp["净值"].iloc[0] - 1
        daily_ret = grp["日收益率"].dropna()
        vol = daily_ret.std() * np.sqrt(252) if len(daily_ret) > 1 else 0
        rf_daily = 0.02 / 252
        sharpe = (daily_ret.mean() - rf_daily) / daily_ret.std() * np.sqrt(252) if daily_ret.std() > 0 else 0
        rolling_max = grp["净值"].cummax()
        mdd = ((grp["净值"] - rolling_max) / rolling_max).min()
        rating = star_rating(sharpe, ret, mdd)
        results.append(YearlyMetrics(
            year=int(year), return_pct=ret, volatility=vol,
            sharpe=sharpe, max_drawdown=mdd, rating=rating
        ))
    return results


def _compute_monthly_returns(nav: pd.DataFrame) -> pd.DataFrame:
    nav = nav.copy()
    nav["year"] = nav["日期"].dt.year
    nav["month"] = nav["日期"].dt.month
    monthly = nav.groupby(["year", "month"]).agg(
        first_nav=("净值", "first"),
        last_nav=("净值", "last"),
    )
    monthly["return"] = monthly["last_nav"] / monthly["first_nav"] - 1
    pivot = monthly["return"].unstack(level="month")
    pivot.columns = [f"{m}月" for m in pivot.columns]
    return pivot


def _compute_weekly_returns(nav: pd.DataFrame) -> pd.Series:
    nav = nav.copy()
    nav["week"] = nav["日期"].dt.isocalendar().week.astype(int)
    nav["year"] = nav["日期"].dt.isocalendar().year.astype(int)
    weekly = nav.groupby(["year", "week"]).agg(
        first_nav=("净值", "first"),
        last_nav=("净值", "last"),
        date=("日期", "last"),
    )
    weekly["return"] = weekly["last_nav"] / weekly["first_nav"] - 1
    weekly.index = weekly["date"]
    return weekly["return"]


def _rolling_sharpe(nav: pd.DataFrame, window: int) -> pd.Series:
    daily_ret = nav.set_index("日期")["日收益率"].dropna()
    rf_daily = 0.02 / 252
    excess = daily_ret - rf_daily
    rolling_mean = excess.rolling(window).mean()
    rolling_std = daily_ret.rolling(window).std()
    return (rolling_mean / rolling_std * np.sqrt(252)).dropna()


def _find_drawdown_events(nav: pd.DataFrame, dd_series: pd.Series) -> list[DrawdownEvent]:
    """找出所有显著回撤事件 (>5%)"""
    events = []
    in_dd = False
    start_idx = None
    max_depth = 0

    dd_values = dd_series.values
    dates = dd_series.index

    for i in range(len(dd_values)):
        if dd_values[i] < -0.01 and not in_dd:
            in_dd = True
            start_idx = i
            max_depth = dd_values[i]
        elif in_dd:
            if dd_values[i] < max_depth:
                max_depth = dd_values[i]
            if dd_values[i] >= -0.005 or i == len(dd_values) - 1:
                in_dd = False
                if max_depth < -0.05:
                    depth = max_depth
                    duration = (dates[i] - dates[start_idx]).days
                    if depth < -0.18:
                        level, sug = "高危", "触发回撤熔断机制，强制减仓"
                    elif depth < -0.15:
                        level, sug = "警惕", "启动风控预案，强制减仓至50%"
                    elif depth < -0.10:
                        level, sug = "重视", "核查持仓结构，控制新增仓位"
                    else:
                        level, sug = "注意", "跟踪市场变化，关注止损信号"
                    events.append(DrawdownEvent(
                        start_date=dates[start_idx].strftime("%Y-%m-%d"),
                        end_date=dates[i].strftime("%Y-%m-%d"),
                        duration_days=duration,
                        max_depth=depth,
                        risk_level=level,
                        suggestion=sug,
                    ))

    events.sort(key=lambda e: e.max_depth)
    return events[:10]


def _compute_variety_metrics(vdf: pd.DataFrame) -> list[VarietyMetrics]:
    results = []
    for name, grp in vdf.groupby("品种"):
        grp = grp.sort_values("日期").reset_index(drop=True)
        if len(grp) < 10:
            continue
        start_nav = grp["净值"].iloc[0]
        end_nav = grp["净值"].iloc[-1]
        if start_nav == 0:
            continue

        cum_ret = end_nav / start_nav - 1
        years = len(grp) / 252
        ann_ret = (1 + cum_ret) ** (1 / years) - 1 if years > 0 else 0

        daily_ret = grp["日收益率"].dropna()
        vol = daily_ret.std() * np.sqrt(252) if len(daily_ret) > 1 else 0
        sharpe = (daily_ret.mean() - 0.02/252) / daily_ret.std() * np.sqrt(252) if daily_ret.std() > 0 else 0

        win_rate = (daily_ret > 0).sum() / len(daily_ret) if len(daily_ret) > 0 else 0
        avg_win = daily_ret[daily_ret > 0].mean() if (daily_ret > 0).any() else 0
        avg_loss = abs(daily_ret[daily_ret < 0].mean()) if (daily_ret < 0).any() else 1
        pnl_ratio = avg_win / avg_loss if avg_loss > 0 else 0

        rolling_max = grp["净值"].cummax()
        mdd = ((grp["净值"] - rolling_max) / rolling_max).min()

        results.append(VarietyMetrics(
            name=name, sector=get_sector(name),
            cumulative_return=cum_ret, annualized_return=ann_ret,
            volatility=vol, sharpe=sharpe,
            win_rate=win_rate, pnl_ratio=pnl_ratio,
            max_drawdown=mdd, trading_days=len(grp),
        ))

    results.sort(key=lambda v: v.cumulative_return, reverse=True)
    return results


def _compute_sector_metrics(variety_metrics: list[VarietyMetrics]) -> list[SectorMetrics]:
    sector_groups = {}
    for v in variety_metrics:
        sector_groups.setdefault(v.sector, []).append(v)

    results = []
    for name, varieties in sector_groups.items():
        n = len(varieties)
        results.append(SectorMetrics(
            name=name,
            varieties=[v.name for v in varieties],
            avg_return=sum(v.annualized_return for v in varieties) / n,
            total_return=sum(v.cumulative_return for v in varieties),
            avg_sharpe=sum(v.sharpe for v in varieties) / n,
            avg_win_rate=sum(v.win_rate for v in varieties) / n,
            avg_pnl_ratio=sum(v.pnl_ratio for v in varieties) / n,
        ))

    results.sort(key=lambda s: s.total_return, reverse=True)
    return results


def generate_text_summary(result: AnalysisResult) -> dict:
    """生成各章节的文字摘要"""
    c = result.core
    d = result.data

    summaries = {}

    # 执行摘要
    if c.annualized_return > 0.20:
        perf_desc = "表现优异，收益水平处于行业上游"
    elif c.annualized_return > 0.10:
        perf_desc = "表现良好，收益水平处于行业中上游"
    elif c.annualized_return > 0.05:
        perf_desc = "表现中规中矩，收益能力有待提升"
    else:
        perf_desc = "表现相对保守，收益能力较弱"

    summaries["executive"] = (
        f"本策略（{d.name}）自{d.start_date}启动运行，截至{d.end_date}，"
        f"累计运行{c.trading_days}个交易日（约{c.years:.1f}年）。"
        f"净值从起始值{c.start_nav:.4f}增长至{c.end_nav:.4f}，历史峰值达到{c.peak_nav:.4f}。\n\n"
        f"在核心业绩指标方面：策略实现累计收益率{c.cumulative_return:.2%}，"
        f"年化收益率{c.annualized_return:.2%}；期间最大回撤控制在{c.max_drawdown:.2%}以内，"
        f"风险调整后收益（夏普比率）为{c.sharpe_ratio:.2f}，"
        f"卡玛比率{c.calmar_ratio:.2f}，索提诺比率{c.sortino_ratio:.2f}。\n\n"
        f"综合评价：策略整体{perf_desc}。"
    )

    # 年度分析
    if result.yearly:
        best = max(result.yearly, key=lambda y: y.return_pct)
        worst = min(result.yearly, key=lambda y: y.return_pct)
        summaries["yearly"] = (
            f"各年度收益率分布不均匀，其中{best.year}年表现最佳（收益率{best.return_pct:.2%}），"
            f"{worst.year}年表现最弱（收益率{worst.return_pct:.2%}）。"
        )

    # 回撤分析
    if result.drawdown_events:
        worst_dd = result.drawdown_events[0]
        summaries["drawdown"] = (
            f"策略最大回撤{c.max_drawdown:.2%}，发生于{c.max_drawdown_date}附近。"
            f"历史上共发生{len(result.drawdown_events)}次显著回撤（深度>5%），"
            f"其中最严重一次回撤深度{worst_dd.max_depth:.2%}，持续{worst_dd.duration_days}天。"
        )
    else:
        summaries["drawdown"] = f"策略最大回撤{c.max_drawdown:.2%}，回撤控制表现良好。"

    # 品种/板块分析
    if result.sector_metrics:
        best_sector = max(result.sector_metrics, key=lambda s: s.total_return)
        worst_sector = min(result.sector_metrics, key=lambda s: s.total_return)
        summaries["sector"] = (
            f"从板块维度看，{best_sector.name}板块表现最佳（累计收益{best_sector.total_return:.2%}），"
            f"{worst_sector.name}板块表现最弱（累计收益{worst_sector.total_return:.2%}）。"
        )

    if result.variety_metrics:
        top3 = result.variety_metrics[:3]
        bottom3 = result.variety_metrics[-3:]
        summaries["variety"] = (
            f"盈利品种{sum(1 for v in result.variety_metrics if v.cumulative_return > 0)}个，"
            f"其中{top3[0].name}盈利最多（{top3[0].cumulative_return:.2%}）。"
            f"亏损品种{sum(1 for v in result.variety_metrics if v.cumulative_return <= 0)}个，"
            f"其中{bottom3[-1].name}亏损最多（{bottom3[-1].cumulative_return:.2%}）。"
        )

    # 改进建议
    suggestions = []
    if c.max_drawdown < -0.15:
        suggestions.append(
            "提升回撤控制能力：建议引入动态止损机制（ATR止损），"
            "建立账户级别的回撤熔断机制（回撤超12%强制减仓50%）。"
        )
    if c.sharpe_ratio < 1.0:
        suggestions.append(
            "提升夏普比率：建议通过多因子信号确认机制优化信号质量，"
            "减少假突破导致的无效交易，提升收益风险比。"
        )
    if c.daily_win_rate < 0.50:
        suggestions.append(
            "关注日胜率偏低问题：日胜率低于50%符合趋势跟踪特征，"
            "但建议优化入场时机和止盈策略，提升盈亏比至1.5以上。"
        )
    if c.daily_pnl_ratio < 1.0:
        suggestions.append(
            "提升盈亏比：当前盈亏比偏低，建议优化止盈止损策略，"
            "确保平均盈利大于平均亏损，提升交易质量。"
        )
    suggestions.append(
        "多品种分散：建议对交易品种进行相关性分析，"
        "确保组合内各品种相关系数控制在0.5以内，降低集中度风险。"
    )
    summaries["suggestions"] = suggestions

    return summaries
