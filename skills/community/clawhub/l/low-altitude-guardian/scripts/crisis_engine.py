"""
危机响应引擎 (Crisis Response Engine)

核心调度模块，负责：
- 危机分级与分类
- 方案匹配与评分
- 执行监控与动态调整
- 知识库自迭代学习
"""

import argparse
import json
import math
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
SOLUTION_TEMPLATES_DIR = PROJECT_ROOT / "assets" / "solution_templates"
DEVICE_PROFILES_DIR = PROJECT_ROOT / "assets" / "device_profiles"
INCIDENTS_DIR = PROJECT_ROOT / ".guardian" / "incidents"
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / ".guardian" / "knowledge_base"


class CrisisLevel(Enum):
    """危机等级枚举。"""
    L1_CAUTION = "L1-CAUTION"
    L2_MINOR = "L2-MINOR"
    L3_MAJOR = "L3-MAJOR"
    L4_SEVERE = "L4-SEVERE"
    L5_CRITICAL = "L5-CRITICAL"

    @property
    def response_time_seconds(self) -> int:
        return {
            "L1-CAUTION": 300,
            "L2-MINOR": 120,
            "L3-MAJOR": 30,
            "L4-SEVERE": 10,
            "L5-CRITICAL": 3,
        }[self.value]

    @property
    def severity_rank(self) -> int:
        return {
            "L1-CAUTION": 1,
            "L2-MINOR": 2,
            "L3-MAJOR": 3,
            "L4-SEVERE": 4,
            "L5-CRITICAL": 5,
        }[self.value]


@dataclass
class CrisisClassification:
    """危机分类结果。"""
    level: CrisisLevel
    crisis_type: str
    sub_type: str
    confidence: float
    is_escalating: bool = False
    cascade_risk: list = field(default_factory=list)
    available_decision_window_s: float = 0
    compound_type: Optional[str] = None
    special_action: Optional[str] = None


@dataclass
class SafetyScore:
    """安全评分。"""
    human_safety: float = 100.0       # S0 - P0
    public_safety: float = 100.0      # S1 - P1
    third_party_property: float = 100.0  # S2 - P2
    device_safety: float = 100.0      # S3 - P3
    mission_completion: float = 100.0  # S4 - P4

    # 权重常量
    W0 = 0.40  # 人员安全
    W1 = 0.25  # 公共安全
    W2 = 0.15  # 第三方财产
    W3 = 0.12  # 本机安全
    W4 = 0.08  # 任务完成

    @property
    def total_score(self) -> float:
        return (
            self.W0 * self.human_safety +
            self.W1 * self.public_safety +
            self.W2 * self.third_party_property +
            self.W3 * self.device_safety +
            self.W4 * self.mission_completion
        )

    @property
    def is_vetoed(self) -> bool:
        """S0 < 80 硬性否决。"""
        return self.human_safety < 80

    @property
    def needs_human_confirm(self) -> bool:
        """S1 < 60 需要人工确认。"""
        return self.public_safety < 60


@dataclass
class DecisionPlan:
    """决策方案。"""
    plan_id: str
    name: str
    source: str  # knowledge_base | emergency_reasoning
    confidence: float
    safety_score: SafetyScore
    steps: list = field(default_factory=list)
    estimated_loss: dict = field(default_factory=dict)
    is_vetoed: bool = False
    veto_reason: str = ""


# ─── 危机分级引擎 ─────────────────────────────────────────────

# 危机类型到基线等级的映射规则
_CRISIS_BASELINE_RULES = {
    "power_failure.single_motor_loss": CrisisLevel.L3_MAJOR,
    "power_failure.multi_motor_loss": CrisisLevel.L4_SEVERE,
    "power_failure.total_power_loss": CrisisLevel.L5_CRITICAL,
    "power_failure.battery_critical": CrisisLevel.L3_MAJOR,
    "power_failure.battery_thermal": CrisisLevel.L4_SEVERE,
    "navigation_failure.gps_loss": CrisisLevel.L3_MAJOR,
    "navigation_failure.imu_failure": CrisisLevel.L4_SEVERE,
    "navigation_failure.multi_sensor_failure": CrisisLevel.L4_SEVERE,
    "communication_failure.rc_lost": CrisisLevel.L2_MINOR,
    "communication_failure.link_lost": CrisisLevel.L3_MAJOR,
    "communication_failure.all_comms_lost": CrisisLevel.L3_MAJOR,
    "environment_threat.severe_weather": CrisisLevel.L3_MAJOR,
    "environment_threat.wind_shear": CrisisLevel.L4_SEVERE,
    "environment_threat.bird_strike": CrisisLevel.L3_MAJOR,
    "collision_risk.manned_aircraft": CrisisLevel.L5_CRITICAL,
    "collision_risk.building": CrisisLevel.L3_MAJOR,
    "collision_risk.ground_crowd": CrisisLevel.L5_CRITICAL,
    "collision_risk.power_line": CrisisLevel.L4_SEVERE,
}

