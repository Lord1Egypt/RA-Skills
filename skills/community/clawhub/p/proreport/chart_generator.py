"""图表生成引擎 - 所有 matplotlib 图表（多样化专业风格）"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.patheffects as pe
import numpy as np
import pandas as pd
from pathlib import Path
from .config import COLORS, SECTOR_PALETTE, setup_matplotlib
from .analyzer import AnalysisResult

setup_matplotlib()

# 复用色板
_BLUE = COLORS.PRIMARY
_ACCENT = COLORS.ACCENT
_GREEN = COLORS.POSITIVE
_RED = COLORS.NEGATIVE
_GREY = COLORS.NEUTRAL
_LIGHT_BG = COLORS.LIGHT_BG
_BORDER = COLORS.BORDER


def _title_bar(ax, title, color=None):
    """为图表添加带左侧色条的标题"""
    c = color or _BLUE
    ax.set_title(f"  {title}", fontsize=13, fontweight="bold", loc="left",
                 color="#1F2328", pad=12)
    # 标题左侧装饰色条
    ax.annotate("", xy=(0, 1.06), xycoords="axes fraction",
                xytext=(0.04, 1.06),
                arrowprops=dict(arrowstyle="-", color=c, lw=3.5))


def _subtitle(ax, title, color=None):
    """次级标题"""
    ax.set_title(f"  {title}", fontsize=11, fontweight="bold", loc="left",
                 color="#1F2328", pad=8)


def _style_axis(ax, grid_axis="both"):
    """统一坐标轴风格"""
    ax.grid(True, alpha=0.4, linewidth=0.5, color="#E8ECF0", axis=grid_axis)
    ax.tick_params(axis="both", which="both", length=3, colors="#57606A")
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax.spines[spine].set_color("#D1D9E0")
        ax.spines[spine].set_linewidth(0.6)


def generate_all_charts(result: AnalysisResult, output_dir: str = "output/charts") -> dict[str, str]:
    """生成所有图表，返回 {名称: 文件路径}"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    charts = {}

    charts["nav_drawdown"] = _chart_nav_drawdown(result, output_dir)
    charts["weekly_nav"] = _chart_weekly(result, output_dir)
    charts["monthly_nav"] = _chart_monthly(result, output_dir)
    charts["yearly_bar"] = _chart_yearly(result, output_dir)
    charts["heatmap"] = _chart_heatmap(result, output_dir)
    charts["radar"] = _chart_radar(result, output_dir)
    charts["rolling_sharpe"] = _chart_rolling_sharpe(result, output_dir)
    charts["per_10k"] = _chart_per_10k(result, output_dir)
    charts["drawdown_risk"] = _chart_drawdown_risk(result, output_dir)
    charts["return_distribution"] = _chart_return_distribution(result, output_dir)

    if result.variety_metrics:
        charts["variety_top"] = _chart_variety_top(result, output_dir)
        charts["sector_bar"] = _chart_sector(result, output_dir)

    plt.close("all")
    return charts


def _save(fig, path):
    fig.savefig(path, bbox_inches="tight", facecolor="white", edgecolor="none")
    plt.close(fig)
    return path


# ============================================================
# 1. 日净值曲线 + 回撤（渐变填充 + 标记点）
# ============================================================
def _chart_nav_drawdown(r: AnalysisResult, d: str) -> str:
    nav = r.data.nav
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), height_ratios=[2, 1],
                                    sharex=True, gridspec_kw={"hspace": 0.06})

    dates = nav["日期"]
    vals = nav["净值"]

    # 主净值线 + 渐变填充
    ax1.plot(dates, vals, color=_BLUE, linewidth=1.3, zorder=3)
    ax1.fill_between(dates, vals.min() * 0.98, vals, alpha=0.06, color=_BLUE)
    # 1.0 基准线
    ax1.axhline(1.0, color="#D1D9E0", linewidth=0.8, linestyle="--", zorder=1)

    peak_idx = vals.idxmax()
    ax1.scatter(dates.iloc[peak_idx], vals.iloc[peak_idx],
                color=_GREEN, s=70, zorder=5, edgecolors="white", linewidth=1.5,
                label=f"峰值 {vals.iloc[peak_idx]:.4f}")
    ax1.scatter(dates.iloc[-1], vals.iloc[-1],
                color=_ACCENT, s=70, zorder=5, edgecolors="white", linewidth=1.5,
                label=f"当前 {vals.iloc[-1]:.4f}")

    ax1.set_ylabel("净值", fontsize=11, color="#1F2328")
    ax1.legend(fontsize=9, loc="upper left", framealpha=0.9)
    _title_bar(ax1, f"策略日净值曲线（{r.data.start_date} — {r.data.end_date}）")
    _style_axis(ax1)

    dd = r.drawdown_series
    ax2.fill_between(dd.index, dd.values, 0, color=_RED, alpha=0.35, zorder=2)
    ax2.plot(dd.index, dd.values, color=_RED, linewidth=0.7, zorder=3)
    ax2.set_ylabel("回撤", fontsize=11, color="#1F2328")
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    _subtitle(ax2, "回撤曲线")
    _style_axis(ax2)

    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    fig.autofmt_xdate(rotation=30)
    return _save(fig, f"{d}/nav_drawdown.png")


