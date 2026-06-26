#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
确认信号系统
增加二次确认，避免假信号
"""

# 确认条件设置
CONFIRMATION_RULES = {
    # 1. 不过热检查：近5日涨幅不能太大
    "not_overheated": {
        "enabled": True,
        "max_gain_5d": 15,  # 5日涨幅不超过15%
        "description": "近5日涨幅不超过15%，避免追高"
    },
    
    # 2. 布林带位置检查：不在上轨
    "boll_not_top": {
        "enabled": True,
        "max_boll_pos": 1.0,  # 布林位置不超过1.0
        "description": "价格不在布林带上轨，留有空间"
    },
    
    # 3. 量能检查：温和放量
    "moderate_volume": {
        "enabled": True,
        "min_vol_ratio": 0.5,  # 量比至少0.5
        "max_vol_ratio": 2.0,  # 量比不超过2.0
        "description": "量比0.5-2.0，温和放量"
    },
    
    # 4. RSI检查：不过热
    "rsi_not_overbought": {
        "enabled": True,
        "max_rsi": 80,  # RSI不超过80
        "description": "RSI不超过80，避免超买"
    },
    
    # 5. MACD柱线检查：不能过大
    "macd_not_too_large": {
        "enabled": True,
        "max_macd_hist": 5,  # MACD柱线不超过5%
        "description": "MACD柱线不超过5%，避免过度强势"
    },
    
    # 6. 趋势确认：MA20持续向上
    "ma20_trending_up": {
        "enabled": True,
        "lookback": 5,  # 过去5天MA20都在上升
        "description": "MA20连续5日上升"
    },
    
    # 7. 缩量回调确认
    "pullback_with_volume": {
        "enabled": False,  # 默认关闭
        "description": "回调时缩量，可能是假摔"
    },
}


def check_confirmation(df, rules=None):
    """
    检查是否满足确认条件
    
    df: 包含技术指标的DataFrame
    返回: {
        "passed": True/False,
        "passed_count": 5/7,
        "total_count": 7,
        "checks": {
            "not_overheated": True,
            "boll_not_top": False,
            ...
        },
        "warnings": ["RSI偏高", ...]
    }
    """
    if rules is None:
        rules = CONFIRMATION_RULES
    
    last = df.iloc[-1]
    prev5 = df.iloc[-6:-1] if len(df) >= 6 else df
    
    result = {
        "passed": True,
        "passed_count": 0,
        "total_count": 0,
        "checks": {},
        "warnings": [],
        "recommendations": []
    }
    
    # 1. 不过热检查
    if rules["not_overheated"]["enabled"]:
        result["total_count"] += 1
        gain_5d = last.get("gain_5d", 0)
        check = gain_5d <= rules["not_overheated"]["max_gain_5d"]
        result["checks"]["not_overheated"] = check
        
        if check:
            result["passed_count"] += 1
        else:
            result["passed"] = False
            result["warnings"].append(f"近5日涨幅{gain_5d:.1f}%过大（>{rules['not_overheated']['max_gain_5d']}%）")
            result["recommendations"].append("等回调后再考虑")
    
    # 2. 布林带位置检查
    if rules["boll_not_top"]["enabled"]:
        result["total_count"] += 1
        boll_pos = last.get("boll_pos", 0)
        check = boll_pos <= rules["boll_not_top"]["max_boll_pos"]
        result["checks"]["boll_not_top"] = check
        
        if check:
            result["passed_count"] += 1
        else:
            result["warnings"].append(f"价格已在布林带上轨")
            result["recommendations"].append("注意回调风险")
    
    # 3. 量能检查
    if rules["moderate_volume"]["enabled"]:
        result["total_count"] += 1
        vol_ratio = last.get("vol_ratio", 1)
        min_v = rules["moderate_volume"]["min_vol_ratio"]
        max_v = rules["moderate_volume"]["max_vol_ratio"]
        check = min_v <= vol_ratio <= max_v
        result["checks"]["moderate_volume"] = check
        
        if check:
            result["passed_count"] += 1
        else:
            if vol_ratio < min_v:
                result["warnings"].append(f"量比{vol_ratio:.1f}偏小")
            else:
                result["warnings"].append(f"量比{vol_ratio:.1f}偏大（放量过度）")
    
    # 4. RSI检查
    if rules["rsi_not_overbought"]["enabled"]:
        result["total_count"] += 1
        rsi = last.get("rsi", 50)
        check = rsi <= rules["rsi_not_overbought"]["max_rsi"]
        result["checks"]["rsi_not_overbought"] = check
        
        if check:
            result["passed_count"] += 1
        else:
            result["warnings"].append(f"RSI({rsi:.0f})偏高，小心回调")
    
    # 5. MACD柱线检查
    if rules["macd_not_too_large"]["enabled"]:
        result["total_count"] += 1
        macd_hist = last.get("hist", 0)
        close = last.get("close", 1)
        macd_pct = abs(macd_hist / close * 100) if close > 0 else 0
        max_macd = rules["macd_not_too_large"]["max_macd_hist"]
        check = macd_pct <= max_macd
        result["checks"]["macd_not_too_large"] = check
        
        if check:
            result["passed_count"] += 1
        else:
            result["warnings"].append(f"MACD柱线{macd_pct:.1f}%过大")
    
    # 6. MA20趋势检查
    if rules["ma20_trending_up"]["enabled"]:
        result["total_count"] += 1
        lookback = rules["ma20_trending_up"]["lookback"]
        
        if len(df) >= lookback + 1:
            ma20_series = df["ma20"].iloc[-(lookback+1):]
            # 检查是否每天都上升
            ma_diffs = ma20_series.diff().dropna()
            check = all(ma_diffs > 0)
        else:
            check = True  # 数据不够，默认通过
        
        result["checks"]["ma20_trending_up"] = check
        
        if check:
            result["passed_count"] += 1
        else:
            result["warnings"].append("MA20上升趋势放缓")
    
    # 计算通过率
    if result["total_count"] > 0:
        result["pass_rate"] = result["passed_count"] / result["total_count"]
        # 通过率80%以上认为是好信号
        if result["pass_rate"] < 0.8:
            result["passed"] = False
    
    return result


def get_confirmation_level(passed_count, total_count, warnings):
    """获取确认等级"""
    if not warnings and passed_count == total_count:
        return "🟢 强确认", "所有条件满足，推荐"
    elif passed_count / total_count >= 0.8 and len(warnings) <= 1:
        return "🟡 中确认", "大部分条件满足，注意风险"
    elif passed_count / total_count >= 0.6:
        return "🟠 弱确认", "部分条件满足，谨慎"
    else:
        return "🔴 未确认", "条件不满足，不推荐"


if __name__ == "__main__":
    print("确认信号系统测试")
    print("=" * 50)
    
    import pandas as pd
    import numpy as np
    
    # 模拟数据
    dates = pd.date_range("2026-03-01", periods=30)
    np.random.seed(42)
    
    df = pd.DataFrame({
        "close": 10 + np.cumsum(np.random.randn(30) * 0.2),
        "volume": np.random.randint(1000000, 5000000, 30),
        "open": 10 + np.cumsum(np.random.randn(30) * 0.2),
        "high": 10 + np.cumsum(np.random.randn(30) * 0.2) + 0.5,
        "low": 10 + np.cumsum(np.random.randn(30) * 0.2) - 0.5,
    })
    
    # 添加指标
    df["ma5"] = df["close"].rolling(5).mean()
    df["ma10"] = df["close"].rolling(10).mean()
    df["ma20"] = df["close"].rolling(20).mean()
    df["rsi"] = 50 + np.random.randn(30) * 20
    df["boll_pos"] = np.random.randn(30) * 0.5
    df["vol_ratio"] = np.random.uniform(0.5, 1.5, 30)
    df["hist"] = np.random.randn(30) * 0.1
    df["gain_5d"] = (df["close"] / df["close"].shift(5) - 1) * 100
    
    # 测试
    result = check_confirmation(df)
    
    print(f"通过: {result['passed_count']}/{result['total_count']}")
    print(f"通过率: {result['pass_rate']*100:.0f}%")
    print()
    
    level, desc = get_confirmation_level(result["passed_count"], result["total_count"], result["warnings"])
    print(f"确认等级: {level}")
    print(f"说明: {desc}")
    print()
    
    if result["warnings"]:
        print("警告:")
        for w in result["warnings"]:
            print(f"  ⚠ {w}")
    
    if result["recommendations"]:
        print("建议:")
        for r in result["recommendations"]:
            print(f"  💡 {r}")
