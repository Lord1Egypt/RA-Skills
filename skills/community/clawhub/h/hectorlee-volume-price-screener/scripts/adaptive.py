#!/usr/bin/env python3
"""
V2 参数自适应模块 - 市场波动率驱动的动态阈值
==============================================
核心思路：放量倍数、振幅阈值不应是固定值，而应随市场状态自适应。

- 市场活跃期（波动率大）：放宽振幅阈值，收紧放量倍数（防噪声）
- 市场低迷期（波动率小）：收紧振幅阈值，放宽放量倍数（捕捉稀缺放量）

基准变量：全市场近20日平均振幅（或指数20日振幅）。
"""

from typing import Dict, Any, Optional


def market_volatility(klines: list) -> Optional[float]:
    """计算市场波动率：近20日平均单日振幅(%)

    输入: klines - 指数或全市场代表序列 [{date,open,close,high,low,volume},...]
    输出: 平均振幅(%)，数据不足返回 None
    """
    if not klines or len(klines) < 5:
        return None
    recent = klines[-20:] if len(klines) >= 20 else klines
    amps = []
    for k in recent:
        low = k.get("low") or 0
        if low <= 0:
            continue
        amps.append((k.get("high", 0) - low) / low * 100.0)
    if not amps:
        return None
    return sum(amps) / len(amps)


def adaptive_params(base_params: Dict[str, Any], vol: float) -> Dict[str, Any]:
    """根据市场波动率生成自适应参数

    vol: 市场近20日平均振幅(%)，典型区间 2%~6%

    调节逻辑（相对 DEFAULT_PARAMS）:
      - vol 高（>4.5%）→ 市场活跃:
          amp_max 上调（允许更大横盘）,
          vol_ratio_min 上调（过滤噪声放量）,
          rise_pct 不变
      - vol 低（<3.0%）→ 市场低迷:
          amp_max 下调（横盘更严格）,
          vol_ratio_min 下调（稀缺放量也算）,
      - 其他 → 接近默认
    """
    p = dict(base_params)
    if vol is None:
        return p  # 无数据时用默认

    # 振幅阈值：以 4.0% 为基准，波动率 ±2% 对应阈值 ∓2%
    base_amp = float(p.get("amp_max", 10.0))
    amp_adj = (vol - 4.0) * 0.8          # vol=6 → +1.6；vol=2 → -1.6
    p["amp_max"] = round(max(6.0, min(15.0, base_amp + amp_adj)), 1)

    # 放量倍数：波动率高→门槛高；低→门槛低
    base_vr = float(p.get("vol_ratio_min", 1.5))
    vr_adj = (vol - 4.0) * 0.15          # vol=6 → +0.3；vol=2 → -0.3
    p["vol_ratio_min"] = round(max(1.2, min(2.5, base_vr + vr_adj)), 2)

    # 缩量天数：低迷期要求更长的缩量确认（防假缩量）
    base_sd = int(p.get("shrink_min_days", 2))
    if vol < 3.0:
        p["shrink_min_days"] = max(2, base_sd + 1)
    else:
        p["shrink_min_days"] = base_sd

    # 记录自适应标记
    p["_adaptive"] = True
    p["_market_vol"] = round(vol, 2)
    return p


def describe(vol: float) -> str:
    """市场状态描述"""
    if vol is None:
        return "未知"
    if vol >= 4.5:
        return f"活跃（振幅{vol:.1f}%）"
    if vol >= 3.5:
        return f"平稳（振幅{vol:.1f}%）"
    return f"低迷（振幅{vol:.1f}%）"


if __name__ == "__main__":
    from pattern_detect import DEFAULT_PARAMS
    print("自适应参数示例：")
    for v in (2.5, 3.5, 4.0, 5.0, 6.0):
        p = adaptive_params(DEFAULT_PARAMS, v)
        print(f"  波动率{v:.1f}% → amp_max={p['amp_max']} vol_ratio_min={p['vol_ratio_min']} "
              f"shrink_min_days={p['shrink_min_days']} ({describe(v)})")
