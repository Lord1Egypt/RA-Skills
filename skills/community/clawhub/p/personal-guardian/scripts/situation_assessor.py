# -*- coding: utf-8 -*-
import sys as _sys
if _sys.platform == "win32":
    try:
        _sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        _sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

"""
personal-rescue-agent
个人终端应急救援智能体
=====================
situation_assessor.py — 态势评估与风险定级引擎

支持两种模式：
  --simulate : 模拟评估（无需真实设备）
  --assess   : 真实评估（需设备数据接口）
"""

import argparse
import json
import sys
import os
from datetime import datetime
from typing import Optional

# ============================================================
# 风险常量
# ============================================================

RISK_LEVELS = {
    "L1": {
        "name": "警觉",
        "score_range": (0, 20),
        "behavior": "确认需求 → 联系指定联系人",
        "time_window_seconds": 60,
    },
    "L2": {
        "name": "关注",
        "score_range": (20, 40),
        "behavior": "询问确认 → 超时无应答升级L3",
        "time_window_seconds": 60,
    },
    "L3": {
        "name": "紧急",
        "score_range": (40, 65),
        "behavior": "开始录音+定位+紧急联系人通知",
        "time_window_seconds": 0,  # 即时执行
    },
    "L4": {
        "name": "危机",
        "score_range": (65, 85),
        "behavior": "立即呼叫120+110+紧急联系人+周边广播",
        "time_window_seconds": 0,
    },
    "L5": {
        "name": "灾难",
        "score_range": (85, 100),
        "behavior": "全饱和广播：急救+警方+联系人+社交网络+周边",
        "time_window_seconds": 0,
    },
}

# 风险因子权重
WEIGHTS = {
    "user_responsive": 0.20,
    "time_risk": 0.15,
    "location_risk": 0.20,
    "physiological_risk": 0.25,
    "environmental_risk": 0.10,
    "device_status_risk": 0.10,
}

# 场景权重因子
SCENARIO_WEIGHTS = {
    "fall": {"physiological": 0.40, "location": 0.20, "time": 0.15, "environmental": 0.25},
    "lost": {"location": 0.35, "time": 0.25, "physiological": 0.15, "environmental": 0.25},
    "threat": {"environmental": 0.35, "time": 0.20, "location": 0.25, "physiological": 0.20},
    "unknown": {"physiological": 0.25, "location": 0.25, "time": 0.25, "environmental": 0.25},
}

# ============================================================
# 评分函数
# ============================================================

def score_user_responsive(responsive: bool, consecutive_no_response: int = 0) -> float:
    """用户响应性评分"""
    if responsive:
        return 0.0
    # 无应答次数越多，风险越高
    base = 50.0
    penalty = min(consecutive_no_response * 15, 50)
    return min(base + penalty, 100.0)


def score_time_risk(hour: int, is_night: bool = None) -> float:
    """时间风险评分"""
    if is_night is None:
        is_night = hour < 6 or hour > 22

    if is_night:
        return 85.0  # 深夜高风险
    elif 22 <= hour <= 23 or 0 <= hour <= 1:
        return 60.0  # 深夜边缘
    elif 6 <= hour <= 8 or 20 <= hour <= 22:
        return 30.0  # 早晚通勤
    else:
        return 10.0  # 白天正常时段


def score_location_risk(location_type: str, is_isolated: bool) -> float:
    """位置风险评分"""
    base_scores = {
        "unknown": 70.0,
        "indoor_private": 20.0,
        "outdoor_public": 30.0,
        "outdoor_remote": 80.0,
        "vehicle": 50.0,
        "elevated": 65.0,
        "underground": 75.0,
        "water_area": 85.0,
    }
    base = base_scores.get(location_type, 40.0)
    if is_isolated:
        base = min(base + 15, 100.0)
    return base


def score_physiological_risk(
    heart_rate: Optional[int] = None,
    fall_detected: bool = False,
    irregular_pulse: bool = False,
) -> float:
    """生理信号风险评分"""
    score = 0.0

    # 摔倒检测（高权重）
    if fall_detected:
        score += 70.0

    # 心率异常
    if heart_rate is not None:
        if heart_rate < 40:  # 心动过缓
            score += 60.0
        elif heart_rate > 150:  # 心动过速
            score += 50.0
        elif heart_rate > 120:
            score += 30.0

    # 心律不齐
    if irregular_pulse:
        score += 40.0

    return min(score, 100.0)


def score_environmental_risk(
    temperature: Optional[float] = None,
    weather: str = "clear",
    is_confined: bool = False,
    crowd_density: str = "medium",
) -> float:
    """环境风险评分"""
    score = 0.0

    # 天气
    weather_scores = {
        "clear": 5.0,
        "cloudy": 10.0,
        "rain": 30.0,
        "storm": 60.0,
        "snow": 50.0,
        "fog": 40.0,
        "extreme_heat": 55.0,
        "extreme_cold": 65.0,
    }
    score += weather_scores.get(weather, 10.0)

    # 极端温度
    if temperature is not None:
        if temperature < 0:
            score += 30.0
        elif temperature > 38:
            score += 25.0

    # 密闭空间
    if is_confined:
        score += 15.0

    # 人群密度
    density_scores = {"none": 5.0, "low": 10.0, "medium": 20.0, "high": 30.0}
    score += density_scores.get(crowd_density, 15.0)

    return min(score, 100.0)