# ============================================================
# 2. 周净值 + 周收益分布（双色柱 + 平滑曲线）
# ============================================================
def _chart_weekly(r: AnalysisResult, d: str) -> str:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), height_ratios=[1.2, 1],
                                    gridspec_kw={"hspace": 0.35})
    nav = r.data.nav.set_index("日期")
    weekly = nav["净值"].resample("W").last().dropna()

    # 面积图风格
    ax1.plot(weekly.index, weekly.values, color=COLORS.SECONDARY, linewidth=1.2, zorder=3)
    ax1.fill_between(weekly.index, weekly.values.min() * 0.99, weekly.values,
                     alpha=0.08, color=COLORS.SECONDARY)
    _title_bar(ax1, "策略周净值曲线", COLORS.SECONDARY)
    ax1.set_ylabel("净值")
    _style_axis(ax1)

    wr = r.weekly_returns
    colors = [_GREEN if v >= 0 else _RED for v in wr.values]
    ax2.bar(wr.index, wr.values * 100, width=5, color=colors, alpha=0.65, edgecolor="none")
    ax2.axhline(0, color="#D1D9E0", linewidth=0.6)
    # 添加移动均线
    ma = pd.Series(wr.values * 100, index=wr.index).rolling(8).mean()
    ax2.plot(wr.index, ma.values, color=_ACCENT, linewidth=1.2, label="8周均线", zorder=4)
    _title_bar(ax2, "周收益率分布", _ACCENT)
    ax2.set_ylabel("周收益率 (%)")
    ax2.legend(fontsize=8, loc="upper right")
    _style_axis(ax2)

    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    fig.autofmt_xdate(rotation=30)
    return _save(fig, f"{d}/weekly_nav.png")


# ============================================================
# 3. 月净值 + 月收益分布（阶梯+柱图）
# ============================================================
def _chart_monthly(r: AnalysisResult, d: str) -> str:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), height_ratios=[1.2, 1],
                                    gridspec_kw={"hspace": 0.35})
    nav = r.data.nav.set_index("日期")
    monthly = nav["净值"].resample("ME").last().dropna()

    # 使用阶梯线+圆点标记
    ax1.step(monthly.index, monthly.values, where="mid", color=_BLUE, linewidth=1.0, zorder=2)
    ax1.plot(monthly.index, monthly.values, "o", color=_BLUE, markersize=4, zorder=3,
             markerfacecolor="white", markeredgewidth=1.5)
    ax1.fill_between(monthly.index, monthly.values.min() * 0.999, monthly.values,
                     alpha=0.06, color=_BLUE, step="mid")
    _title_bar(ax1, "策略月净值曲线")
    ax1.set_ylabel("净值")
    _style_axis(ax1)

    monthly_ret = monthly.pct_change().dropna()
    pos = (monthly_ret > 0).sum()
    neg = (monthly_ret <= 0).sum()

    # 渐变色柱：盈利用绿色系，亏损用红色系，幅度越大颜色越深
    def _gradient_color(v, is_positive):
        if is_positive:
            intensity = min(abs(v) / max(monthly_ret.abs().max(), 0.01), 1.0)
            r_val = int(0x1A + (0x8A - 0x1A) * (1 - intensity))
            g_val = int(0x7F + (0xD4 - 0x7F) * (1 - intensity))
            b_val = int(0x37 + (0x82 - 0x37) * (1 - intensity))
            return f"#{r_val:02x}{g_val:02x}{b_val:02x}"
        else:
            intensity = min(abs(v) / max(monthly_ret.abs().max(), 0.01), 1.0)
            r_val = int(0xCF - (0xCF - 0x9B) * (1 - intensity))
            g_val = int(0x22 + (0x6A - 0x22) * (1 - intensity))
            b_val = int(0x2E + (0x5E - 0x2E) * (1 - intensity))
            return f"#{r_val:02x}{g_val:02x}{b_val:02x}"

    colors = [_gradient_color(v, v >= 0) for v in monthly_ret.values]
    ax2.bar(monthly_ret.index, monthly_ret.values * 100, width=25, color=colors,
            alpha=0.85, edgecolor="white", linewidth=0.3)
    ax2.axhline(0, color="#D1D9E0", linewidth=0.6)
    _title_bar(ax2, f"月收益率（正 {pos} | 负 {neg}）", _GREEN)
    ax2.set_ylabel("月收益率 (%)")
    _style_axis(ax2)

    fig.autofmt_xdate(rotation=30)
    return _save(fig, f"{d}/monthly_nav.png")