# 复合故障矩阵：当快照中同时存在多个故障信号时，识别复合故障
# key: frozenset of crisis types, value: compound info
COMPOUND_FAILURE_MATRIX = {
    frozenset(["navigation_failure.gps_loss", "communication_failure.link_lost"]): {
        "compound_type": "navigation_comms_blackout",
        "level_override": CrisisLevel.L4_SEVERE,
        "cascade_risks": ["设备进入盲飞状态：无GPS且无遥测链路，无法接收指令也无法自主导航"],
        "special_action": "立即激活预置返航程序（不依赖GPS的惯导模式）",
    },
    frozenset(["power_failure.single_motor_loss", "power_failure.battery_critical"]): {
        "compound_type": "degraded_power_critical",
        "level_override": CrisisLevel.L4_SEVERE,
        "cascade_risks": ["剩余电机因过载可能继续失效", "电量不足以支撑降级飞行完成返航"],
        "special_action": "放弃返航，就近选择安全区域立即降落",
    },
    frozenset(["power_failure.battery_thermal", "power_failure.battery_critical"]): {
        "compound_type": "battery_failure_imminent",
        "level_override": CrisisLevel.L5_CRITICAL,
        "cascade_risks": ["热失控可能在60秒内导致爆炸或起火，威胁地面人员"],
        "special_action": "优先寻找水域或空旷地执行受控坠机，人员撤离",
    },
    frozenset(["navigation_failure.gps_loss", "navigation_failure.imu_failure"]): {
        "compound_type": "full_navigation_failure",
        "level_override": CrisisLevel.L5_CRITICAL,
        "cascade_risks": ["无任何可靠位置/姿态参考，设备无法维持稳定飞行"],
        "special_action": "立即切换视觉定位（如有），否则执行最近区域受控降落",
    },
    frozenset(["power_failure.multi_motor_loss", "power_failure.battery_critical"]): {
        "compound_type": "catastrophic_power_failure",
        "level_override": CrisisLevel.L5_CRITICAL,
        "cascade_risks": ["多电机失效 + 低电量，设备无法维持飞行，迫降不可避免"],
        "special_action": "立即选择损失最小的坠落区域，发出紧急广播",
    },
}


def detect_compound_failures(snapshot: dict, detected_types: list) -> Optional[dict]:
    """
    检测复合故障。

    Args:
        snapshot: 态势感知快照（保留以供将来扩展）
        detected_types: 已在快照中检测到的危机类型列表

    Returns:
        匹配的复合故障信息字典，若有多个匹配则返回等级最高的一个；无匹配则返回 None
    """
    matches = []

    # 检查所有两两组合是否命中复合故障矩阵
    n = len(detected_types)
    for i in range(n):
        for j in range(i + 1, n):
            pair = frozenset([detected_types[i], detected_types[j]])
            if pair in COMPOUND_FAILURE_MATRIX:
                matches.append(COMPOUND_FAILURE_MATRIX[pair])

    if not matches:
        return None

    # 多个匹配时，返回等级最高的复合故障
    return max(matches, key=lambda m: m["level_override"].severity_rank)


