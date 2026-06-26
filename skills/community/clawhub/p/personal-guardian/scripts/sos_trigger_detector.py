"""
sos_trigger_detector.py — 多源SOS信号检测与融合

整合主动触发、被动生理检测、行为异常检测、远程触发
输出标准化的 TriggerEvent，传入 AutonomousDecisionEngine
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import hashlib


@dataclass
class TriggerEvent:
    """SOS触发事件——决策引擎的输入门票"""
    activated: bool
    trigger_type: str          # manual / biometric / behavioral / remote / compound
    trigger_sources: list      # 触发来源列表
    raw_data: dict             # 原始传感器数据
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    event_id: str = ""

    def __post_init__(self):
        if not self.event_id:
            raw = f"{self.timestamp}{self.trigger_type}"
            self.event_id = hashlib.sha256(raw.encode()).hexdigest()[:12]


class SOSTriggerDetector:
    """
    多源SOS信号检测器

    检测维度：
    1. 主动触发（按键/语音/手势）
    2. 生物特征异常（心率/血氧/跌倒）
    3. 行为异常（静止/签到超时/夜间独行）
    4. 远程触发（授权联系人核验）
    """

    # ── 检测阈值 ──────────────────────────────────────────────────
    FALL_CONFIRM_MOTIONLESS_SEC = 30       # 跌倒后静止30秒确认
    HEART_RATE_MIN = 45                    # 心率下限（低于=危险）
    HEART_RATE_MAX = 175                   # 心率上限（高于=危险）
    SPO2_THRESHOLD = 93.0                  # 血氧阈值
    MOTIONLESS_WARN_SEC = 120              # 静止120秒发出预警
    MOTIONLESS_SOS_SEC = 300               # 静止300秒触发SOS
    CHECKIN_GRACE_PERIOD_SEC = 300         # 签到宽限期
    NIGHT_HOURS = (22, 6)                  # 夜间时段（22:00-06:00）

    def evaluate(self, sensor_data: dict) -> TriggerEvent:
        """
        评估传感器数据，判断是否触发SOS

        sensor_data 字段（全部可选，提供越多越准确）：
          heart_rate, heart_rate_baseline, spo2, skin_temp
          fall_detected, impact_g_force, motionless_sec
          sos_button_pressed, voice_keyword_detected, gesture_sos
          checkin_overdue_sec, location, location_drift_detected
          remote_trigger_verified, hour_of_day
          battery_level, network_available
        """
        sources = []
        trigger_type = "none"

        # ── 1. 主动触发（绝对优先）─────────────────────────────────
        if sensor_data.get("sos_button_pressed"):
            sources.append(("manual_button", "CRITICAL", "SOS按键主动按下"))
            trigger_type = "manual"

        if sensor_data.get("voice_keyword_detected"):
            sources.append(("voice_sos", "SEVERE", "语音SOS关键词识别"))
            trigger_type = trigger_type if trigger_type != "none" else "manual"

        if sensor_data.get("gesture_sos"):
            sources.append(("gesture_sos", "SEVERE", "SOS手势识别"))

        # ── 2. 生物特征异常检测 ────────────────────────────────────
        hr = sensor_data.get("heart_rate")
        hr_baseline = sensor_data.get("heart_rate_baseline", 70)
        if hr is not None:
            if hr < self.HEART_RATE_MIN:
                sources.append(("hr_low", "CRITICAL", f"心率危低 {hr}bpm"))
                trigger_type = "biometric"
            elif hr > self.HEART_RATE_MAX:
                sources.append(("hr_high", "CRITICAL", f"心率危高 {hr}bpm"))
                trigger_type = "biometric"
            elif hr_baseline and abs(hr - hr_baseline) / hr_baseline > 0.55:
                sources.append(("hr_deviation", "SEVERE",
                                 f"心率偏离 {hr}bpm vs 基线{hr_baseline}bpm"))
                trigger_type = trigger_type if trigger_type != "none" else "biometric"

        spo2 = sensor_data.get("spo2")
        if spo2 is not None and spo2 < self.SPO2_THRESHOLD:
            sources.append(("spo2_low", "CRITICAL", f"血氧 {spo2:.1f}%"))
            trigger_type = "biometric"

        # ── 3. 跌倒检测（结合静止确认）────────────────────────────
        fall = sensor_data.get("fall_detected", False)
        motionless = sensor_data.get("motionless_sec", 0)
        g_force = sensor_data.get("impact_g_force")

        if fall:
            if motionless >= self.FALL_CONFIRM_MOTIONLESS_SEC:
                level = "CRITICAL" if (g_force and g_force > 6.0) else "SEVERE"
                sources.append(("fall_confirmed", level,
                                 f"跌倒后静止{motionless}秒（{g_force or '?'}G）"))
                trigger_type = "biometric"
            else:
                # 跌倒但用户可能已起身，记录但不触发
                sources.append(("fall_detected_only", "WATCH",
                                 f"跌倒检测（静止{motionless}s，等待确认）"))

        # ── 4. 行为异常检测 ─────────────────────────────────────
        if not fall and motionless >= self.MOTIONLESS_SOS_SEC:
            sources.append(("long_motionless", "SEVERE",
                             f"长时间静止 {motionless}s"))
            trigger_type = trigger_type if trigger_type != "none" else "behavioral"

        checkin_overdue = sensor_data.get("checkin_overdue_sec", 0)
        if checkin_overdue > self.CHECKIN_GRACE_PERIOD_SEC:
            sources.append(("checkin_timeout", "URGENT",
                             f"签到超时 {checkin_overdue}s"))
            trigger_type = trigger_type if trigger_type != "none" else "behavioral"

        if sensor_data.get("location_drift_detected"):
            sources.append(("location_drift", "URGENT", "位置异常漂移"))

        hour = sensor_data.get("hour_of_day")
        if hour is not None:
            night_start, night_end = self.NIGHT_HOURS
            is_night = hour >= night_start or hour < night_end
            if is_night and len(sources) >= 2:
                sources.append(("night_context", "WATCH",
                                 f"夜间{hour:02d}时（加权系数+20%）"))

        # ── 5. 远程授权触发 ─────────────────────────────────────
        if sensor_data.get("remote_trigger_verified"):
            sources.append(("remote_verified", "SEVERE",
                             "授权联系人远程核验触发"))
            trigger_type = trigger_type if trigger_type != "none" else "remote"

        # ── 判断是否激活 ────────────────────────────────────────
        critical_sources = [s for s in sources if s[1] == "CRITICAL"]
        severe_sources = [s for s in sources if s[1] == "SEVERE"]

        activated = (
            len(critical_sources) >= 1 or
            len(severe_sources) >= 1 or
            (len(sources) >= 3)  # 3个及以上任意信号=触发
        )

        if len(critical_sources) >= 1 and len(severe_sources) >= 1:
            trigger_type = "compound"

        return TriggerEvent(
            activated=activated,
            trigger_type=trigger_type if activated else "none",
            trigger_sources=[{"id": s[0], "level": s[1], "desc": s[2]}
                              for s in sources],
            raw_data=sensor_data,
        )

    def describe(self, event: TriggerEvent) -> str:
        """生成人类可读的触发摘要"""
        if not event.activated:
            non_critical = [s["desc"] for s in event.trigger_sources]
            if non_critical:
                return f"未触发SOS。观测到：{'；'.join(non_critical)}"
            return "未触发SOS。传感器数据正常。"

        sources_text = "；".join(s["desc"] for s in event.trigger_sources)
        return (
            f"[{event.event_id}] SOS已触发（类型：{event.trigger_type}）\n"
            f"信号来源：{sources_text}\n"
            f"触发时间：{event.timestamp}"
        )


# ─────────────────────────── CLI 调试入口 ───────────────────────────

if __name__ == "__main__":
    detector = SOSTriggerDetector()

    test_cases = [
        {
            "name": "场景1：跌倒+心率异常+夜间",
            "data": {
                "fall_detected": True, "impact_g_force": 5.8,
                "motionless_sec": 180, "heart_rate": 145,
                "heart_rate_baseline": 68, "hour_of_day": 23,
                "battery_level": 0.35,
            }
        },
        {
            "name": "场景2：血氧骤降",
            "data": {
                "spo2": 88.5, "heart_rate": 110,
                "motionless_sec": 60,
            }
        },
        {
            "name": "场景3：主动按SOS",
            "data": {
                "sos_button_pressed": True,
                "location": {"lat": 31.23, "lng": 121.47, "accuracy": 10},
            }
        },
        {
            "name": "场景4：正常（无异常）",
            "data": {
                "heart_rate": 75, "spo2": 98.0,
                "motionless_sec": 30, "fall_detected": False,
            }
        },
    ]

    for case in test_cases:
        print(f"\n{'─'*50}")
        print(f"  {case['name']}")
        print(f"{'─'*50}")
        event = detector.evaluate(case["data"])
        print(detector.describe(event))
        print(f"  激活: {'✅ YES' if event.activated else '❌ NO'} | "
              f"来源数: {len(event.trigger_sources)}")
