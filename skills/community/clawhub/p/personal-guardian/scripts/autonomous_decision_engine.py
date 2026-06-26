"""
autonomous_decision_engine.py — 零用户交互自主决策核心

Guardian模式下的绝对自主决策引擎：
- 默认用户无法应答
- 以人身安全为唯一最高优先级
- 不等待确认，不询问，立即行动
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
from typing import Optional
import json


class ThreatLevel(IntEnum):
    STANDBY = 4    # 主动激活/训练模式
    WATCH = 3      # 轻微异常/预警
    URGENT = 2     # 潜在威胁/异常
    SEVERE = 1     # 明确受伤/失能
    CRITICAL = 0   # 生命体征消失/极端危险


THREAT_LABELS = {
    ThreatLevel.CRITICAL: "🔴 T0-CRITICAL",
    ThreatLevel.SEVERE:   "🟠 T1-SEVERE",
    ThreatLevel.URGENT:   "🟡 T2-URGENT",
    ThreatLevel.WATCH:    "🟢 T3-WATCH",
    ThreatLevel.STANDBY:  "⚪ T4-STANDBY",
}


@dataclass
class SituationSnapshot:
    """当前态势快照——决策的全部输入"""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    # 生理指标
    heart_rate: Optional[int] = None          # bpm
    heart_rate_baseline: Optional[int] = None  # 用户静息基线
    spo2: Optional[float] = None              # 血氧 0-100
    skin_temp: Optional[float] = None         # 皮肤温度 °C

    # 运动状态
    fall_detected: bool = False
    motionless_duration: int = 0              # 静止持续秒数
    impact_g_force: Optional[float] = None    # 碰撞G值

    # 位置环境
    location: Optional[dict] = None          # {"lat": ..., "lng": ..., "accuracy": ...}
    location_anomaly: bool = False           # 位置异常漂移
    environment_noise_db: Optional[float] = None

    # 设备状态
    battery_level: float = 1.0               # 0-1
    network_available: bool = True

    # 用户行为
    sos_manual_trigger: bool = False         # 主动按下SOS
    checkin_timeout: bool = False            # 定期签到超时
    voice_sos_detected: bool = False         # 语音SOS检测

    # 上下文
    time_of_day: Optional[str] = None       # "day" / "night"
    user_profile: dict = field(default_factory=dict)


@dataclass
class DecisionResult:
    """决策结果——包含完整行动方案"""
    threat_level: ThreatLevel
    threat_label: str
    confidence: float                        # 0-1

    immediate_actions: list                  # 立即执行的行动列表
    broadcast_script: str                   # 对外广播的文本模板
    data_to_collect: list                   # 需要立即采集的数据
    escalation_plan: dict                   # 升级计划（时间->行动）

    rationale: str                          # 决策推理说明
    battery_strategy: str                   # 低电量应对策略
    estimated_critical_window: int          # 预估关键响应窗口（秒）


class AutonomousDecisionEngine:
    """
    零交互自主决策引擎

    设计原则：
    1. 宁可误报，绝不漏报（生命安全非对称原则）
    2. 最坏情况假设（无法联系到用户=用户失能）
    3. 饱和广播优于精准通知
    4. 电量优先保留通讯功能
    """

    # 生理异常阈值
    HEART_RATE_CRITICAL_HIGH = 180
    HEART_RATE_CRITICAL_LOW = 40
    HEART_RATE_SEVERE_DEVIATION = 0.6     # 偏离基线60%以上
    SPO2_CRITICAL = 90.0
    SPO2_SEVERE = 94.0
    MOTIONLESS_CRITICAL_SEC = 300         # 5分钟静止=严重
    MOTIONLESS_SEVERE_SEC = 180           # 3分钟静止=严重预警
    IMPACT_CRITICAL_G = 8.0
    IMPACT_SEVERE_G = 4.0

    def evaluate(self, snapshot: SituationSnapshot) -> DecisionResult:
        """核心决策方法——输入态势快照，输出完整决策"""

        # 计算威胁信号矩阵
        signals = self._compute_threat_signals(snapshot)
        level = self._determine_threat_level(signals, snapshot)
        confidence = self._compute_confidence(signals, snapshot)

        return DecisionResult(
            threat_level=level,
            threat_label=THREAT_LABELS[level],
            confidence=confidence,
            immediate_actions=self._plan_immediate_actions(level, snapshot),
            broadcast_script=self._compose_broadcast_script(level, snapshot),
            data_to_collect=self._determine_data_collection(level, snapshot),
            escalation_plan=self._build_escalation_plan(level),
            rationale=self._explain_rationale(signals, level),
            battery_strategy=self._battery_strategy(snapshot.battery_level, level),
            estimated_critical_window=self._estimate_critical_window(level, snapshot),
        )

    def _compute_threat_signals(self, s: SituationSnapshot) -> dict:
        """计算各维度威胁信号"""
        signals = {}

        # 主动SOS信号（最高权重）
        if s.sos_manual_trigger:
            signals["manual_sos"] = ("CRITICAL", "用户主动激活SOS")
        if s.voice_sos_detected:
            signals["voice_sos"] = ("SEVERE", "语音SOS检测")

        # 跌倒检测
        if s.fall_detected:
            if s.impact_g_force and s.impact_g_force >= self.IMPACT_CRITICAL_G:
                signals["fall"] = ("CRITICAL", f"高冲击跌倒 {s.impact_g_force:.1f}G")
            elif s.impact_g_force and s.impact_g_force >= self.IMPACT_SEVERE_G:
                signals["fall"] = ("SEVERE", f"跌倒检测 {s.impact_g_force:.1f}G")
            else:
                signals["fall"] = ("URGENT", "跌倒检测（低冲击）")

        # 静止时长
        if s.motionless_duration >= self.MOTIONLESS_CRITICAL_SEC:
            signals["motionless"] = ("CRITICAL", f"静止 {s.motionless_duration}秒（>{self.MOTIONLESS_CRITICAL_SEC}s阈值）")
        elif s.motionless_duration >= self.MOTIONLESS_SEVERE_SEC:
            signals["motionless"] = ("SEVERE", f"静止 {s.motionless_duration}秒")

        # 心率异常
        if s.heart_rate is not None:
            if s.heart_rate >= self.HEART_RATE_CRITICAL_HIGH or s.heart_rate <= self.HEART_RATE_CRITICAL_LOW:
                signals["heart_rate"] = ("CRITICAL", f"心率极值 {s.heart_rate}bpm")
            elif s.heart_rate_baseline:
                deviation = abs(s.heart_rate - s.heart_rate_baseline) / s.heart_rate_baseline
                if deviation >= self.HEART_RATE_SEVERE_DEVIATION:
                    signals["heart_rate"] = ("SEVERE", f"心率偏离基线 {deviation:.0%}（{s.heart_rate}bpm vs 基线{s.heart_rate_baseline}bpm）")

        # 血氧
        if s.spo2 is not None:
            if s.spo2 < self.SPO2_CRITICAL:
                signals["spo2"] = ("CRITICAL", f"血氧危急 {s.spo2:.1f}%")
            elif s.spo2 < self.SPO2_SEVERE:
                signals["spo2"] = ("SEVERE", f"血氧偏低 {s.spo2:.1f}%")

        # 签到超时
        if s.checkin_timeout:
            signals["checkin"] = ("URGENT", "定期签到超时")

        # 位置异常
        if s.location_anomaly:
            signals["location_anomaly"] = ("URGENT", "位置异常漂移")

        return signals

    def _determine_threat_level(self, signals: dict, s: SituationSnapshot) -> ThreatLevel:
        """从信号矩阵推导最终威胁等级"""
        if not signals:
            return ThreatLevel.STANDBY

        level_priority = {"CRITICAL": 0, "SEVERE": 1, "URGENT": 2, "WATCH": 3}
        highest = min(signals.values(), key=lambda x: level_priority.get(x[0], 99))
        highest_label = highest[0]

        # 信号叠加升级：两个SEVERE=CRITICAL
        severe_count = sum(1 for v in signals.values() if v[0] == "SEVERE")
        if highest_label == "SEVERE" and severe_count >= 2:
            highest_label = "CRITICAL"

        mapping = {"CRITICAL": ThreatLevel.CRITICAL, "SEVERE": ThreatLevel.SEVERE,
                   "URGENT": ThreatLevel.URGENT, "WATCH": ThreatLevel.WATCH}
        return mapping.get(highest_label, ThreatLevel.STANDBY)

    def _compute_confidence(self, signals: dict, s: SituationSnapshot) -> float:
        """计算决策置信度"""
        if s.sos_manual_trigger:
            return 0.99  # 主动触发：最高置信

        signal_count = len(signals)
        base_confidence = min(0.5 + signal_count * 0.15, 0.95)

        # 信号一致性加成
        labels = [v[0] for v in signals.values()]
        if len(set(labels)) == 1:
            base_confidence = min(base_confidence + 0.1, 0.97)

        return round(base_confidence, 2)

    def _plan_immediate_actions(self, level: ThreatLevel, s: SituationSnapshot) -> list:
        """规划立即行动清单"""
        actions = []

        if level <= ThreatLevel.CRITICAL:
            actions += [
                {"priority": 1, "action": "CALL_EMERGENCY", "target": "120",
                 "message": f"用户疑似失能，位置：{self._format_location(s.location)}"},
                {"priority": 2, "action": "CALL_EMERGENCY", "target": "110",
                 "message": "安全预警同步"},
                {"priority": 3, "action": "START_RECORDING", "duration": -1,
                 "note": "全程录音存证"},
                {"priority": 4, "action": "BROADCAST_ALL_CONTACTS",
                 "urgency": "CRITICAL"},
                {"priority": 5, "action": "BROADCAST_LOCATION",
                 "interval_sec": 30},
            ]

        elif level <= ThreatLevel.SEVERE:
            actions += [
                {"priority": 1, "action": "CALL_EMERGENCY", "target": "120"},
                {"priority": 2, "action": "SMS_EMERGENCY_CONTACTS",
                 "urgency": "SEVERE"},
                {"priority": 3, "action": "START_RECORDING", "duration": 3600},
                {"priority": 4, "action": "BROADCAST_LOCATION",
                 "interval_sec": 30},
            ]

        elif level <= ThreatLevel.URGENT:
            actions += [
                {"priority": 1, "action": "SMS_TIER1_CONTACTS",
                 "urgency": "URGENT"},
                {"priority": 2, "action": "PUSH_NOTIFICATION_ALL"},
                {"priority": 3, "action": "SCHEDULE_ESCALATION",
                 "delay_sec": 600, "to_level": "SEVERE"},
            ]

        else:  # WATCH / STANDBY
            actions += [
                {"priority": 1, "action": "PUSH_NOTIFICATION_PRIMARY"},
                {"priority": 2, "action": "AWAIT_USER_CONFIRMATION",
                 "timeout_sec": 120},
            ]

        return actions

    def _compose_broadcast_script(self, level: ThreatLevel,
                                   s: SituationSnapshot) -> str:
        """生成对外广播文本"""
        user_name = s.user_profile.get("name", "您的联系人")
        time_str = datetime.now().strftime("%H:%M")
        location_str = self._format_location(s.location)

        if level <= ThreatLevel.CRITICAL:
            return (
                f"【🔴紧急求救】{user_name} 于 {time_str} 触发紧急求救信号，"
                f"设备检测到生命体征异常，本人可能无法回应。"
                f"当前位置：{location_str}。"
                f"请立即拨打120或前往查看。此消息由AI守护系统自动发送。"
            )
        elif level <= ThreatLevel.SEVERE:
            return (
                f"【🟠紧急提醒】{user_name} 于 {time_str} 触发安全警报，"
                f"检测到异常状态（跌倒/心率异常/长时间无响应）。"
                f"位置：{location_str}。请立即联系确认安全。"
            )
        elif level <= ThreatLevel.URGENT:
            return (
                f"【🟡安全提醒】{user_name} 的设备于 {time_str} 检测到异常，"
                f"当前位置：{location_str}。请尝试联系确认状态。"
            )
        else:
            return (
                f"【ℹ️状态通知】{user_name} 已激活个人守护模式，"
                f"当前位置：{location_str}，状态监控中。"
            )

    def _determine_data_collection(self, level: ThreatLevel,
                                    s: SituationSnapshot) -> list:
        """确定需要立即采集的数据"""
        base = ["gps_location", "device_timestamp", "battery_status"]

        if level <= ThreatLevel.SEVERE:
            base += ["audio_recording", "heart_rate_stream",
                     "spo2_stream", "accelerometer_stream"]
        if level <= ThreatLevel.URGENT:
            base += ["environment_photo"]

        return base

    def _build_escalation_plan(self, current_level: ThreatLevel) -> dict:
        """构建时间轴升级计划"""
        if current_level <= ThreatLevel.CRITICAL:
            return {
                "30s": "重播位置广播，检查120是否接通",
                "2min": "拨打所有一级联系人",
                "5min": "拨打所有二级联系人，启动蓝牙周边广播",
                "10min": "社交媒体紧急广播（已授权账号）",
                "continuous": "每5分钟循环，直至救援确认",
            }
        elif current_level <= ThreatLevel.SEVERE:
            return {
                "2min_no_response": "升级至CRITICAL协议",
                "5min": "拨打二级联系人",
                "10min": "拨打120",
            }
        else:
            return {
                "10min_no_response": "升级至SEVERE协议",
                "20min_no_response": "升级至CRITICAL协议",
            }

    def _explain_rationale(self, signals: dict, level: ThreatLevel) -> str:
        """推理说明"""
        if not signals:
            return "无异常信号，进入待机守护状态。"

        signal_descriptions = [f"{v[1]}" for v in signals.values()]
        level_desc = THREAT_LABELS[level]
        return (
            f"检测到 {len(signals)} 个异常信号：{'；'.join(signal_descriptions)}。"
            f"综合评定威胁等级：{level_desc}。"
            f"基于生命安全优先原则，立即启动对应响应协议。"
        )

    def _battery_strategy(self, battery: float, level: ThreatLevel) -> str:
        """低电量应对策略"""
        if battery > 0.3:
            return "电量充足，全功能运行。"
        elif battery > 0.15:
            return "低电量模式：关闭屏幕显示、停止非必要传感器，优先保留GPS+通讯。"
        elif battery > 0.05:
            return "极低电量：仅保留短信发送和GPS，每5分钟发送一次位置，关闭录音。"
        else:
            if level <= ThreatLevel.SEVERE:
                return "临界电量：发送最后一条位置短信后保持通讯待机，拒绝接入非紧急操作。"
            return "临界电量：发送最后位置后节能待机，等待救援充电。"

    def _estimate_critical_window(self, level: ThreatLevel,
                                   s: SituationSnapshot) -> int:
        """预估关键响应窗口（秒）"""
        if level == ThreatLevel.CRITICAL:
            return 300   # 5分钟
        elif level == ThreatLevel.SEVERE:
            return 600   # 10分钟
        elif level == ThreatLevel.URGENT:
            return 1800  # 30分钟
        return 3600

    def _format_location(self, location: Optional[dict]) -> str:
        if not location:
            return "位置获取中..."
        lat = location.get("lat", "?")
        lng = location.get("lng", "?")
        return f"经纬度 {lat},{lng}（精度 {location.get('accuracy', '?')}m）"


# ─────────────────────────── CLI 调试入口 ───────────────────────────

if __name__ == "__main__":
    engine = AutonomousDecisionEngine()

    # 测试场景：深夜跌倒 + 心率异常 + 长时间静止
    snapshot = SituationSnapshot(
        heart_rate=148,
        heart_rate_baseline=72,
        spo2=93.5,
        fall_detected=True,
        impact_g_force=5.2,
        motionless_duration=420,
        location={"lat": 31.2304, "lng": 121.4737, "accuracy": 15},
        battery_level=0.23,
        time_of_day="night",
        user_profile={"name": "用户A", "age": 32},
    )

    result = engine.evaluate(snapshot)

    print(f"\n{'='*60}")
    print(f"威胁等级: {result.threat_label}  |  置信度: {result.confidence:.0%}")
    print(f"{'='*60}")
    print(f"\n推理说明:\n  {result.rationale}")
    print(f"\n关键响应窗口: {result.estimated_critical_window}秒")
    print(f"\n立即行动 ({len(result.immediate_actions)} 项):")
    for a in result.immediate_actions:
        print(f"  [{a['priority']}] {a['action']}")
    print(f"\n广播脚本:\n  {result.broadcast_script}")
    print(f"\n电量策略:\n  {result.battery_strategy}")
    print(f"\n升级计划:")
    for t, plan in result.escalation_plan.items():
        print(f"  {t}: {plan}")