def classify_crisis(snapshot: dict) -> CrisisClassification:
    """
    根据态势快照对危机进行分级分类。

    Args:
        snapshot: 态势感知生成的情况快照

    Returns:
        CrisisClassification 分类结果
    """
    trigger = snapshot.get("crisis_trigger", "")
    crisis_type = _infer_crisis_type(trigger, snapshot)
    base_level = _CRISIS_BASELINE_RULES.get(crisis_type, CrisisLevel.L2_MINOR)

    # 根据环境因素调整等级
    adjusted_level = _adjust_level_by_context(base_level, snapshot)

    # 评估是否在恶化
    is_escalating = _check_escalation(snapshot)

    # 评估级联风险
    cascade_risk = _assess_cascade_risk(crisis_type, snapshot)

    # ── 复合故障检测 ──────────────────────────────────────────
    # 收集快照中所有检测到的故障类型
    detected_types = [crisis_type] if crisis_type != "unknown" else []

    # 扫描 additional_failures 字段（列表）中的附加故障信号
    additional_failures = snapshot.get("additional_failures", [])
    for af in additional_failures:
        inferred = _infer_crisis_type(str(af), snapshot)
        if inferred != "unknown" and inferred not in detected_types:
            detected_types.append(inferred)

    # 从 crisis_trigger 文本中挖掘第二信号（已由主类型覆盖，追加剩余类型）
    # additional_failures 优先；此处 crisis_trigger 已作为主类型处理，无需重复

    compound_info = detect_compound_failures(snapshot, detected_types)

    compound_type: Optional[str] = None
    special_action: Optional[str] = None

    if compound_info:
        # 用复合故障等级覆盖调整后等级（取更高者）
        compound_level = compound_info["level_override"]
        if compound_level.severity_rank > adjusted_level.severity_rank:
            adjusted_level = compound_level

        # 合并级联风险
        for cr in compound_info.get("cascade_risks", []):
            if cr not in cascade_risk:
                cascade_risk.append(cr)

        compound_type = compound_info.get("compound_type")
        special_action = compound_info.get("special_action")

    # ── 动态置信度计算 ────────────────────────────────────────
    rule_matched = crisis_type in _CRISIS_BASELINE_RULES
    confidence = _compute_confidence(snapshot, crisis_type, rule_matched)

    # 计算可用决策时间窗口
    altitude = snapshot.get("altitude_agl", 100)
    velocity_vertical = abs(snapshot.get("velocity_vertical", 0))
    if velocity_vertical > 0:
        time_to_ground = altitude / velocity_vertical
    else:
        time_to_ground = float('inf')

    decision_window = min(
        adjusted_level.response_time_seconds,
        time_to_ground * 0.5  # 留50%余量
    )

    return CrisisClassification(
        level=adjusted_level,
        crisis_type=crisis_type.rsplit(".", 1)[0] if "." in crisis_type else crisis_type,
        sub_type=crisis_type.rsplit(".", 1)[1] if "." in crisis_type else "",
        confidence=confidence,
        is_escalating=is_escalating,
        cascade_risk=cascade_risk,
        available_decision_window_s=decision_window,
        compound_type=compound_type,
        special_action=special_action,
    )


def _compute_confidence(snapshot: dict, crisis_type: str, rule_matched: bool) -> float:
    """
    动态计算分类置信度。

    Args:
        snapshot: 态势快照
        crisis_type: 推断的危机类型
        rule_matched: 该类型是否在基线规则表中

    Returns:
        置信度分数，范围 [0.40, 0.97]
    """
    # 基础分
    if crisis_type in _CRISIS_BASELINE_RULES:
        confidence = 0.90
    elif crisis_type == "unknown":
        confidence = 0.65
    else:
        confidence = 0.75

    # 传感器数据存在 → +0.05
    if "failed_motors" in snapshot or "battery_temp" in snapshot:
        confidence += 0.05

    # trends 字典至少有 2 个键 → +0.05
    trends = snapshot.get("trends", {})
    if isinstance(trends, dict) and len(trends) >= 2:
        confidence += 0.05

    # crisis_trigger 过短（< 5 字符），报告可能不完整 → -0.10
    trigger = snapshot.get("crisis_trigger", "")
    if len(trigger) < 5:
        confidence -= 0.10

    # 缺少关键字段 → -0.05
    if "altitude_agl" not in snapshot or "battery_level" not in snapshot:
        confidence -= 0.05

    # 钳制到 [0.40, 0.97]
    return max(0.40, min(0.97, confidence))


