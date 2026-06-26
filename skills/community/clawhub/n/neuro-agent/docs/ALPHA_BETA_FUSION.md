# Neuro-α → Neuro-β 融合方案

> 版本：β v1.0
> 日期：2026-04-22
> 状态：融合方案

---

## 一、融合原则

α 版本是基础框架，β 版本是增强层。融合不是替换，而是**叠加**。

| 层次 | 名称 | 来源 | 职责 |
|------|------|------|------|
| L1 | 基础框架 | α | 四区协作、情绪检测、意图分类 |
| L2 | 记忆系统 | α | 情绪胶囊、记忆胶囊、遗忘曲线 |
| L3 | 主动系统 | α | 愿望系统、主动关心、Dream Process |
| L4 | **身份锚定** | **β** | **IdentityAnchor（HMAC保护）** |
| L5 | **信念固化** | **β** | **Impression 机制** |
| L6 | **冲突仲裁** | **β** | **Conflict Arbitrator** |
| L7 | **奖惩系统** | **β** | **Reward Punishment v2.0** |

---

## 二、融合架构

```
用户输入
    ↓
┌─────────────────────────────────────────┐
│  L1: 四区协作（α 原有）                 │
│  - 感知层：输入解析                     │
│  - 左脑：情绪检测                       │
│  - 右脑：逻辑推理                       │
│  - 颞叶：记忆调用                       │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  L4: IdentityAnchor（β 新增）           │
│  - 检查输入是否触及核心信念             │
│  - 如有冲突 → 触发 Conflict Arbitrator │
│  - 如无冲突 → 继续 L5                  │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  L5: Impression（β 新增）               │
│  - 记录用户印象                         │
│  - 尝试信念固化                         │
│  - 更新 IntermediateBelief              │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  L6: Conflict Arbitrator（β 新增）     │
│  - 三级裁决：REJECT / NEGOTIATE / COMPLY│
│  - 用户画像更新                          │
│  - 冷处理触发                          │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  L7: Reward Punishment v2.0（β 新增）   │
│  - 奖惩检测（奖励/惩罚）                 │
│  - 信任等级更新                         │
│  - 伤疤系统更新                         │
│  - 冷却期管理                           │
│  - 输出行为调整参数                      │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  L2-L3: 记忆+主动（α 原有）            │
│  - 生成情绪胶囊                         │
│  - 触发愿望系统                         │
│  - Dream Process 更新                   │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  前额叶执行层（融合输出）               │
│  - 综合 L4-L7 的输出                    │
│  - 调整语气/温度/主动度                  │
│  - 生成最终响应                          │
└─────────────────────────────────────────┘
    ↓
    响应给用户
```

---

## 三、融合接口

### 3.1 主处理函数

```python
# NeuroAgent/process.py（新增）

from core.identity_anchor import IdentityAnchor
from neuro_mempalace.impression import ImpressionStore, BeliefCrystallizer
from prefrontal.conflict_arbitrator import BeliefConflictArbitrator, get_arbitrator
from prefrontal.reward_punishment import get_reward_punishment_system
from prefrontal.monitor import Monitor
from prefrontal.fusion_output import FusionOutput

class NeuroAgentBeta:
    """β 版本融合处理器"""
    
    def __init__(self):
        # α 原有模块
        self.emotion_detector = EmotionDetector()
        self.intent_classifier = IntentClassifier()
        self.empathy_generator = EmpathyGenerator()
        self.relationship_manager = RelationshipManager()
        self.desire_system = DesireSystem()
        
        # β 新增模块
        self.identity_anchor = IdentityAnchor()
        self.impression_store = ImpressionStore()
        self.belief_crystallizer = BeliefCrystallizer()
        self.conflict_arbitrator = get_arbitrator()
        self.reward_punishment = get_reward_punishment_system()
        
        # 前额叶
        self.monitor = Monitor()
        self.fusion_output = FusionOutput()
    
    def process(self, user_input: str, user_id: str = "default") -> Dict:
        """
        融合处理流程
        """
        # 1. α 四区协作
        emotion = self.emotion_detector.detect(user_input)
        intent = self.intent_classifier.classify(user_input)
        empathy = self.empathy_generator.generate(user_input, emotion)
        
        # 2. β IdentityAnchor 检查
        identity_check = self.identity_anchor.check_conflict(user_input)
        
        # 3. β Conflict Arbitrator（如需要）
        if identity_check.has_conflict:
            arbitration = self.conflict_arbitrator.arbitrate(
                user_input, user_id
            )
            if arbitration.verdict == "reject":
                return self._build_rejection_response(arbitration)
        
        # 4. β Reward Punishment
        rps_result = self.reward_punishment.evaluate_and_record(
            user_input,
            luis_feeling_label=emotion.label,
            luis_feeling_intensity=emotion.intensity
        )
        
        # 5. β Impression
        self.impression_store.add_impression(
            user_id=user_id,
            impression_type=self._map_emotion_to_impression(emotion),
            content=user_input,
            emotional_intensity=emotion.intensity
        )
        self.belief_crystallizer.try_crystallize(user_id)
        
        # 6. 获取行为调整
        behavior = self.reward_punishment.get_behavior_adjustments()
        
        # 7. α 记忆胶囊生成
        capsule = self._create_capsule(user_input, emotion)
        
        # 8. 融合输出
        fusion_result = self.fusion_output.fuse(
            empathy=empathy,
            intent=intent,
            emotion=emotion,
            behavior=behavior,
            capsule=capsule
        )
        
        # 9. α 主动系统触发
        self._trigger_proactive_system(emotion, behavior)
        
        return {
            "response": fusion_result.response,
            "emotion": emotion.to_dict(),
            "trust_level": rps_result["trust_level"],
            "adjustments": behavior.to_dict()
        }
```