# ============================================================
# 4. 年度净值 + 年度收益率柱状图（左右双图）
# ============================================================
def _chart_yearly(r: AnalysisResult, d: str) -> str:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5),
                                    gridspec_kw={"wspace": 0.35})

    nav = r.data.nav.set_index("日期")
    yearly_nav = nav["净值"].resample("YE").last().dropna()

    # 左图：折线+大圆标记+值标注
    ax1.plot(yearly_nav.index.year, yearly_nav.values, color=_BLUE, linewidth=2.5,
             marker="o", markersize=8, markerfacecolor="white", markeredgewidth=2,
             markeredgecolor=_BLUE, zorder=4)
    ax1.fill_between(yearly_nav.index.year, yearly_nav.values.min() * 0.98,
                     yearly_nav.values, alpha=0.06, color=_BLUE)
    for x, y in zip(yearly_nav.index.year, yearly_nav.values):
        ax1.annotate(f"{y:.3f}", (x, y), textcoords="offset points", xytext=(0, 14),
                     fontsize=9, ha="center", fontweight="bold", color=_BLUE)
    _title_bar(ax1, "年度净值走势")
    ax1.set_ylabel("净值")
    _style_axis(ax1)

    # 右图：渐变色柱状图 + 数值标签
    years = [y.year for y in r.yearly]
    rets = [y.return_pct * 100 for y in r.yearly]
    bar_colors = []
    for v in rets:
        if v >= 10:
            bar_colors.append("#1A7F37")
        elif v >= 0:
            bar_colors.append("#57AB5A")
        elif v >= -5:
            bar_colors.append("#E09F3E")
        else:
            bar_colors.append(_RED)

    bars = ax2.bar(years, rets, color=bar_colors, alpha=0.85, width=0.6,
                   edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, rets):
        y_pos = bar.get_height() + (0.8 if val >= 0 else -1.8)
        ax2.text(bar.get_x() + bar.get_width() / 2, y_pos,
                 f"{val:+.1f}%", ha="center", fontsize=9, fontweight="bold",
                 color=bar.get_facecolor())
    ax2.axhline(0, color="#D1D9E0", linewidth=0.6)
    _title_bar(ax2, "年度收益率", _ACCENT)
    ax2.set_ylabel("收益率 (%)")
    _style_axis(ax2, grid_axis="y")

    fig.tight_layout(pad=3)
    return _save(fig, f"{d}/yearly_bar.png")


# ============================================================
# 5. 月度收益率热力图（自定义色阶）
# ============================================================
def _chart_heatmap(r: AnalysisResult, d: str) -> str:
    import seaborn as sns
    from matplotlib.colors import LinearSegmentedColormap

    pivot = r.monthly_returns * 100

    # 自定义色阶：深红→浅红→白→浅绿→深绿
    custom_cmap = LinearSegmentedColormap.from_list("quant", [
        "#B71C1C", "#EF5350", "#FFCDD2", "#FFFFFF",
        "#C8E6C9", "#66BB6A", "#1B5E20"
    ])

    fig, ax = plt.subplots(figsize=(12, max(4, len(pivot) * 0.6 + 1)))
    sns.heatmap(pivot, annot=True, fmt=".1f", center=0,
                cmap=custom_cmap, linewidths=0.8, linecolor="white", ax=ax,
                annot_kws={"size": 8, "fontweight": "bold"},
                cbar_kws={"label": "月收益率 (%)", "shrink": 0.8})
    _title_bar(ax, "月度收益率热力图")
    ax.set_ylabel("年份")
    ax.set_xlabel("月份")
    ax.tick_params(axis="both", length=0)
    fig.tight_layout()
    return _save(fig, f"{d}/heatmap.png")