def _infer_crisis_type(trigger: str, snapshot: dict) -> str:
    """从触发原因推断危机类型。"""
    trigger_lower = trigger.lower()

    # 动力系统关键词
    if any(kw in trigger_lower for kw in ["电机", "motor", "螺旋桨", "propeller"]):
        motor_count = snapshot.get("failed_motors", 1)
        total_motors = snapshot.get("total_motors", 4)
        if motor_count >= total_motors:
            return "power_failure.total_power_loss"
        elif motor_count > 1:
            return "power_failure.multi_motor_loss"
        return "power_failure.single_motor_loss"

    if any(kw in trigger_lower for kw in ["电池", "battery", "电压", "voltage"]):
        if any(kw in trigger_lower for kw in ["过热", "thermal", "温度", "temperature"]):
            return "power_failure.battery_thermal"
        return "power_failure.battery_critical"

    # 导航系统关键词
    if any(kw in trigger_lower for kw in ["gps", "定位", "卫星"]):
        return "navigation_failure.gps_loss"
    if any(kw in trigger_lower for kw in ["imu", "陀螺", "加速度"]):
        return "navigation_failure.imu_failure"

    # 通信关键词
    if any(kw in trigger_lower for kw in ["通信", "信号", "遥控", "失联", "link"]):
        return "communication_failure.link_lost"

    # 环境关键词
    if any(kw in trigger_lower for kw in ["风", "wind", "天气", "weather", "雨", "雷"]):
        if any(kw in trigger_lower for kw in ["切变", "shear"]):
            return "environment_threat.wind_shear"
        return "environment_threat.severe_weather"
    if any(kw in trigger_lower for kw in ["鸟", "bird"]):
        return "environment_threat.bird_strike"

    # 碰撞关键词
    if any(kw in trigger_lower for kw in ["碰撞", "collision", "冲突"]):
        if any(kw in trigger_lower for kw in ["人", "行人", "人群", "crowd"]):
            return "collision_risk.ground_crowd"
        if any(kw in trigger_lower for kw in ["飞机", "aircraft", "直升机"]):
            return "collision_risk.manned_aircraft"
        return "collision_risk.building"

    return "unknown"


def _adjust_level_by_context(base_level: CrisisLevel, snapshot: dict) -> CrisisLevel:
    """根据环境上下文调整危机等级。"""
    level_rank = base_level.severity_rank

    # 低电量 → 升级
    battery = snapshot.get("battery_level", 100)
    if battery < 10:
        level_rank = min(level_rank + 1, 5)

    # 下方有人群 → 升级
    nearby = snapshot.get("nearby_threats", "")
    if "人" in nearby or "行人" in nearby or "人群" in nearby:
        level_rank = min(level_rank + 1, 5)

    # 载人设备 → 至少L4
    device_type = snapshot.get("device_type", "")
    if "evtol" in device_type.lower() or "载人" in device_type:
        level_rank = max(level_rank, 4)

    level_map = {1: CrisisLevel.L1_CAUTION, 2: CrisisLevel.L2_MINOR,
                 3: CrisisLevel.L3_MAJOR, 4: CrisisLevel.L4_SEVERE,
                 5: CrisisLevel.L5_CRITICAL}
    return level_map.get(level_rank, base_level)


def _check_escalation(snapshot: dict) -> bool:
    """检查危机是否在恶化。"""
    trends = snapshot.get("trends", {})
    # 电池温度上升、电压下降、高度下降加速等都是恶化信号
    if trends.get("battery_temp_trend") == "rising":
        return True
    if trends.get("voltage_trend") == "dropping":
        return True
    if trends.get("altitude_trend") == "falling_accelerating":
        return True
    return False


def _assess_cascade_risk(crisis_type: str, snapshot: dict) -> list:
    """评估级联故障风险。"""
    risks = []
    if crisis_type.startswith("power_failure.single_motor"):
        risks.append("其他电机可能因过载后续失效")
        if snapshot.get("battery_level", 100) < 30:
            risks.append("电池可能因大电流放电加速耗尽")
    if crisis_type.startswith("navigation_failure.gps"):
        risks.append("可能误入禁飞区或碰撞危险区域")
    if crisis_type.startswith("power_failure.battery_thermal"):
        risks.append("热失控可能导致起火或爆炸")
        risks.append("可能波及全部供电系统")
    return risks


