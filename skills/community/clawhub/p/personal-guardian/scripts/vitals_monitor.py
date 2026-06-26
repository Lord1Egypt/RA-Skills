"""
vitals_monitor.py — 生命体征持续监控与趋势预警

持续采集并分析生理信号，发出预警供 autonomous_decision_engine 决策使用。
支持滑动窗口趋势分析，区分"瞬时异常"和"持续恶化"。
"""

from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
from typing import Optional
import statistics


@dataclass
class VitalReading:
    """单次生命体征读数"""
    timestamp: str
    heart_rate: Optional[int] = None
    spo2: Optional[float] = None
    skin_temp: Optional[float] = None
    motion_g: Optional[float] = None     # 加速度G值
    irregular_pulse: bool = False


@dataclass
class VitalAlert:
    """生命体征预警"""
    alert_type: str      # hr_high / hr_low / spo2_low / temp_extreme / trend_deteriorate
    severity: str        # WARNING / CRITICAL
    value: float
    threshold: float
    trend: str           # rising / falling / stable
    message: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class VitalsMonitor:
    """
    生命体征持续监控器

    特性：
    - 滑动窗口（默认最近20次读数）
    - 趋势分析：区分瞬时异常 vs 持续恶化
    - 个性化基线：基于用户历史数据动态调整
    """

    # ── 默认阈值（可被用户基线覆盖）─────────────────────────
    HR_MIN = 45
    HR_MAX = 175
    HR_CRITICAL_MIN = 35
    HR_CRITICAL_MAX = 200
    SPO2_WARNING = 94.0
    SPO2_CRITICAL = 90.0
    TEMP_HIGH_WARNING = 38.5
    TEMP_HIGH_CRITICAL = 40.0
    TEMP_LOW_WARNING = 35.0
    TEMP_LOW_CRITICAL = 33.0

    WINDOW_SIZE = 20

    def __init__(self, user_baseline: Optional[dict] = None):
        self.baseline = user_baseline or {}
        self.history: deque = deque(maxlen=self.WINDOW_SIZE)
        self.active_alerts: list = []
        self._user_hr_baseline = self.baseline.get("heart_rate", 70)

    def ingest(self, reading: VitalReading) -> list:
        """摄入一次读数，返回新触发的预警列表"""
        self.history.append(reading)
        new_alerts = []

        # ── 心率检测 ──────────────────────────────────────────
        if reading.heart_rate is not None:
            hr = reading.heart_rate
            if hr <= self.HR_CRITICAL_MIN:
                new_alerts.append(VitalAlert(
                    "hr_low", "CRITICAL", hr, self.HR_CRITICAL_MIN,
                    "falling", f"心率危低 {hr}bpm（心搏骤停风险）"
                ))
            elif hr >= self.HR_CRITICAL_MAX:
                new_alerts.append(VitalAlert(
                    "hr_high", "CRITICAL", hr, self.HR_CRITICAL_MAX,
                    "rising", f"心率危高 {hr}bpm"
                ))
            elif hr <= self.HR_MIN or hr >= self.HR_MAX:
                new_alerts.append(VitalAlert(
                    "hr_abnormal", "WARNING", hr,
                    self.HR_MIN if hr <= self.HR_MIN else self.HR_MAX,
                    "stable", f"心率异常 {hr}bpm"
                ))
            else:
                # 检查偏离用户基线
                deviation = abs(hr - self._user_hr_baseline) / self._user_hr_baseline
                if deviation > 0.6:
                    new_alerts.append(VitalAlert(
                        "hr_deviation", "WARNING", hr, self._user_hr_baseline,
                        "rising" if hr > self._user_hr_baseline else "falling",
                        f"心率偏离基线 {deviation:.0%}（{hr} vs 基线{self._user_hr_baseline}）"
                    ))

        # ── 血氧检测 ──────────────────────────────────────────
        if reading.spo2 is not None:
            spo2 = reading.spo2
            if spo2 < self.SPO2_CRITICAL:
                new_alerts.append(VitalAlert(
                    "spo2_low", "CRITICAL", spo2, self.SPO2_CRITICAL,
                    "falling", f"血氧危低 {spo2:.1f}%（缺氧风险）"
                ))
            elif spo2 < self.SPO2_WARNING:
                new_alerts.append(VitalAlert(
                    "spo2_warning", "WARNING", spo2, self.SPO2_WARNING,
                    "falling", f"血氧偏低 {spo2:.1f}%"
                ))

        # ── 体温检测 ──────────────────────────────────────────
        if reading.skin_temp is not None:
            temp = reading.skin_temp
            if temp >= self.TEMP_HIGH_CRITICAL:
                new_alerts.append(VitalAlert(
                    "temp_high", "CRITICAL", temp, self.TEMP_HIGH_CRITICAL,
                    "rising", f"体温极高 {temp:.1f}°C（高烧危险）"
                ))
            elif temp <= self.TEMP_LOW_CRITICAL:
                new_alerts.append(VitalAlert(
                    "temp_low", "CRITICAL", temp, self.TEMP_LOW_CRITICAL,
                    "falling", f"体温极低 {temp:.1f}°C（失温危险）"
                ))

        # ── 趋势分析（滑动窗口）──────────────────────────────
        trend_alerts = self._analyze_trends()
        new_alerts.extend(trend_alerts)

        self.active_alerts.extend(new_alerts)
        return new_alerts

    def _analyze_trends(self) -> list:
        """分析近N次读数的趋势"""
        alerts = []
        if len(self.history) < 5:
            return alerts

        recent = list(self.history)[-5:]

        # 心率趋势
        hr_values = [r.heart_rate for r in recent if r.heart_rate]
        if len(hr_values) >= 4:
            trend = hr_values[-1] - hr_values[0]
            if trend > 40:  # 5次读数内心率上升40bpm
                alerts.append(VitalAlert(
                    "hr_trend_rising", "WARNING",
                    hr_values[-1], hr_values[0],
                    "rising", f"心率持续快速上升（+{trend}bpm/近5次）"
                ))
            elif trend < -30:  # 心率快速下降
                alerts.append(VitalAlert(
                    "hr_trend_falling", "WARNING",
                    hr_values[-1], hr_values[0],
                    "falling", f"心率持续快速下降（{trend}bpm/近5次）"
                ))

        # 血氧趋势
        spo2_values = [r.spo2 for r in recent if r.spo2]
        if len(spo2_values) >= 4:
            trend = spo2_values[-1] - spo2_values[0]
            if trend < -3.0:  # 血氧持续下降3%
                alerts.append(VitalAlert(
                    "spo2_trend_falling", "WARNING",
                    spo2_values[-1], spo2_values[0],
                    "falling", f"血氧持续下降（{trend:.1f}%/近5次）"
                ))

        return alerts

    def summarize(self) -> dict:
        """生成当前生命体征摘要"""
        if not self.history:
            return {"status": "no_data"}

        latest = self.history[-1]
        hr_values = [r.heart_rate for r in self.history if r.heart_rate]
        spo2_values = [r.spo2 for r in self.history if r.spo2]

        return {
            "timestamp": latest.timestamp,
            "latest": {
                "heart_rate": latest.heart_rate,
                "spo2": latest.spo2,
                "skin_temp": latest.skin_temp,
            },
            "statistics": {
                "hr_avg": round(statistics.mean(hr_values), 1) if hr_values else None,
                "hr_min": min(hr_values) if hr_values else None,
                "hr_max": max(hr_values) if hr_values else None,
                "spo2_avg": round(statistics.mean(spo2_values), 1) if spo2_values else None,
            },
            "active_alerts": len(self.active_alerts),
            "critical_alerts": len([a for a in self.active_alerts if a.severity == "CRITICAL"]),
        }