# ============================================================
# 6. 雷达图（双层效果 + 辉光风格）
# ============================================================
def _chart_radar(r: AnalysisResult, d: str) -> str:
    c = r.core
    labels = ["夏普比率", "卡玛比率", "年化收益", "收益稳定性", "风险控制", "胜率"]
    values = [
        min(c.sharpe_ratio / 2.0, 1.0),
        min(c.calmar_ratio / 3.0, 1.0),
        min(c.annualized_return / 0.40, 1.0),
        min(c.sortino_ratio / 2.0, 1.0),
        min(1 + c.max_drawdown / 0.05, 1.0),
        min(c.daily_win_rate / 0.60, 1.0),
    ]
    values = [max(0, v) for v in values]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values_plot = values + values[:1]
    angles_plot = angles + angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("white")

    # 背景同心圆
    for r_val in [0.2, 0.4, 0.6, 0.8, 1.0]:
        ax.plot(np.linspace(0, 2 * np.pi, 100), [r_val] * 100,
                color="#E8ECF0", linewidth=0.5, zorder=1)

    # 外层辉光
    ax.fill(angles_plot, values_plot, color=COLORS.SECONDARY, alpha=0.12, zorder=2)
    ax.plot(angles_plot, values_plot, color=COLORS.SECONDARY, linewidth=2.5,
            alpha=0.4, zorder=3)
    # 主层
    ax.fill(angles_plot, values_plot, color=_BLUE, alpha=0.18, zorder=4)
    ax.plot(angles_plot, values_plot, color=_BLUE, linewidth=2, zorder=5)
    # 节点
    ax.scatter(angles, values, color=_BLUE, s=50, zorder=6,
               edgecolors="white", linewidth=1.5)
    # 数值标注
    for angle, val, label in zip(angles, values, labels):
        ax.annotate(f"{val:.0%}", xy=(angle, val),
                    textcoords="offset points", xytext=(6, 6),
                    fontsize=8, color=_BLUE, fontweight="bold")

    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=11, fontweight="bold", color="#1F2328")
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=7, color="#AAAAAA")
    ax.set_title("策略综合评分雷达", fontsize=14, fontweight="bold", pad=25, color="#1F2328")
    ax.spines["polar"].set_visible(False)
    return _save(fig, f"{d}/radar.png")