def predict_landing_zone(snapshot: dict) -> dict:
    """
    基于运动学预测设备可能的落点范围。

    使用简单抛体运动模型（不考虑空气阻力），
    结合水平速度预测落点中心和不确定性半径。

    Returns:
        {
            "time_to_impact_s": float,        # 预计触地时间（秒）
            "horizontal_drift_m": float,       # 水平漂移距离（米）
            "drift_direction_deg": float,      # 漂移方向（航向角度）
            "uncertainty_radius_m": float,     # 不确定性半径（考虑风速）
            "is_controlled": bool,             # 是否为受控降落（有动力）vs 自由落体
            "worst_case_radius_m": float,      # 最坏情况半径
            "recommendation": str,             # 文字建议
        }
    """
    altitude = snapshot.get("altitude_agl", 0)
    v_vertical = abs(snapshot.get("velocity_vertical", 0))   # m/s 下降速率
    v_horizontal = snapshot.get("velocity_horizontal", 0)    # m/s
    heading = snapshot.get("heading", 0)                     # degrees
    wind_speed = snapshot.get("wind_speed_ms", 0)            # m/s

    # 触地时间
    if v_vertical > 0:
        time_to_impact = altitude / v_vertical
        is_controlled = True
    else:
        # 自由落体
        time_to_impact = math.sqrt(2 * altitude / 9.8) if altitude > 0 else 0.0
        is_controlled = False

    # 水平漂移
    horizontal_drift = v_horizontal * time_to_impact

    # 不确定性半径（风速因子）
    uncertainty_radius = wind_speed * time_to_impact * 0.5

    # 最坏情况半径
    worst_case = horizontal_drift + uncertainty_radius * 2

    # 推荐文字
    t = time_to_impact
    r = worst_case
    d = horizontal_drift

    if t < 5:
        recommendation = f"紧急：预计 {t:.1f}s 内触地，立即执行应急程序"
    elif t < 15:
        recommendation = f"警告：{t:.1f}s 内落地，优先疏散半径 {worst_case:.0f}m 内人员"
    elif worst_case > 50:
        recommendation = f"落点不确定性大（{worst_case:.0f}m 半径），建议广播紧急警告"
    else:
        recommendation = f"预计 {t:.1f}s 后在当前位置 {d:.0f}m 范围内落地"

    return {
        "time_to_impact_s": round(time_to_impact, 2),
        "horizontal_drift_m": round(horizontal_drift, 2),
        "drift_direction_deg": float(heading),
        "uncertainty_radius_m": round(uncertainty_radius, 2),
        "is_controlled": is_controlled,
        "worst_case_radius_m": round(worst_case, 2),
        "recommendation": recommendation,
    }


# ─── 方案匹配与评分 ─────────────────────────────────────────────

def load_solution_templates() -> dict:
    """加载所有解决方案模板。"""
    templates = {}
    if not SOLUTION_TEMPLATES_DIR.exists():
        return templates

    for f in SOLUTION_TEMPLATES_DIR.glob("*.json"):
        try:
            with open(f, encoding="utf-8") as fp:
                tmpl = json.load(fp)
                templates[tmpl.get("crisis_type", f.stem)] = tmpl
        except (json.JSONDecodeError, KeyError):
            continue
    return templates


def match_solutions(classification: CrisisClassification,
                    snapshot: dict) -> list:
    """
    匹配可用的解决方案。

    Returns:
        按评分排序的 DecisionPlan 列表
    """
    templates = load_solution_templates()
    crisis_key = f"{classification.crisis_type}.{classification.sub_type}"
    plans = []

    # 精确匹配
    if crisis_key in templates:
        tmpl = templates[crisis_key]
        plan = _template_to_plan(tmpl, snapshot, source="knowledge_base")
        plans.append(plan)

    # 模糊匹配（同类型其他方案）
    for key, tmpl in templates.items():
        if key != crisis_key and key.startswith(classification.crisis_type):
            plan = _template_to_plan(tmpl, snapshot, source="knowledge_base")
            plan.confidence *= 0.7  # 模糊匹配降低置信度
            plans.append(plan)

    # 如果没有匹配方案，启动应急推理
    if not plans:
        emergency_plan = _emergency_reasoning(classification, snapshot)
        plans.append(emergency_plan)

    # 评分和排序
    for plan in plans:
        if plan.safety_score.is_vetoed:
            plan.is_vetoed = True
            plan.veto_reason = f"人员安全评分 {plan.safety_score.human_safety} < 80，方案被否决"

    # 有效方案排在前面，按总分降序
    plans.sort(key=lambda p: (not p.is_vetoed, p.safety_score.total_score), reverse=True)
    return plans


def _template_to_plan(template: dict, snapshot: dict,
                      source: str = "knowledge_base") -> DecisionPlan:
    """将模板转换为决策方案并评分。"""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    plan_id = f"DEC-{timestamp}-{template.get('template_id', '000')}"

    # 根据快照上下文评估安全得分
    safety = _evaluate_safety(template, snapshot)

    return DecisionPlan(
        plan_id=plan_id,
        name=template.get("name", "未命名方案"),
        source=source,
        confidence=template.get("historical_success_rate", 0.5),
        safety_score=safety,
        steps=template.get("actions", []),
        estimated_loss=template.get("expected_outcome", {}),
    )