# ─────────────────────────── CLI 调试入口 ───────────────────────────

if __name__ == "__main__":
    monitor = VitalsMonitor(user_baseline={"heart_rate": 68})

    # 模拟一组读数：血氧逐渐下降 + 心率上升（溺水/缺氧场景）
    import time
    test_readings = [
        VitalReading(datetime.now().isoformat(), heart_rate=70, spo2=98.0),
        VitalReading(datetime.now().isoformat(), heart_rate=82, spo2=97.2),
        VitalReading(datetime.now().isoformat(), heart_rate=95, spo2=96.1),
        VitalReading(datetime.now().isoformat(), heart_rate=112, spo2=94.8),
        VitalReading(datetime.now().isoformat(), heart_rate=135, spo2=92.3),
        VitalReading(datetime.now().isoformat(), heart_rate=148, spo2=89.5),
    ]

    print("="*50)
    print("生命体征监控模拟（缺氧场景）")
    print("="*50)

    for i, reading in enumerate(test_readings):
        alerts = monitor.ingest(reading)
        status = "⚠️ " + " | ".join(a.message for a in alerts) if alerts else "✅ 正常"
        print(f"  读数{i+1}: HR={reading.heart_rate}bpm  SpO2={reading.spo2}%  →  {status}")

    print(f"\n生命体征摘要:")
    summary = monitor.summarize()
    for k, v in summary.items():
        print(f"  {k}: {v}")