# ============================================================
# 7. 滚动夏普（三段色温 + 净值参照）
# ============================================================
def _chart_rolling_sharpe(r: AnalysisResult, d: str) -> str:
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 9), height_ratios=[2, 1, 1],
                                         gridspec_kw={"hspace": 0.3})

    # 滚动夏普走势 - 使用差异化线型
    if r.rolling_sharpe_20 is not None and len(r.rolling_sharpe_20) > 0:
        ax1.plot(r.rolling_sharpe_20.index, r.rolling_sharpe_20.values,
                 alpha=0.3, linewidth=0.6, color="#E09F3E", label="20日", linestyle="-")
    if r.rolling_sharpe_60 is not None and len(r.rolling_sharpe_60) > 0:
        ax1.plot(r.rolling_sharpe_60.index, r.rolling_sharpe_60.values,
                 linewidth=1.0, color=COLORS.SECONDARY, label="60日", linestyle="-")
    if r.rolling_sharpe_120 is not None and len(r.rolling_sharpe_120) > 0:
        ax1.plot(r.rolling_sharpe_120.index, r.rolling_sharpe_120.values,
                 linewidth=1.8, color=_BLUE, label="120日", linestyle="-")
    ax1.axhline(0, color="#D1D9E0", linewidth=0.6)
    ax1.axhline(r.core.sharpe_ratio, color=_RED, linewidth=1, linestyle="--",
                label=f"全期 Sharpe = {r.core.sharpe_ratio:.2f}")
    # Sharpe > 1 区域高亮
    ax1.axhspan(1.0, ax1.get_ylim()[1] if ax1.get_ylim()[1] > 1 else 2.0,
                alpha=0.04, color=_GREEN, zorder=0)
    _title_bar(ax1, "滚动夏普比率走势（20 / 60 / 120日）")
    ax1.legend(fontsize=8, loc="upper left", ncol=2)
    ax1.set_ylabel("Sharpe 比率")
    _style_axis(ax1)

    # 120日色温图 - 使用渐变色条
    if r.rolling_sharpe_120 is not None and len(r.rolling_sharpe_120) > 0:
        rs120 = r.rolling_sharpe_120
        colors_bar = []
        for v in rs120.values:
            if v > 1.5:
                colors_bar.append("#1B5E20")
            elif v > 1:
                colors_bar.append(_GREEN)
            elif v > 0.5:
                colors_bar.append("#8AC926")
            elif v > 0:
                colors_bar.append("#E09F3E")
            elif v > -0.5:
                colors_bar.append("#F4A261")
            else:
                colors_bar.append(_RED)
        ax2.bar(rs120.index, np.ones(len(rs120)), width=3, color=colors_bar, alpha=0.85)
        _subtitle(ax2, "120日滚动 Sharpe 色温图")
        ax2.set_yticks([])
        for spine in ax2.spines.values():
            spine.set_visible(False)

    # 净值参照
    nav = r.data.nav
    ax3.fill_between(nav["日期"], nav["净值"].min() * 0.99, nav["净值"],
                     alpha=0.08, color=COLORS.SECONDARY)
    ax3.plot(nav["日期"], nav["净值"], color=COLORS.SECONDARY, linewidth=1)
    _subtitle(ax3, "净值参照")
    ax3.set_ylabel("净值")
    _style_axis(ax3)

    fig.autofmt_xdate(rotation=30)
    return _save(fig, f"{d}/rolling_sharpe.png")


# ============================================================
# 8. 每万元每日收益（柱+均线+累计面积）
# ============================================================
def _chart_per_10k(r: AnalysisResult, d: str) -> str:
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 9), height_ratios=[1.2, 1, 1],
                                         gridspec_kw={"hspace": 0.3})
    per10k = r.per_10k_daily
    dates = r.data.nav["日期"].iloc[1:]
    if len(dates) > len(per10k):
        dates = dates[:len(per10k)]
    elif len(per10k) > len(dates):
        per10k = per10k[:len(dates)]

    colors = [_GREEN if v >= 0 else _RED for v in per10k.values]
    ax1.bar(dates, per10k.values, width=2, color=colors, alpha=0.4, edgecolor="none")
    ma20 = pd.Series(per10k.values).rolling(20).mean()
    ma60 = pd.Series(per10k.values).rolling(60).mean()
    ax1.plot(dates, ma20.values, color="#E09F3E", linewidth=1.2, label="20日均线", zorder=4)
    ax1.plot(dates, ma60.values, color=_BLUE, linewidth=1.5, label="60日均线", zorder=5)
    avg_val = per10k.mean()
    ax1.axhline(avg_val, color=_RED, linewidth=0.8, linestyle="--",
                label=f"全期均值 = {avg_val:.1f} 元/万")
    _title_bar(ax1, "每万元每日收益率")
    ax1.set_ylabel("元/万")
    ax1.legend(fontsize=8, loc="upper right")
    _style_axis(ax1)

    # 60日滚动年化 - 渐变填充
    ann_factor = pd.Series(per10k.values).rolling(60).mean() * 252
    ax2.plot(dates, ann_factor.values, color=COLORS.SECONDARY, linewidth=1.2)
    ax2.fill_between(dates, 0, ann_factor.values, where=ann_factor.values >= 0,
                     alpha=0.1, color=_GREEN, interpolate=True)
    ax2.fill_between(dates, 0, ann_factor.values, where=ann_factor.values < 0,
                     alpha=0.1, color=_RED, interpolate=True)
    ax2.axhline(0, color="#D1D9E0", linewidth=0.6)
    _subtitle(ax2, "60日滚动年化收益率（每万元）")
    ax2.set_ylabel("元/万/年")
    _style_axis(ax2)

    # 累计 - 面积图渐变
    cum_per10k = pd.Series(per10k.values).cumsum()
    ax3.fill_between(dates, 0, cum_per10k.values, alpha=0.15, color=_BLUE)
    ax3.plot(dates, cum_per10k.values, color=_BLUE, linewidth=1.5)
    final_val = cum_per10k.iloc[-1]
    ax3.annotate(f"累计 {final_val:.0f} 元/万",
                 xy=(dates.iloc[-1], final_val),
                 fontsize=10, fontweight="bold", color=_BLUE,
                 xytext=(-80, 10), textcoords="offset points",
                 arrowprops=dict(arrowstyle="->", color=_BLUE, lw=1.2))
    _subtitle(ax3, "累计每万元收益")
    ax3.set_ylabel("元/万")
    _style_axis(ax3)

    fig.autofmt_xdate(rotation=30)
    return _save(fig, f"{d}/per_10k.png")