def score_device_status(battery_level: int, network_status: str, sensors_available: list) -> float:
    """设备状态风险评分"""
    score = 0.0

    # 电量
    if battery_level < 5:
        score += 50.0
    elif battery_level < 20:
        score += 25.0
    elif battery_level < 50:
        score += 10.0

    # 网络
    network_scores = {"offline": 60.0, "poor": 30.0, "normal": 5.0, "good": 0.0}
    score += network_scores.get(network_status, 20.0)

    # 传感器可用性
    critical_sensors = ["gps", "microphone"]
    missing_critical = [s for s in critical_sensors if s not in sensors_available]
    score += len(missing_critical) * 20

    return min(score, 100.0)


def calculate_overall_score(
    scenario: str,
    user_responsive: bool,
    consecutive_no_response: int,
    hour: int,
    location_type: str,
    is_isolated: bool,
    heart_rate: Optional[int],
    fall_detected: bool,
    irregular_pulse: bool,
    temperature: Optional[float],
    weather: str,
    is_confined: bool,
    crowd_density: str,
    battery_level: int,
    network_status: str,
    sensors_available: list,
) -> dict:
    """综合评分计算"""

    # 各项评分
    user_score = score_user_responsive(user_responsive, consecutive_no_response)
    time_score = score_time_risk(hour)
    location_score = score_location_risk(location_type, is_isolated)
    physio_score = score_physiological_risk(heart_rate, fall_detected, irregular_pulse)
    env_score = score_environmental_risk(temperature, weather, is_confined, crowd_density)
    device_score = score_device_status(battery_level, network_status, sensors_available)

    # 使用场景权重
    weights = SCENARIO_WEIGHTS.get(scenario, SCENARIO_WEIGHTS["unknown"])

    # 综合得分（使用场景权重）
    total_score = (
        user_score * weights["physiological"] +
        time_score * weights["time"] +
        location_score * weights["location"] +
        physio_score * weights["physiological"] +
        env_score * weights["environmental"] +
        device_score * 0.10  # 设备状态固定权重
    )

    # 确定等级
    assigned_level = "L1"
    for level, info in RISK_LEVELS.items():
        lo, hi = info["score_range"]
        if lo <= total_score < hi:
            assigned_level = level
            break
    if total_score >= 85:
        assigned_level = "L5"

    return {
        "total_score": round(total_score, 1),
        "level": assigned_level,
        "breakdown": {
            "user_responsive_score": round(user_score, 1),
            "time_risk_score": round(time_score, 1),
            "location_risk_score": round(location_score, 1),
            "physiological_risk_score": round(physio_score, 1),
            "environmental_risk_score": round(env_score, 1),
            "device_status_score": round(device_score, 1),
        },
        "weights_used": weights,
    }


def assess_situation(input_data: dict, scenario: str = "unknown") -> dict:
    """主评估函数"""
    result = calculate_overall_score(
        scenario=scenario,
        user_responsive=input_data.get("user_responsive", True),
        consecutive_no_response=input_data.get("consecutive_no_response", 0),
        hour=input_data.get("hour", datetime.now().hour),
        location_type=input_data.get("location_type", "unknown"),
        is_isolated=input_data.get("is_isolated", False),
        heart_rate=input_data.get("heart_rate"),
        fall_detected=input_data.get("fall_detected", False),
        irregular_pulse=input_data.get("irregular_pulse", False),
        temperature=input_data.get("temperature"),
        weather=input_data.get("weather", "clear"),
        is_confined=input_data.get("is_confined", False),
        crowd_density=input_data.get("crowd_density", "medium"),
        battery_level=input_data.get("battery_level", 100),
        network_status=input_data.get("network_status", "good"),
        sensors_available=input_data.get("sensors_available", ["gps", "microphone"]),
    )

    level_info = RISK_LEVELS[result["level"]]

    return {
        "safe_moment_id": f"SM-{datetime.now().strftime('%Y%m%d')}-{hash(str(input_data)) % 10000:04d}",
        "scenario": scenario,
        "assessment": {
            "current_level": result["level"],
            "level_name": level_info["name"],
            "total_risk_score": result["total_score"],
            "score_breakdown": result["breakdown"],
            "agent_behavior": level_info["behavior"],
            "time_window_seconds": level_info["time_window_seconds"],
        },
        "trigger": input_data.get("trigger", "manual"),
        "timestamp": datetime.now().isoformat(),
    }