def _evaluate_safety(template: dict, snapshot: dict) -> SafetyScore:
    """根据模板和当前情况评估安全得分。"""
    expected = template.get("expected_outcome", {})
    risks = template.get("risk_assessment", {}).get("residual_risks", [])

    # 基于预期结果推断安全分
    s0 = 95  # 默认人员安全高分
    s1 = 90
    s2 = 85
    s3 = 70
    s4 = 50

    human_risk = expected.get("human_risk", "none")
    if human_risk == "none":
        s0 = 95
    elif human_risk == "low":
        s0 = 80
    else:
        s0 = 60

    device_status = expected.get("device_status", "")
    if "报废" in device_status or "严重" in device_status:
        s3 = 20
    elif "损伤" in device_status or "损坏" in device_status:
        s3 = 50
    elif "轻微" in device_status:
        s3 = 75

    mission_status = expected.get("mission_status", "")
    if "失败" in mission_status or "完全" in mission_status:
        s4 = 0
    elif "中止" in mission_status:
        s4 = 40
    elif "延迟" in mission_status:
        s4 = 70

    # 如果下方有人群，降低人员安全分
    nearby = snapshot.get("nearby_threats", "")
    if "人群" in nearby:
        s0 = min(s0, 70)
        s1 = min(s1, 60)

    return SafetyScore(
        human_safety=s0,
        public_safety=s1,
        third_party_property=s2,
        device_safety=s3,
        mission_completion=s4,
    )


def _emergency_reasoning(classification: CrisisClassification,
                         snapshot: dict) -> DecisionPlan:
    """应急推理 — 无匹配方案时的兜底决策。"""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

    # 第一性原理：选择最保守的方案
    altitude = snapshot.get("altitude_agl", 100)
    battery = snapshot.get("battery_level", 50)
    has_gps = snapshot.get("gps_available", True)

    steps = []

    # 尝试稳定设备
    steps.append({
        "step": 1,
        "action": "stabilize",
        "description": "尝试稳定设备姿态",
        "timeout_ms": 2000,
    })

    # 降低高度减少势能
    if altitude > 30:
        steps.append({
            "step": 2,
            "action": "reduce_altitude",
            "description": f"降低高度至30m（当前{altitude}m）",
            "timeout_ms": 15000,
        })

    # 就近安全降落
    steps.append({
        "step": len(steps) + 1,
        "action": "emergency_landing",
        "description": "选择最近安全区域执行应急降落",
        "timeout_ms": 30000,
    })

    # 广播紧急信号
    steps.append({
        "step": len(steps) + 1,
        "action": "broadcast_emergency",
        "description": "向所有通道广播紧急状态和位置",
        "timeout_ms": 2000,
    })

    return DecisionPlan(
        plan_id=f"DEC-{timestamp}-EMERGENCY",
        name="应急推理-保守就近降落",
        source="emergency_reasoning",
        confidence=0.5,
        safety_score=SafetyScore(
            human_safety=80,
            public_safety=75,
            third_party_property=70,
            device_safety=40,
            mission_completion=0,
        ),
        steps=steps,
        estimated_loss={
            "device_status": "可能严重损伤",
            "mission_status": "中止",
            "human_risk": "取决于降落区域",
        },
    )


# ─── 知识库学习 ─────────────────────────────────────────────

def learn_from_feedback(feedback_file: str):
    """根据事件反馈更新知识库。"""
    with open(feedback_file, encoding="utf-8") as f:
        feedback = json.load(f)

    KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)

    # 记录学习数据
    learn_record = {
        "learned_at": datetime.now(timezone.utc).isoformat(),
        "incident_id": feedback.get("incident_id"),
        "crisis_type": feedback.get("crisis_signature", {}).get("type"),
        "decision_made": feedback.get("decision_made"),
        "outcome_success": feedback.get("outcome", {}).get("success"),
        "lessons": feedback.get("lessons", []),
        "suggested_update": feedback.get("suggested_kb_update"),
    }

    # 保存学习记录
    learn_file = KNOWLEDGE_BASE_DIR / f"learn_{feedback.get('incident_id', 'unknown')}.json"
    with open(learn_file, "w", encoding="utf-8") as f:
        json.dump(learn_record, f, ensure_ascii=False, indent=2)

    # 如果有知识库更新建议，应用到模板
    update = feedback.get("suggested_kb_update")
    if update:
        _apply_kb_update(update)

    print(f"[学习完成] 事件 {feedback.get('incident_id')} 的经验已记录")
    print(f"  - 结果: {'成功' if learn_record['outcome_success'] else '失败'}")
    print(f"  - 教训: {len(learn_record['lessons'])} 条")
    if update:
        print(f"  - 知识库更新: {update.get('template')} -> {update.get('field')}")