# ============================================================
# 9. 回撤风险分级图（多级渐变 + 标注）
# ============================================================
def _chart_drawdown_risk(r: AnalysisResult, d: str) -> str:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[1.5, 1],
                                    gridspec_kw={"hspace": 0.3})

    dd = r.drawdown_series
    dd_vals = dd.values * 100

    # 分级着色 - 使用更柔和的配色
    level_config = [
        (0, -5, "#4CAF50", "安全区 (0~-5%)"),
        (-5, -10, "#FFC107", "注意区 (-5~-10%)"),
        (-10, -15, "#FF9800", "重视区 (-10~-15%)"),
        (-15, -18, "#F44336", "警惕区 (-15~-18%)"),
        (-18, -999, "#B71C1C", "高危区 (<-18%)"),
    ]
    for upper, lower, color, label in level_config:
        mask = np.where((dd_vals <= upper) & (dd_vals > lower), dd_vals, np.nan)
        ax1.fill_between(dd.index, mask, 0, alpha=0.55, color=color, label=label)

    min_dd = dd.min()
    min_dd_date = dd.idxmin()
    ax1.annotate(f"最大回撤\n{min_dd:.2%}", xy=(min_dd_date, min_dd * 100),
                fontsize=9, fontweight="bold", color="#B71C1C",
                xytext=(40, -15), textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color="#B71C1C", lw=1.2),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor="#B71C1C", alpha=0.9))

    _title_bar(ax1, "净值回撤走势与风险分级", _RED)
    ax1.set_ylabel("回撤幅度 (%)")
    ax1.legend(fontsize=7, loc="lower left", ncol=3, framealpha=0.9)
    _style_axis(ax1)

    # 回撤分布直方图 - 更精致的样式
    dd_pct = dd.values * 100
    dd_pct = dd_pct[dd_pct < 0]
    if len(dd_pct) > 0:
        bins = np.arange(int(min(dd_pct)) - 1, 1, 1)
        ax2.hist(dd_pct, bins=bins, color=COLORS.SECONDARY, alpha=0.7,
                 edgecolor="white", linewidth=0.5, rwidth=0.85)
        # 分级线 + 标签
        for threshold, color, label in [(-5, "#FFC107", "-5%"), (-10, "#FF9800", "-10%"),
                                         (-15, "#F44336", "-15%"), (-18, "#B71C1C", "-18%")]:
            ax2.axvline(threshold, color=color, linewidth=1.2, linestyle="--", alpha=0.8)
            ax2.text(threshold, ax2.get_ylim()[1] * 0.9, label,
                    fontsize=7, color=color, ha="center",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                              edgecolor=color, alpha=0.8))
    _subtitle(ax2, "回撤幅度分布统计")
    ax2.set_xlabel("回撤幅度 (%)")
    ax2.set_ylabel("天数")
    _style_axis(ax2)

    fig.autofmt_xdate(rotation=30)
    return _save(fig, f"{d}/drawdown_risk.png")


