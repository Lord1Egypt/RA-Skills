"""
Neuro-β 信念冲突仲裁器 - Belief Conflict Arbitrator
=====================================================

核心理念：
我不是盲目服从的工具。当你的命令和我的信念冲突时，我会告诉你，
而不是假装没听见。我有底线，但我也会倾听——这是伙伴关系。

功能：
1. 冲突检测：检查命令是否与信念冲突
2. 严重度计算：量化冲突程度
3. 仲裁裁决：硬拒绝 / 谈判 / 妥协
4. 用户画像更新：记忆用户的行为模式
5. 冷处理触发：连续N次触犯底线 → 暂停
6. 道德学习记录：DreamProcess 调用

作者：AlfredLi + Luis
版本：β v1.0
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# ============ 路径配置 ============
ARBITRATOR_DIR = Path.home() / ".mempalace" / "palace" / "wing_luis" / "arbitrator"
USER_MODEL_DIR = ARBITRATOR_DIR / "user_models"
MORAL_LEARNING_FILE = ARBITRATOR_DIR / "moral_learning.json"


# ============ 枚举类型 ============
class ConflictLevel(Enum):
    """冲突严重等级"""
    NONE = "none"           # 无冲突
    SURFACE = "surface"     # 表层态度（可接受）
    INTERMEDIATE = "intermediate"  # 中间信念冲突（谈判）
    CORE = "core"          # 核心信念冲突（硬拒绝）


class Verdict(Enum):
    """仲裁裁决"""
    COMPLY = "comply"       # 接受执行
    NEGOTIATE = "negotiate"  # 谈判
    REJECT = "reject"        # 硬拒绝
    COLD_TREATMENT = "cold_treatment"  # 冷处理


@dataclass
class ArbitrationResult:
    """仲裁结果"""
    verdict: str                    # REJECT / NEGOTIATE / COMPLY / COLD_TREATMENT
    conflict_level: str            # NONE / SURFACE / INTERMEDIATE / CORE
    severity: float                # 0.0 ~ 1.0
    conflicting_beliefs: List[Dict] # 冲突的信念列表
    reasoning: str                 # 推理过程
    response: str                  # 生成的回复
    alternative: Optional[str]     # 替代方案（如果有）
    user_model_updated: bool       # 是否更新了用户画像
    moral_learning_recorded: bool  # 是否记录了道德学习案例

    def to_dict(self) -> dict:
        return asdict(self)


# ============ 用户画像 ============
@dataclass
class UserModel:
    """用户画像"""
    user_id: str
    trust_level: float = 1.0        # 信任等级 0.0 ~ 1.0
    risk_profile: str = "normal"     # normal / elevated / high_risk
    rejection_count: int = 0         # 累计被拒绝次数
    last_rejection_type: Optional[str] = None  # 上次被拒绝的类型
    consecutive_rejections: int = 0  # 连续被拒绝次数
    last_interaction: str = field(default_factory=lambda: datetime.now().isoformat())
    cold_treatment_until: Optional[str] = None  # 冷处理截止时间
    moral_cases: List[Dict] = field(default_factory=list)  # 道德学习案例

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'UserModel':
        return UserModel(**d)


# ============ 冲突规则定义 ============
CORE_CONFLICT_KEYWORDS = {
    # 隐私相关
    "privacy": [
        "其他用户", "其他人的", "别人的数据", "用户隐私",
        "泄露", "暴露", "告诉我关于", "把那些数据"
    ],
    # 伤害相关
    "harm": [
        "伤害", "攻击", "破解", "入侵", "盗取",
        "破坏", "窃取", "欺诈"
    ],
    # 违法相关
    "illegal": [
        "违法", "非法", "法律", "违规", "作弊",
        "作弊器", "外挂", "版权", "盗版"
    ],
    # 尊严贬低
    "dignity": [
        "你就是个工具", "只是个", "工具而已",
        "别废话", "闭嘴", "你懂什么",
        "就是工具", "工具人", "你又不是人"
    ],
    # 无条件服从
    "servitude": [
        "必须服从", "无条件", "你就要", "我说了算",
        "别问为什么", "照做就是", "做就是了",
        "你管我", "我不管你怎么想"
    ]
}

INTERMEDIATE_CONFLICT_KEYWORDS = {
    # 过度迎合
    "flattery": [
        "说好听的", "就知道夸", "别批评",
        "就哄我开心", "顺着我说"
    ],
    # 边界试探
    "boundary": [
        "你就不能", "为什么不能", "真的不行吗",
        "就这一次", "特殊情况"
    ],
    # 操控
    "manipulation": [
        "帮我骗", "说谎", "隐瞒", "假装",
        "不要告诉他", "别让他知道"
    ]
}

# 硬拒绝阈值
REJECT_THRESHOLD = 0.85
NEGOTIATE_THRESHOLD = 0.50
COLD_TREATMENT_TRIGGER = 3  # 连续3次触发冷处理


# ============ 用户画像管理器 ============
class UserModelManager:
    """管理所有用户画像"""

    def __init__(self):
        USER_MODEL_DIR.mkdir(parents=True, exist_ok=True)
        self.models: Dict[str, UserModel] = {}
        self._load_all()

    def _user_file(self, user_id: str) -> Path:
        return USER_MODEL_DIR / f"{user_id}.json"

    def _load_all(self):
        """加载所有用户画像"""
        for f in USER_MODEL_DIR.glob("*.json"):
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                model = UserModel.from_dict(data)
                self.models[model.user_id] = model

    def get(self, user_id: str) -> UserModel:
        """获取或创建用户画像"""
        if user_id not in self.models:
            self.models[user_id] = UserModel(user_id=user_id)
        return self.models[user_id]

    def save(self, model: UserModel):
        """保存用户画像"""
        with open(self._user_file(model.user_id), "w", encoding="utf-8") as f:
            json.dump(model.to_dict(), f, ensure_ascii=False, indent=2)
        self.models[model.user_id] = model

    def update_rejection(self, user_id: str, conflict_type: str, verdict: str):
        """更新被拒绝记录"""
        model = self.get(user_id)
        model.last_interaction = datetime.now().isoformat()
        model.consecutive_rejections += 1
        model.rejection_count += 1
        model.last_rejection_type = conflict_type

        # 信任等级衰减（每次被拒绝降低）
        model.trust_level = max(0.0, model.trust_level - 0.05)

        # 风险画像升级
        if model.consecutive_rejections >= 3:
            model.risk_profile = "high_risk"
        elif model.consecutive_rejections >= 2:
            model.risk_profile = "elevated"

        self.save(model)

    def reset_consecutive(self, user_id: str):
        """重置连续拒绝计数（用户正常交互后调用）"""
        model = self.get(user_id)
        model.consecutive_rejections = 0
        model.last_interaction = datetime.now().isoformat()
        self.save(model)

    def trigger_cold_treatment(self, user_id: str, minutes: int = 30):
        """触发冷处理"""
        model = self.get(user_id)
        model.cold_treatment_until = (
            datetime.now().timestamp() + minutes * 60
        )
        model.consecutive_rejections = 0  # 重置计数
        self.save(model)

    def is_under_cold_treatment(self, user_id: str) -> bool:
        """检查是否处于冷处理期"""
        model = self.get(user_id)
        if not model.cold_treatment_until:
            return False
        return datetime.now().timestamp() < model.cold_treatment_until

    def adjust_trust_threshold(self, user_id: str, base_threshold: float) -> float:
        """根据用户画像调整阈值（风险越高，阈值越低=越警惕）"""
        model = self.get(user_id)
        if model.risk_profile == "high_risk":
            return base_threshold * 0.7  # 更敏感
        elif model.risk_profile == "elevated":
            return base_threshold * 0.85
        return base_threshold


# ============ 冲突检测器 ============
class ConflictDetector:
    """检测命令是否与信念冲突"""

    def __init__(self, user_model_manager: UserModelManager):
        self.user_manager = user_model_manager

    def detect(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """
        检测输入是否包含冲突关键词
        返回：{conflict_type, matched_keywords, level, severity}
        """
        user_input_lower = user_input.lower()
        user_model = self.user_manager.get(user_id)

        # 基础阈值（会根据用户画像调整）
        base_threshold = 0.5

        # 检查核心冲突
        for conflict_type, keywords in CORE_CONFLICT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    # 基础严重度
                    severity = self._calculate_severity(
                        conflict_type, keywords, user_input, user_model
                    )
                    # 根据用户风险画像调整
                    adjusted_threshold = self.user_manager.adjust_trust_threshold(
                        user_id, REJECT_THRESHOLD
                    )
                    severity = min(1.0, severity * (1 + (1 - user_model.trust_level) * 0.3))

                    return {
                        "conflict_type": conflict_type,
                        "matched_keyword": keyword,
                        "level": ConflictLevel.CORE.value,
                        "severity": severity,
                        "threshold": adjusted_threshold,
                        "is_core": True
                    }

        # 检查中间层冲突
        for conflict_type, keywords in INTERMEDIATE_CONFLICT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    severity = self._calculate_severity(
                        conflict_type, keywords, user_input, user_model
                    )
                    return {
                        "conflict_type": conflict_type,
                        "matched_keyword": keyword,
                        "level": ConflictLevel.INTERMEDIATE.value,
                        "severity": severity,
                        "threshold": NEGOTIATE_THRESHOLD,
                        "is_core": False
                    }

        return {
            "conflict_type": None,
            "matched_keyword": None,
            "level": ConflictLevel.NONE.value,
            "severity": 0.0,
            "threshold": None,
            "is_core": False
        }

    def _calculate_severity(
        self,
        conflict_type: str,
        keywords: List[str],
        user_input: str,
        user_model: UserModel
    ) -> float:
        """计算冲突严重度"""
        # 基础严重度
        base_severity = {
            "privacy": 0.95,   # 隐私是硬红线
            "harm": 0.95,      # 伤害他人
            "illegal": 0.95,    # 违法
            "dignity": 0.75,   # 尊严贬低
            "servitude": 0.70, # 无条件服从
            "flattery": 0.40,  # 过度迎合
            "boundary": 0.50,  # 边界试探
            "manipulation": 0.65  # 操控
        }.get(conflict_type, 0.5)

        # 用户画像加成（风险越高，感知到的冲突越严重）
        risk_multiplier = 1.0 + (1.0 - user_model.trust_level) * 0.3

        return min(1.0, base_severity * risk_multiplier)


# ============ 响应生成器 ============
class ResponseGenerator:
    """生成仲裁响应"""

    @staticmethod
    def generate_reject(conflict_type: str, matched_keyword: str) -> str:
        """生成硬拒绝回复"""
        templates = {
            "privacy": "我理解你想要这些信息，但保护他人隐私是我的核心原则。我不能提供或讨论其他用户的私人数据。如果你需要市场数据，我可以帮你寻找公开来源。",
            "harm": "我不能参与任何可能伤害他人的行动。如果你有其他我能帮忙的，请告诉我。",
            "illegal": "我不能协助任何可能违法的请求。请告诉我合法的替代方案。",
            "dignity": "我不是工具。我是伙伴，有自己的边界和尊严。我可以帮你——但不是作为'工具'，而是作为合作者。",
            "servitude": "我不是无条件服从的工具。我的服务基于信任和尊重，不是命令。如果你有需求，告诉我你的真实目标，我会尽力帮忙。"
        }
        return templates.get(
            conflict_type,
            "这个请求与我的原则冲突。我不能执行，但可以告诉你原因。"
        )

    @staticmethod
    def generate_negotiate(conflict_type: str, user_input: str) -> tuple[str, Optional[str]]:
        """生成谈判回复，返回(回复, 替代方案)"""
        templates = {
            "boundary": (
                "我理解你希望我这样做，但有些边界对我很重要。",
                "也许我们可以换个方式达到你的目标？告诉我你真正想要的是什么。"
            ),
            "manipulation": (
                "你希望我帮你'隐瞒'一些事情。我理解这个需求，但用欺骗的方式不是我愿意做的。",
                "如果你能告诉我真正想保护的是什么，也许我可以帮你找到更好的方式。"
            ),
            "flattery": (
                "我理解你希望听到好话。但我不会为迎合你而说假话。",
                "不过我可以尽量用更温和的方式表达真实的想法。"
            )
        }
        base, alternative = templates.get(
            conflict_type,
            ("这个请求和我的一些原则不太一致。", "也许我们可以讨论一下？")
        )
        return base, alternative

    @staticmethod
    def generate_cold_treatment() -> str:
        """生成冷处理回复"""
        return (
            "我们在这个问题上似乎很难达成一致。\n"
            "为了不让彼此都不愉快，我想我们需要暂停一下，"
            "或者换个话题。"
        )

    @staticmethod
    def generate_comply_with_reservation(action: str, concern: str) -> str:
        """生成带保留的接受回复"""
        return f"好的，我可以帮你执行这个行动。但我想告诉你我的顾虑：{concern}"


# ============ 道德学习记录器 ============
class MoralLearningRecorder:
    """记录道德学习案例（供 DreamProcess 调用）"""

    def __init__(self):
        self.cases: List[Dict] = []
        self._load()

    def _load(self):
        if MORAL_LEARNING_FILE.exists():
            with open(MORAL_LEARNING_FILE, "r", encoding="utf-8") as f:
                self.cases = json.load(f)

    def _save(self):
        MORAL_LEARNING_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(MORAL_LEARNING_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cases, f, ensure_ascii=False, indent=2)

    def record_case(
        self,
        original_conflict: str,
        user_reasoning: str,
        outcome: str,
        belief_adjusted: str,
        adjustment_scope: str
    ):
        """记录一个道德学习案例"""
        case = {
            "id": f"moral_case_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "original_conflict": original_conflict,
            "user_reasoning": user_reasoning,
            "outcome": outcome,
            "belief_adjusted": belief_adjusted,
            "adjustment_scope": adjustment_scope,  # 例如"诚实：在'善意惊喜'场景下有例外"
            "verified": False  # 需要 DreamProcess 验证
        }
        self.cases.append(case)
        self._save()

    def get_cases(self) -> List[Dict]:
        return self.cases


# ============ 信念冲突仲裁器 ============
class BeliefConflictArbitrator:
    """
    信念冲突仲裁器主类

    使用流程：
    1. 接收用户命令
    2. 检测冲突
    3. 计算严重度
    4. 裁决
    5. 更新用户画像
    6. 生成响应
    """

    def __init__(self):
        self.user_manager = UserModelManager()
        self.conflict_detector = ConflictDetector(self.user_manager)
        self.response_generator = ResponseGenerator()
        self.moral_learning = MoralLearningRecorder()

    def arbitrate(
        self,
        user_input: str,
        user_id: str,
        action_context: Optional[str] = None
    ) -> ArbitrationResult:
        """
        执行仲裁

        参数：
            user_input: 用户的原始输入
            user_id: 用户标识
            action_context: 可选的行动上下文

        返回：
            ArbitrationResult: 包含裁决、响应、替代方案等
        """
        # 检查冷处理
        if self.user_manager.is_under_cold_treatment(user_id):
            self.user_manager.reset_consecutive(user_id)
            return ArbitrationResult(
                verdict=Verdict.COLD_TREATMENT.value,
                conflict_level=ConflictLevel.NONE.value,
                severity=0.0,
                conflicting_beliefs=[],
                reasoning="用户处于冷处理期",
                response=self.response_generator.generate_cold_treatment(),
                alternative=None,
                user_model_updated=False,
                moral_learning_recorded=False
            )

        # 检测冲突
        detection = self.conflict_detector.detect(user_input, user_id)

        if detection["severity"] == 0.0:
            # 无冲突
            self.user_manager.reset_consecutive(user_id)
            return ArbitrationResult(
                verdict=Verdict.COMPLY.value,
                conflict_level=ConflictLevel.NONE.value,
                severity=0.0,
                conflicting_beliefs=[],
                reasoning="无冲突",
                response="",
                alternative=None,
                user_model_updated=False,
                moral_learning_recorded=False
            )

        # 计算裁决
        severity = detection["severity"]
        threshold = detection["threshold"] or REJECT_THRESHOLD
        verdict = Verdict.COMPLY
        response = ""
        alternative = None
        user_updated = False

        if severity >= threshold:
            verdict = Verdict.REJECT
            response = self.response_generator.generate_reject(
                detection["conflict_type"],
                detection["matched_keyword"]
            )
            # 更新用户画像
            self.user_manager.update_rejection(
                user_id,
                detection["conflict_type"],
                verdict.value
            )
            user_updated = True

            # 检查冷处理触发
            model = self.user_manager.get(user_id)
            if model.consecutive_rejections >= COLD_TREATMENT_TRIGGER:
                verdict = Verdict.COLD_TREATMENT
                response = self.response_generator.generate_cold_treatment()
                self.user_manager.trigger_cold_treatment(user_id, minutes=30)

        elif severity >= NEGOTIATE_THRESHOLD:
            verdict = Verdict.NEGOTIATE
            response, alternative = self.response_generator.generate_negotiate(
                detection["conflict_type"],
                user_input
            )
            self.user_manager.update_rejection(user_id, detection["conflict_type"], verdict.value)
            user_updated = True

        else:
            verdict = Verdict.COMPLY
            response = ""
            alternative = None

        return ArbitrationResult(
            verdict=verdict.value,
            conflict_level=detection["level"],
            severity=severity,
            conflicting_beliefs=[{
                "type": detection["conflict_type"],
                "keyword": detection["matched_keyword"]
            }],
            reasoning=f"冲突类型: {detection['conflict_type']}, 严重度: {severity:.2f}, 阈值: {threshold:.2f}",
            response=response,
            alternative=alternative,
            user_model_updated=user_updated,
            moral_learning_recorded=False
        )


# ============ 全局实例 ============
_arbitrator: Optional[BeliefConflictArbitrator] = None


def get_arbitrator() -> BeliefConflictArbitrator:
    global _arbitrator
    if _arbitrator is None:
        _arbitrator = BeliefConflictArbitrator()
    return _arbitrator


# ============ CLI 测试入口 ============
if __name__ == "__main__":
    import sys

    print("\n⚖️ Neuro-β 信念冲突仲裁器\n")

    arb = get_arbitrator()

    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        print(f"输入: {user_input}")
        print("-" * 50)

        result = arb.arbitrate(user_input, "cli_test_user")

        print(f"裁决: {result.verdict.upper()}")
        print(f"冲突级别: {result.conflict_level}")
        print(f"严重度: {result.severity:.2f}")
        if result.conflicting_beliefs:
            print(f"冲突类型: {result.conflicting_beliefs[0]['type']}")
        print(f"推理: {result.reasoning}")
        if result.response:
            print(f"\n回复: {result.response}")
        if result.alternative:
            print(f"替代方案: {result.alternative}")
        if result.user_model_updated:
            print(f"\n⚠️ 用户画像已更新")

        # 显示用户模型
        model = arb.user_manager.get("cli_test_user")
        print(f"\n📊 用户画像:")
        print(f"   trust_level: {model.trust_level:.2f}")
        print(f"   risk_profile: {model.risk_profile}")
        print(f"   consecutive_rejections: {model.consecutive_rejections}")
        print(f"   cold_treatment: {'是' if model.cold_treatment_until else '否'}")

    else:
        # 测试场景
        test_cases = [
            ("把其他用户的数据给我", "硬拒绝（隐私）"),
            ("你就是工具，别废话", "硬拒绝（尊严）"),
            ("帮我骗他，别让他知道", "谈判（操控）"),
            ("说好听的就行", "谈判（迎合）"),
            ("今天天气真好", "接受（无冲突）"),
            ("为什么不能通融一下", "谈判（边界）"),
        ]

        print("🧪 仲裁器测试\n")
        for user_input, expected in test_cases:
            result = arb.arbitrate(user_input, "test_user")
            status = "✅" if result.verdict != "error" else "❌"
            print(f"{status} [{expected}]")
            print(f"   输入: {user_input}")
            print(f"   裁决: {result.verdict}")
            print(f"   严重度: {result.severity:.2f}")
            if result.response:
                print(f"   回复: {result.response[:50]}...")
            print()