def simulate_scenario(scenario_name: str) -> dict:
    """预置场景模拟"""
    scenarios = {
        "fall": {
            "scenario": "fall",
            "description": "用户摔倒检测 + 无应答",
            "input": {
                "trigger": "device_signal:fall_detected",
                "user_responsive": False,
                "consecutive_no_response": 3,
                "hour": 22,
                "location_type": "indoor_private",
                "is_isolated": True,
                "heart_rate": 55,  # 偏低，可能失去意识
                "fall_detected": True,
                "irregular_pulse": False,
                "temperature": 22,
                "weather": "clear",
                "is_confined": False,
                "crowd_density": "low",
                "battery_level": 35,
                "network_status": "good",
                "sensors_available": ["gps", "microphone", "accelerometer"],
            },
        },
        "lost": {
            "scenario": "lost",
            "description": "用户迷路 + 超时无应答",
            "input": {
                "trigger": "ai_predicted:route_deviation",
                "user_responsive": False,
                "consecutive_no_response": 2,
                "hour": 15,
                "location_type": "outdoor_remote",
                "is_isolated": True,
                "heart_rate": 88,
                "fall_detected": False,
                "irregular_pulse": False,
                "temperature": 8,
                "weather": "fog",
                "is_confined": False,
                "crowd_density": "none",
                "battery_level": 18,  # 低电量警告
                "network_status": "poor",  # 信号差
                "sensors_available": ["gps", "microphone"],
            },
        },
        "threat": {
            "scenario": "threat",
            "description": "人身安全威胁 + 手动激活",
            "input": {
                "trigger": "user_activated:safe_moment",
                "user_responsive": False,
                "consecutive_no_response": 1,
                "hour": 23,
                "location_type": "outdoor_remote",
                "is_isolated": True,
                "heart_rate": 165,  # 惊恐心率
                "fall_detected": False,
                "irregular_pulse": False,
                "temperature": 18,
                "weather": "clear",
                "is_confined": False,
                "crowd_density": "none",
                "battery_level": 62,
                "network_status": "normal",
                "sensors_available": ["gps", "microphone"],
            },
        },
        "false_alarm": {
            "scenario": "fall",
            "description": "误报：用户正常但手表误判",
            "input": {
                "trigger": "device_signal:fall_detected",
                "user_responsive": True,
                "consecutive_no_response": 0,
                "hour": 14,
                "location_type": "indoor_private",
                "is_isolated": False,
                "heart_rate": 72,
                "fall_detected": True,  # 误判
                "irregular_pulse": False,
                "temperature": 24,
                "weather": "clear",
                "is_confined": False,
                "crowd_density": "medium",
                "battery_level": 80,
                "network_status": "good",
                "sensors_available": ["gps", "microphone", "accelerometer"],
            },
        },
    }

    if scenario_name not in scenarios:
        available = ", ".join(scenarios.keys())
        print(f"未知场景。可用场景: {available}")
        sys.exit(1)

    s = scenarios[scenario_name]
    print(f"\n{'='*60}")
    print(f"  场景模拟: {s['description']}")
    print(f"{'='*60}\n")

    result = assess_situation(s["input"], scenario=s["scenario"])

    # 格式化输出
    print(f"🆔 安全时刻ID: {result['safe_moment_id']}")
    print(f"⏰ 时间戳: {result['timestamp']}")
    print(f"\n📊 风险评估结果:")
    print(f"   等级: {result['assessment']['current_level']} - {result['assessment']['level_name']}")
    print(f"   综合风险评分: {result['assessment']['total_risk_score']} / 100")
    print(f"\n📋 评分明细:")
    for key, val in result["assessment"]["score_breakdown"].items():
        bar = "█" * int(val / 10) + "░" * (10 - int(val / 10))
        print(f"   {key:30s} [{bar}] {val}")

    print(f"\n🚨 Agent 行动建议:")
    print(f"   {result['assessment']['agent_behavior']}")
    print(f"   时限: {result['assessment']['time_window_seconds']}秒")

    return result


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="personal-rescue-agent — 态势评估与风险定级引擎"
    )
    parser.add_argument(
        "--simulate",
        choices=["fall", "lost", "threat", "false_alarm"],
        help="运行预置场景模拟",
    )
    parser.add_argument(
        "--assess",
        action="store_true",
        help="从标准输入读取数据进行评估",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="JSON 格式化输出",
    )

    args = parser.parse_args()

    if args.simulate:
        result = simulate_scenario(args.simulate)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.assess:
        # 从 stdin 读取 JSON 数据
        data = json.load(sys.stdin)
        result = assess_situation(data)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🆔 {result['safe_moment_id']} | {result['assessment']['current_level']} | 评分: {result['assessment']['total_risk_score']}")
        return

    # 无参数时显示帮助
    parser.print_help()
    print("\n\n📌 快速示例:")
    print("  python3 scripts/situation_assessor.py --simulate fall")
    print("  python3 scripts/situation_assessor.py --simulate lost")
    print("  python3 scripts/situation_assessor.py --simulate threat")


if __name__ == "__main__":
    main()