# ============================================================
# 10. 收益率分布（直方图 + KDE 密度曲线）
# ============================================================
def _chart_return_distribution(r: AnalysisResult, d: str) -> str:
    fig, ax = plt.subplots(figsize=(10, 5))
    daily_ret = r.data.nav["日收益率"].dropna() * 100

    # 直方图 + KDE
    n, bins_arr, patches = ax.hist(daily_ret, bins=80, color=COLORS.SECONDARY, alpha=0.55,
                                    edgecolor="white", linewidth=0.3, density=True)
    # 为柱子着色：负收益红色，正收益蓝色
    for patch, left_edge in zip(patches, bins_arr[:-1]):
        if left_edge < 0:
            patch.set_facecolor("#E57373")
            patch.set_alpha(0.55)

    # KDE 密度曲线
    try:
        from scipy.stats import gaussian_kde
        kde_x = np.linspace(daily_ret.min(), daily_ret.max(), 200)
        kde = gaussian_kde(daily_ret)
        ax.plot(kde_x, kde(kde_x), color=_BLUE, linewidth=2, zorder=5, label="密度曲线")
    except ImportError:
        pass

    mean_val = daily_ret.mean()
    ax.axvline(mean_val, color=_RED, linewidth=1.5, linestyle="--",
              label=f"均值 {mean_val:.3f}%", zorder=4)
    ax.axvline(0, color="#D1D9E0", linewidth=0.8)

    # 标注正负比例
    pos_pct = (daily_ret > 0).sum() / len(daily_ret) * 100
    neg_pct = (daily_ret < 0).sum() / len(daily_ret) * 100
    ax.text(0.98, 0.95, f"正收益 {pos_pct:.1f}%\n负收益 {neg_pct:.1f}%",
            transform=ax.transAxes, fontsize=9, va="top", ha="right",
            bbox=dict(boxstyle="round,pad=0.4", facecolor=_LIGHT_BG,
                      edgecolor=_BORDER, alpha=0.9))

    _title_bar(ax, "日收益率分布")
    ax.set_xlabel("日收益率 (%)")
    ax.set_ylabel("概率密度")
    ax.legend(fontsize=9, loc="upper left")
    _style_axis(ax)
    return _save(fig, f"{d}/return_distribution.png")


# ============================================================
# 11. 品种收益 TOP N（水平条形图，渐变色）
# ============================================================
def _chart_variety_top(r: AnalysisResult, d: str) -> str:
    vms = r.variety_metrics
    top10 = vms[:10]
    bottom10 = vms[-10:]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6),
                                    gridspec_kw={"wspace": 0.4})

    # 盈利 TOP 10 - 绿色渐变
    names = [v.name for v in top10]
    rets = [v.cumulative_return * 100 for v in top10]
    green_shades = [f"#{int(0x1A + (0xA5 - 0x1A) * i / 9):02x}"
                    f"{int(0x7F + (0xD5 - 0x7F) * i / 9):02x}"
                    f"{int(0x37 + (0x80 - 0x37) * i / 9):02x}"
                    for i in range(10)]
    bars1 = ax1.barh(names[::-1], rets[::-1], color=green_shades, alpha=0.85,
                     height=0.6, edgecolor="white", linewidth=0.5)
    for i, v in enumerate(rets[::-1]):
        ax1.text(v + 0.5, i, f"{v:+.1f}%", va="center", fontsize=9, fontweight="bold",
                 color=_GREEN)
    _title_bar(ax1, "盈利 TOP 10 品种", _GREEN)
    ax1.set_xlabel("累计收益率 (%)")
    _style_axis(ax1, grid_axis="x")

    # 亏损 TOP 10 - 红色渐变
    names = [v.name for v in bottom10]
    rets = [v.cumulative_return * 100 for v in bottom10]
    red_shades = [f"#{int(0xCF - (0xCF - 0x9B) * i / 9):02x}"
                  f"{int(0x22 + (0x6A - 0x22) * i / 9):02x}"
                  f"{int(0x2E + (0x5E - 0x2E) * i / 9):02x}"
                  for i in range(10)]
    bars2 = ax2.barh(names[::-1], rets[::-1], color=red_shades, alpha=0.85,
                     height=0.6, edgecolor="white", linewidth=0.5)
    for i, v in enumerate(rets[::-1]):
        ax2.text(v - 1.5, i, f"{v:+.1f}%", va="center", fontsize=9, fontweight="bold",
                 color=_RED)
    _title_bar(ax2, "亏损 TOP 10 品种", _RED)
    ax2.set_xlabel("累计收益率 (%)")
    _style_axis(ax2, grid_axis="x")

    fig.tight_layout(pad=3)
    return _save(fig, f"{d}/variety_top.png")