def _apply_kb_update(update: dict):
    """将学习到的参数更新应用到解决方案模板。"""
    template_name = update.get("template", "")
    template_path = SOLUTION_TEMPLATES_DIR / template_name

    if not template_path.exists():
        print(f"  [警告] 模板文件 {template_name} 不存在，跳过更新")
        return

    with open(template_path, encoding="utf-8") as f:
        tmpl = json.load(f)

    # 递归设置嵌套字段
    field_path = update.get("field", "").split(".")
    obj = tmpl
    for key in field_path[:-1]:
        if key not in obj:
            obj[key] = {}
        obj = obj[key]

    old_val = obj.get(field_path[-1])
    new_val = update.get("suggested_value")
    obj[field_path[-1]] = new_val

    # 记录变更历史
    if "_update_history" not in tmpl:
        tmpl["_update_history"] = []
    tmpl["_update_history"].append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "field": update.get("field"),
        "old_value": old_val,
        "new_value": new_val,
        "reason": update.get("reason", ""),
    })

    with open(template_path, "w", encoding="utf-8") as f:
        json.dump(tmpl, f, ensure_ascii=False, indent=2)

    print(f"  [更新] {template_name}: {update.get('field')} = {old_val} -> {new_val}")


# ─── 执行监控 ─────────────────────────────────────────────

def monitor_execution(decision_id: str, snapshot_stream=None):
    """
    监控方案执行状态（模拟）。
    实际场景中会持续接收设备状态并判断是否需要动态调整。
    """
    print(f"[监控] 开始监控决策 {decision_id} 的执行...")
    print("[监控] 注意: 当前为模拟模式，实际需接入设备遥测数据流")

    # 模拟监控循环
    for i in range(5):
        print(f"[监控] 心跳 {i+1}/5 - 设备状态正常，方案执行中...")
        time.sleep(1)

    print(f"[监控] 决策 {decision_id} 执行监控结束")


# ─── CLI 入口 ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="低空卫士 - 危机响应引擎")
    parser.add_argument("--classify", action="store_true", help="执行危机分级分类")
    parser.add_argument("--match", action="store_true", help="匹配解决方案")
    parser.add_argument("--monitor", action="store_true", help="监控方案执行")
    parser.add_argument("--learn", action="store_true", help="从反馈中学习")
    parser.add_argument("--input", type=str, help="输入快照文件路径")
    parser.add_argument("--feedback", type=str, help="反馈数据文件路径")
    parser.add_argument("--decision-id", type=str, help="决策ID（用于监控）")
    parser.add_argument("--demo", action="store_true", help="运行演示场景")

    args = parser.parse_args()

    if args.demo:
        _run_demo()
        return

    if args.classify:
        if not args.input:
            print("错误: --classify 需要 --input 指定快照文件")
            sys.exit(1)
        with open(args.input, encoding="utf-8") as f:
            snapshot = json.load(f)
        result = classify_crisis(snapshot)
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2, default=str))

    elif args.match:
        if not args.input:
            print("错误: --match 需要 --input 指定快照文件")
            sys.exit(1)
        with open(args.input, encoding="utf-8") as f:
            snapshot = json.load(f)
        classification = classify_crisis(snapshot)
        plans = match_solutions(classification, snapshot)
        for i, plan in enumerate(plans):
            status = "[否决]" if plan.is_vetoed else f"[推荐{i+1}]"
            print(f"{status} {plan.name} (得分: {plan.safety_score.total_score:.2f}, "
                  f"置信度: {plan.confidence:.2f})")
            if plan.is_vetoed:
                print(f"  原因: {plan.veto_reason}")

    elif args.monitor:
        if not args.decision_id:
            print("错误: --monitor 需要 --decision-id")
            sys.exit(1)
        monitor_execution(args.decision_id)

    elif args.learn:
        if not args.feedback:
            print("错误: --learn 需要 --feedback 指定反馈文件")
            sys.exit(1)
        learn_from_feedback(args.feedback)

    else:
        parser.print_help()