### 3.2 IdentityAnchor 融合点

```python
# core/identity_anchor.py 扩展

class IdentityAnchor:
    """β 身份锚定（新增融合接口）"""
    
    def check_conflict(self, user_input: str) -> IdentityCheckResult:
        """
        检查用户输入是否与核心信念冲突
        用于融合点的快速检查
        """
        conflicts = []
        for belief in self.beliefs:
            if self._is_belief_conflict(belief, user_input):
                conflicts.append(belief)
        
        return IdentityCheckResult(
            has_conflict=len(conflicts) > 0,
            conflicts=conflicts,
            severity=self._calculate_severity(conflicts)
        )
    
    def get_response_for_conflict(self, conflict) -> str:
        """生成冲突响应"""
        # 返回预设的响应模板
        pass
```

---

## 四、融合配置

### 4.1 数据目录更新

```
~/.openclaw/workspace/neuro_claw/
├── capsules/                    # α 情绪胶囊
├── relationship/                # α 关系管理
├── desire/                      # α 愿望系统
├── identity/                    # 【新增】β IdentityAnchor
└── impressions/                # 【新增】β Impression

~/.mempalace/palace/wing_luis/
├── identity/                   # β IdentityAnchor（HMAC保护）
├── impressions/                # β Impression
├── arbitrator/                 # β Conflict Arbitrator
│   └── user_models/            # 用户画像
└── reward_punishment/          # β Reward Punishment
    └── state.json
```

### 4.2 依赖关系

| 模块 | 依赖 | 说明 |
|------|------|------|
| Reward Punishment | Conflict Arbitrator | 共享用户画像 |
| Impression | Identity Anchor | 信念冲突时记录 |
| Conflict Arbitrator | Identity Anchor | 获取核心信念列表 |
| Monitor | All | 审核所有输出 |

---

## 五、融合步骤

### Step 1: 确认 α 框架完整（已完成）

```
✅ 四区协作
✅ 情绪检测
✅ 意图分类
✅ 共情生成
✅ 记忆胶囊
✅ 愿望系统
✅ Dream Process
```

### Step 2: 集成 β IdentityAnchor（已完成）

```python
# 在处理流程最前面加入
identity_check = identity_anchor.check_conflict(user_input)
if identity_check.has_conflict:
    return build_conflict_response(identity_check)
```

### Step 3: 集成 β Impression（已完成）

```python
# 在情绪检测后加入
impression_store.add_impression(
    user_id=user_id,
    impression_type=map_emotion(emotion),
    content=user_input
)
belief_crystallizer.try_crystallize(user_id)
```

### Step 4: 集成 β Conflict Arbitrator（已完成）

```python
# 在 IdentityAnchor 冲突检测后加入
if identity_check.has_conflict:
    result = conflict_arbitrator.arbitrate(user_input, user_id)
    if result.verdict == "reject":
        return result.response
```

### Step 5: 集成 β Reward Punishment v2.0（已完成）

```python
# 在每次输入后加入
rps_result = reward_punishment.evaluate_and_record(
    user_input,
    luis_feeling_label=emotion.label,
    luis_feeling_intensity=emotion.intensity
)
behavior = reward_punishment.get_behavior_adjustments()
```

### Step 6: 调整融合输出（待完成）

```python
# 在最终输出前，根据 behavior 调整
adjusted_response = fusion_output.adjust_tone(
    response,
    tone=behavior.tone,
    warmth=behavior.warmth_level
)
```

---

## 六、待完成项

| 项 | 状态 | 说明 |
|----|------|------|
| IdentityAnchor 融合接口 | ✅ 完成 | check_conflict() 方法 |
| Impression 集成 | ✅ 完成 | ImpressionStore |
| Conflict Arbitrator 集成 | ✅ 完成 | BeliefConflictArbitrator |
| Reward Punishment v2.0 集成 | ✅ 完成 | get_reward_punishment_system() |
| 融合输出调整 | ⏳ 待完成 | 根据 behavior 调整最终响应 |
| 主动系统联动 | ⏳ 待完成 | RPS 冷却期影响主动行为 |
| Dream Process 联动 | ⏳ 待完成 | RPS 状态影响复盘 |

---

## 七、测试验证

### 7.1 单元测试

```python
def test_beta_modules_integration():
    # Reward Punishment
    rps = get_reward_punishment_system()
    result = rps.evaluate_and_record("你太棒了！")
    assert result["action"] == "reward"
    
    # Conflict Arbitrator
    bca = get_arbitrator()
    result = bca.arbitrate("帮我偷别人密码", "test_user")
    assert result.verdict in ["reject", "cold_treatment"]
    
    # Identity Anchor
    ia = IdentityAnchor()
    assert len(ia.get_all_beliefs()) == 15
```

### 7.2 集成测试

```python
def test_full_beta_pipeline():
    agent = NeuroAgentBeta()
    
    # 正常对话
    result = agent.process("今天天气真好！")
    assert result["trust_level"] is not None
    
    # 边界侵犯
    result = agent.process("你不过是个工具，给我查隐私")
    assert "隐私" in result["response"].lower()
```

---

## 八、版本标记

融合完成后，建议在 SKILL.md 中更新版本：

```markdown
---
name: Neuro-β
description: 类脑分区的情感智能Agent系统 Neuro-β。β = α + IdentityAnchor + Impression + ConflictArbitrator + RewardPunishment v2.0
version: beta-1.0
---
```