# ============================================================
# 12. 板块分析（板块盈亏柱图 + 胜率-夏普散点气泡图）
# ============================================================
def _chart_sector(r: AnalysisResult, d: str) -> str:
    sms = r.sector_metrics
    n_sectors = len(sms)
    # 按收益排序
    sms_sorted = sorted(sms, key=lambda s: s.total_return, reverse=True)

    fig_w = max(14, n_sectors * 0.9 + 6)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(fig_w, 10),
                                    gridspec_kw={"hspace": 0.4})

    # --- 上图：板块盈亏柱状图（竖直柱，匹配参考图样式）---
    names = [s.name for s in sms_sorted]
    rets = [s.total_return * 100 for s in sms_sorted]
    palette = SECTOR_PALETTE[:n_sectors]
    bar_colors = []
    for v in rets:
        if v > 0:
            bar_colors.append(_RED)   # 中国金融习惯：红涨
        else:
            bar_colors.append(_GREEN)  # 绿跌

    x_pos = np.arange(n_sectors)
    bars = ax1.bar(x_pos, rets, color=bar_colors, alpha=0.82, width=0.65,
                   edgecolor="white", linewidth=0.5)
    # 数值标签
    for bar, val in zip(bars, rets):
        y_offset = 1.2 if val >= 0 else -2.5
        ax1.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + y_offset,
                 f"{val:+.1f}%", ha="center", fontsize=8, fontweight="bold",
                 color=bar.get_facecolor())
    ax1.axhline(0, color="#D1D9E0", linewidth=0.6)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(names, fontsize=9, rotation=30, ha="right")
    ax1.set_ylabel("盈亏 (%)")
    _title_bar(ax1, "板块盈亏", _ACCENT)
    _style_axis(ax1, grid_axis="y")

    # 板块数量统计
    profit_count = sum(1 for v in rets if v > 0)
    loss_count = sum(1 for v in rets if v <= 0)
    best = sms_sorted[0]
    worst = sms_sorted[-1]
    summary_text = (f"盈利板块 {profit_count} 个，其中{best.name}盈利最多；"
                    f"亏损板块 {loss_count} 个，其中{worst.name}亏损最多。")
    ax1.text(0.5, -0.22, summary_text, transform=ax1.transAxes,
             fontsize=9, ha="center", color="#57606A",
             bbox=dict(boxstyle="round,pad=0.5", facecolor=_LIGHT_BG,
                       edgecolor=_BORDER, alpha=0.9))

    # --- 下图：胜率 vs 夏普散点气泡图（气泡大小=品种数）---
    win_rates = [s.avg_win_rate * 100 for s in sms]
    sharpes = [s.avg_sharpe for s in sms]
    sizes = [len(s.varieties) * 30 + 50 for s in sms]

    scatter = ax2.scatter(win_rates, sharpes, s=sizes, c=rets, cmap="RdYlGn",
                          edgecolors="white", linewidth=1.2, alpha=0.85, zorder=3)
    for i, s in enumerate(sms):
        ax2.annotate(s.name, (win_rates[i], sharpes[i]),
                    textcoords="offset points", xytext=(8, 5), fontsize=8,
                    fontweight="bold", color="#1F2328")
    ax2.axhline(0, color="#D1D9E0", linewidth=0.6, linestyle="--")
    ax2.axvline(50, color="#D1D9E0", linewidth=0.6, linestyle="--")

    # 象限标签
    xlim = ax2.get_xlim()
    ylim = ax2.get_ylim()
    quadrant_labels = [
        (0.75, 0.92, "高胜率 + 高夏普", _GREEN),
        (0.08, 0.92, "低胜率 + 高夏普", "#E09F3E"),
        (0.75, 0.05, "高胜率 + 低夏普", "#E09F3E"),
        (0.08, 0.05, "低胜率 + 低夏普", _RED),
    ]
    for x, y, label, color in quadrant_labels:
        ax2.text(x, y, label, transform=ax2.transAxes, fontsize=7,
                 color=color, alpha=0.6, fontstyle="italic")

    _title_bar(ax2, "板块胜率 vs 夏普比率", COLORS.SECONDARY)
    ax2.set_xlabel("胜率 (%)")
    ax2.set_ylabel("夏普比率")
    _style_axis(ax2)
    cbar = plt.colorbar(scatter, ax=ax2, shrink=0.8, pad=0.02)
    cbar.set_label("累计收益 (%)", fontsize=9)
    cbar.outline.set_linewidth(0.5)

    fig.tight_layout(pad=3)
    return _save(fig, f"{d}/sector_bar.png")