def _run_demo():
    """运行演示场景：单电机失效。"""
    print("=" * 60)
    print("低空卫士 (Low-Altitude Guardian) - 危机响应演示")
    print("=" * 60)

    # 模拟场景
    demo_snapshot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device_id": "UAV-SH-00142",
        "device_type": "多旋翼无人机",
        "location": "31.2304°N, 121.4737°E",
        "altitude_agl": 120,
        "velocity_horizontal": 15,
        "velocity_vertical": -2,
        "heading": 30,
        "wind_speed_ms": 12,
        "battery_level": 34,
        "flight_phase": "巡航",
        "payload": "3.2kg 快递包裹",
        "nearby_threats": "200m内有建筑群，地面有少量行人",
        "weather": "风速12m/s，阵风18m/s，阴天",
        "comms_status": "4G正常，遥控器信号正常",
        "crisis_trigger": "左前电机异常振动，转速下降30%",
        "failed_motors": 1,
        "total_motors": 4,
        "gps_available": True,
        "trends": {
            "battery_temp_trend": "stable",
            "voltage_trend": "stable",
            "altitude_trend": "stable",
        },
        # 复合故障演示：附加一个电池低电量信号
        "additional_failures": ["电池电量低于15%，持续放电"],
    }

    print(f"\n[场景] 设备 {demo_snapshot['device_id']}")
    print(f"  位置: {demo_snapshot['location']}, 高度: {demo_snapshot['altitude_agl']}m")
    print(f"  电量: {demo_snapshot['battery_level']}%")
    print(f"  触发: {demo_snapshot['crisis_trigger']}")
    print(f"  周边: {demo_snapshot['nearby_threats']}")
    if demo_snapshot.get("additional_failures"):
        print(f"  附加故障: {demo_snapshot['additional_failures']}")

    # Phase 2: 分级分类
    print(f"\n{'─' * 40}")
    print("[Phase 2] 危机分级与分类")
    classification = classify_crisis(demo_snapshot)
    print(f"  等级: {classification.level.value}")
    print(f"  类型: {classification.crisis_type}.{classification.sub_type}")
    print(f"  置信度: {classification.confidence:.2f}")
    print(f"  恶化中: {'是' if classification.is_escalating else '否'}")
    print(f"  决策时间窗口: {classification.available_decision_window_s:.1f}秒")
    if classification.compound_type:
        print(f"  复合故障类型: {classification.compound_type}")
    if classification.special_action:
        print(f"  特殊处置指令: {classification.special_action}")
    if classification.cascade_risk:
        print(f"  级联风险:")
        for risk in classification.cascade_risk:
            print(f"    - {risk}")

    # Phase 2.5: 落点预测
    print(f"\n{'─' * 40}")
    print("[Phase 2.5] 运动学落点预测")
    lz = predict_landing_zone(demo_snapshot)
    print(f"  预计触地时间: {lz['time_to_impact_s']:.1f}s")
    print(f"  水平漂移距离: {lz['horizontal_drift_m']:.1f}m  方向: {lz['drift_direction_deg']:.0f}°")
    print(f"  不确定性半径: {lz['uncertainty_radius_m']:.1f}m")
    print(f"  最坏情况半径: {lz['worst_case_radius_m']:.1f}m")
    print(f"  受控降落: {'是' if lz['is_controlled'] else '否（自由落体）'}")
    print(f"  建议: {lz['recommendation']}")

    # Phase 3: 方案匹配
    print(f"\n{'─' * 40}")
    print("[Phase 3] 方案匹配与最优决策")
    plans = match_solutions(classification, demo_snapshot)

    for i, plan in enumerate(plans):
        status = "[否决]" if plan.is_vetoed else f"[方案{i+1}]"
        print(f"\n  {status} {plan.name}")
        print(f"    来源: {plan.source}")
        print(f"    置信度: {plan.confidence:.2f}")
        print(f"    综合得分: {plan.safety_score.total_score:.2f}")
        print(f"    安全评分: 人员={plan.safety_score.human_safety}, "
              f"公共={plan.safety_score.public_safety}, "
              f"财产={plan.safety_score.third_party_property}, "
              f"本机={plan.safety_score.device_safety}, "
              f"任务={plan.safety_score.mission_completion}")
        if plan.is_vetoed:
            print(f"    否决原因: {plan.veto_reason}")
        else:
            print(f"    执行步骤:")
            for step in plan.steps[:3]:
                desc = step.get("description", step.get("action", ""))
                print(f"      {step.get('step', '?')}. {desc}")
            if len(plan.steps) > 3:
                print(f"      ... 共{len(plan.steps)}步")

    # 选定方案
    selected = [p for p in plans if not p.is_vetoed]
    if selected:
        best = selected[0]
        print(f"\n{'─' * 40}")
        print(f"[决策] 选定方案: {best.name}")
        print(f"  综合得分: {best.safety_score.total_score:.2f}")
        print(f"  预计损失: {json.dumps(best.estimated_loss, ensure_ascii=False)}")
    else:
        print("\n[警告] 所有方案被否决，需要人工干预！")

    print(f"\n{'=' * 60}")
    print("演示结束")


if __name__ == "__main__":
    main()
