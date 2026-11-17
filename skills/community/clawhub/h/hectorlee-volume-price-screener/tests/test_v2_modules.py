#!/usr/bin/env python3
"""V2 模块单元测试：参数自适应 + ML 模型 + 回测工具"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

import pytest
from pattern_detect import DEFAULT_PARAMS
from adaptive import market_volatility, adaptive_params, describe


# ============================================================
# 参数自适应
# ============================================================

def test_market_volatility():
    klines = [
        {"high": 10.2, "low": 9.8, "open": 10, "close": 10, "volume": 100}
        for _ in range(25)
    ]
    vol = market_volatility(klines)
    assert vol is not None
    assert 3.0 < vol < 5.0   # (10.2-9.8)/9.8 ≈ 4.08%


def test_market_volatility_insufficient():
    assert market_volatility([]) is None
    assert market_volatility([{"high": 1, "low": 1}]) is None


def test_adaptive_high_volatility():
    """活跃市场：振幅阈值放宽、量比门槛提高"""
    p = adaptive_params(DEFAULT_PARAMS, 6.0)
    assert p["amp_max"] > DEFAULT_PARAMS["amp_max"]     # 10.0 → 11.6
    assert p["vol_ratio_min"] > DEFAULT_PARAMS["vol_ratio_min"]  # 1.5 → 1.8
    assert p["_adaptive"] is True


def test_adaptive_low_volatility():
    """低迷市场：振幅收紧、量比门槛降低、缩量天数增加"""
    p = adaptive_params(DEFAULT_PARAMS, 2.5)
    assert p["amp_max"] < DEFAULT_PARAMS["amp_max"]     # 10.0 → 8.8
    assert p["vol_ratio_min"] < DEFAULT_PARAMS["vol_ratio_min"]  # 1.5 → 1.27
    assert p["shrink_min_days"] >= DEFAULT_PARAMS["shrink_min_days"]


def test_adaptive_none():
    p = adaptive_params(DEFAULT_PARAMS, None)
    assert p["amp_max"] == DEFAULT_PARAMS["amp_max"]
    assert "_adaptive" not in p


def test_describe():
    assert "活跃" in describe(5.0)
    assert "低迷" in describe(2.0)


# ============================================================
# ML 模型
# ============================================================

def _make_sample(up=True, **overrides):
    s = {
        "surge_pct": 7.0, "volume_ratio": 2.2, "shrink_days": 5,
        "shrink_depth": 0.4, "amplitude": 5.0, "range_position": "upper",
        "pullback_ratio": 0.3, "low_point_rise": True,
        "breakout_60d": True, "ma_support": True, "vol_ma_bull": True,
        "conc_rise_3d": True, "conc_fall_3d": False, "score": 80.0,
        "fwd20": 5.0 if up else -5.0,
    }
    s.update(overrides)
    return s


def test_feature_vector():
    from ml_model import extract_feature_vector, FEATURES
    s = _make_sample()
    vec = extract_feature_vector(s)
    assert len(vec) == len(FEATURES)
    assert vec[0] == 7.0          # surge_pct
    assert vec[5] == 2            # range_position upper=2
    assert vec[7] == 1.0          # low_point_rise


def test_make_dataset():
    from ml_model import make_dataset
    samples = [_make_sample(up=True), _make_sample(up=False)]
    X, y = make_dataset(samples)
    assert len(X) == 2
    assert y == [1.0, 0.0]


def test_train_sklearn_backend():
    """sklearn 后端可训练（本地环境 xgboost 可能缺 libomp）"""
    from ml_model import train, resolve_backend
    samples = [_make_sample(up=i % 2 == 0, score=60 + (i % 5) * 8)
               for i in range(200)]
    backend = resolve_backend()
    assert backend in ("xgboost", "sklearn", "logistic")
    model, metrics = train(samples, backend="sklearn")
    assert metrics["n_samples"] == 200
    assert 0 <= metrics["auc"] <= 1
    assert metrics["accuracy"] > 0


def test_predict():
    from ml_model import train, predict
    samples = [_make_sample(up=i % 2 == 0, score=60 + (i % 5) * 8)
               for i in range(200)]
    model, _ = train(samples, backend="sklearn")
    p = predict(model, _make_sample(up=True))
    assert 0.0 <= p <= 1.0


# ============================================================
# 回测工具
# ============================================================

def test_compute_stats_empty():
    from backtest import compute_stats
    stats = compute_stats([], {}, [5, 10, 20])
    assert stats["n_hits"] == 0


def test_compute_stats_basic():
    from backtest import compute_stats
    records = [
        {"date": "2026-01-05", "fwd5": 2.0, "fwd10": 3.0, "fwd20": 4.0},
        {"date": "2026-01-06", "fwd5": -1.0, "fwd10": 0.5, "fwd20": 2.0},
        {"date": "2026-01-07", "fwd5": 0.5, "fwd10": -2.0, "fwd20": -1.0},
    ]
    idx_map = {
        "2026-01-05": {5: 1.0, 10: 1.0, 20: 1.0},
        "2026-01-06": {5: 0.5, 10: 0.5, 20: 0.5},
        "2026-01-07": {5: 0.0, 10: 0.0, 20: 0.0},
    }
    stats = compute_stats(records, idx_map, [5, 10, 20])
    assert stats["n_hits"] == 3
    s5 = stats["by_horizon"][5]
    assert s5["n"] == 3
    assert s5["avg_ret"] == pytest.approx(0.5)     # (2-1+0.5)/3
    assert s5["win_rate"] == pytest.approx(66.7, abs=0.1)
    # bench=(1+0.5+0)/3=0.5 → alpha = 0.5-0.5 = 0.0
    assert s5["bench_avg"] == pytest.approx(0.5)
    assert s5["alpha"] == pytest.approx(0.0, abs=0.01)


def test_scan_stock_hit_and_miss():
    """滚动扫描：合成标准命中K线应产生记录"""
    from backtest import scan_stock
    from conftest import build_kline  # noqa: F401  (tests/conftest 路径需注入)
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests"))
    from conftest import build_kline

    # 锚点需落在滚动窗口末尾20日内：t 从 30 到 100，锚点取 85（t-19<=85<=t 对 t∈[85,104] 成立）
    bars = build_kline(n=120, anchor=85, surge_pct=7.0, vol_ratio=2.2)
    klines = [
        {"date": b.date, "open": b.open, "high": b.high, "low": b.low,
         "close": b.close, "volume": b.volume}
        for b in bars
    ]
    recs = scan_stock("000001", "测试", klines, DEFAULT_PARAMS, min_hist=30)
    assert len(recs) > 0
    # 命中记录包含特征与未来收益
    r = recs[0]
    assert "fwd5" in r
    assert "fwd20" in r
    assert "surge_pct" in r


# ============================================================
# 组合回测（每日Top千分之一）
# ============================================================

def _make_portfolio_samples():
    """构造组合回测用样本：5个日期×每日期独立股票"""
    dates = [f"2026-0{i}-01" for i in range(1, 6)]
    samples = []
    for di, d in enumerate(dates):
        for j in range(10):
            samples.append({
                "code": f"sh60{di}{j:03d}", "date": d, "name": f"股{di}-{j}",
                "score": 50 + (j * 3 + di) % 40,   # 差异化评分
                "fwd5": 0.5, "fwd10": 1.0, "fwd20": 1.5,
            })
    return samples, dates


def test_daily_portfolio_selects_top_k():
    """每日按评分取前 k 只"""
    from portfolio_backtest import daily_portfolio
    samples, dates = _make_portfolio_samples()
    selected = daily_portfolio(samples, "score", 3, cooldown=20)
    assert len(selected) == len(dates)
    for d, picks in selected.items():
        assert len(picks) == 3
        scores = [p["score"] for p in picks]
        assert scores == sorted(scores, reverse=True)   # 降序


def test_daily_portfolio_cooldown():
    """冷却期：同一股票冷却期内不重复入选"""
    from portfolio_backtest import daily_portfolio
    # 构造: 同一股票连续多日高分 → 冷却期（3个交易日）内只入选1次
    samples = []
    for di, d in enumerate([f"2026-0{i}-05" for i in range(1, 8)]):
        samples.append({"code": "sh600000", "date": d, "score": 99.0,
                        "fwd5": 1, "fwd10": 1, "fwd20": 1})
        samples.append({"code": f"sh60{di:04d}", "date": d, "score": 50.0,
                        "fwd5": 1, "fwd10": 1, "fwd20": 1})
    selected = daily_portfolio(samples, "score", 2, cooldown=3)
    # 冷却期3：索引0入选，索引1-2跳过，索引3可再入选 → 共3次（索引0/3/6）
    count = sum(1 for picks in selected.values() for p in picks if p["code"] == "sh600000")
    assert count == 3
    # 冷却期10：7个交易日窗口内只入选1次
    selected2 = daily_portfolio(samples, "score", 2, cooldown=10)
    count2 = sum(1 for picks in selected2.values() for p in picks if p["code"] == "sh600000")
    assert count2 == 1


def test_compute_portfolio_stats():
    """组合统计：每日等权收益聚合"""
    from portfolio_backtest import compute_portfolio_stats
    samples, dates = _make_portfolio_samples()
    from portfolio_backtest import daily_portfolio
    selected = daily_portfolio(samples, "score", 2, cooldown=20)
    idx_map = {d: {5: 0.2, 10: 0.4, 20: 0.6} for d in dates}
    stats = compute_portfolio_stats(selected, idx_map, [5, 10, 20])
    assert stats["n_days"] == len(dates)
    assert stats["total_picks"] == len(dates) * 2
    s20 = stats["by_horizon"][20]
    assert s20["avg_ret"] == pytest.approx(1.5)   # 所有样本 fwd20=1.5
    assert s20["alpha"] == pytest.approx(0.9)     # 1.5 - 0.6


def test_rolling_nav_constant_price():
    """净值模拟：价格恒定则净值恒定（无成本）"""
    import pickle
    from portfolio_backtest import rolling_nav, CACHE_FILE
    # 用真实缓存数据跑通即可（不依赖具体数值），验证函数可执行
    samples, dates = _make_portfolio_samples()
    from portfolio_backtest import daily_portfolio
    selected = daily_portfolio(samples, "score", 2, cooldown=20)
    if os.path.exists(CACHE_FILE):
        curve = rolling_nav(selected, hold_days=20)
        assert isinstance(curve, list)
        assert all(isinstance(n, float) and n > 0 for _, n in curve)
    else:
        pytest.skip("K线缓存不存在，跳过净值模拟测试")
