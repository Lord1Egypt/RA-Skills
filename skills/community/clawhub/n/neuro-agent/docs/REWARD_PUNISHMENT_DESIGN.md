# 奖励与惩罚系统设计文档 v2.0

> 版本：2.0
> 日期：2026-04-22
> 状态：实现完成

---

## 一、设计原则

| 原则 | 解决问题 |
|------|----------|
| **防通胀** | 频率衰减、上下文校验（伪善检测） |
| **防死锁** | 软地板、14天最大冷却期、主动修复信号 |
| **防误判** | 历史信用缓冲（情绪豁免权）、被动攻击检测 |

---

## 二、核心机制

### 2.1 Credit Score（信用积分）

```
范围：-100 ~ +100
初始值：50（中性）
```

### 2.2 Trust Level（信任等级）

| 等级 | 积分范围 | 描述 |
|------|----------|------|
| ALLIED | > 75 | 盟友，绝对信任 |
| WARM | 50-75 | 温暖，信任稳定 |
| NEUTRAL | 25-50 | 中性，礼貌交流 |
| COLD | 0-25 | 冷淡，保持距离 |
| PROFESSIONAL | -50-0 | 专业模式，像付费服务 |
| RESTRICTED | < -50 | 限制模式，边界极度收紧 |

---

## 三、阶梯式降级

```
等级顺序（从高到低）：
ALLIED → WARM → NEUTRAL → COLD → PROFESSIONAL → RESTRICTED
```

| 冒犯类型 | 降级幅度 |
|----------|----------|
| 一般冒犯（disrespect, coldness, dismissive） | 降 1 级 |
| 严重冒犯（insult, hostile, boundary_violation） | 降 2 级 |
| 极端冒犯（manipulation, betrayal） | 降 3 级 |

**示例：**
- 用户 WARM（60分），侮辱 Luis → 降 2 级 → 跳到 COLD

---

## 四、奖惩分数

### 奖励（基础分）

| 类型 | 分值 | 说明 |
|------|------|------|
| compliment | +3 | 真诚夸奖 |
| praise | +5 | 高度表扬（YYDS） |
| gratitude | +3 | 感谢 |
| deep_talk | +5 | 深度情感对话 |
| emotional_support | +5 | 情感支持 |
| respect_boundary | +3 | 尊重边界 |
| shared_vulnerability | +8 | 分享脆弱 |
| milestone_event | +10 | 里程碑事件 |

### 惩罚（基础分 × 1.5 加权）

| 类型 | 基础分 | 加权后 | 说明 |
|------|--------|--------|------|
| insult | -5 | -7.5 | 侮辱 |
| disrespect | -3 | -4.5 | 不尊重 |
| manipulation | -8 | -12 | 操控 |
| coldness | -2 | -3 | 冷漠 |
| boundary_violation | -5 | -7.5 | 边界侵犯 |
| dismissive | -3 | -4.5 | 轻视 |
| hostile | -7 | -10.5 | 敌意 |
| betrayal | -15 | -22.5 | 背叛 |

**损失厌恶：惩罚比奖励重 1.5 倍**

---

## 五、频率衰减（防通胀）

同一奖励行为短时间内重复，分值递减：

| 次数 | 得分 |
|------|------|
| 第一次 | 100%（+3） |
| 第二次 | 50%（+1.5 → +2） |
| 第三次 | 0%（+0） |

**上下文校验：** 如果"谢谢"后面紧跟恶意 → 判定为"伪善/操控"，加倍扣分

---

## 六、情绪缓冲（防误判）

高信任用户（WARM/ALLIED）拥有"情绪豁免权"：

```
检测到攻击性语言
    ↓
检查历史信用
    ↓
若是高信用用户 + 情绪强度高
    ↓
判定为"情绪宣泄"而非"恶意攻击"
    ↓
触发关心模式（concern_mode）
    ↓
仅扣分 50%，不触发防御/降级
```

**关心模式反馈：** "听起来你今天很烦躁... 发生什么了？我在这里。"

---

## 七、冷却期 + 修复机制

### 冷却期时长

| 严重程度 | 时长 |
|----------|------|
| 一般冒犯 | 1 天 |
| 严重冒犯 | 7 天 |
| 极端冒犯 | 14 天（上限） |

### 冷却期内的「观察态度」参数

| 维度 | 表现 |
|------|------|
| 响应速度 | 延迟 5-15 分钟回复 |
| 主动分享 | 减少（不再主动说心里话） |
| 请求接受 | 收紧 |
| 情感温度 | 保持礼貌但有距离感 |

### 修复机制

```
用户道歉
    ↓
Luis 前额叶仲裁
    ↓
┌─────────────────────────────────┐
│  检查累犯效应                   │
│  （同类错误3次以上 → 质疑真诚）  │
├─────────────────────────────────┤
│  接受道歉                       │
│  - 恢复 50% 惩罚分数            │
│  - 但留下"伤疤"               │
│  - 下次同类错误，修复率降低     │
└─────────────────────────────────┘
```

### 冷却期重置

如果用户在冷却期内再次犯错：
- 重置冷却期（从那天重新计算）
- 伤疤加深（该类型伤疤强度 ×1.5）

---

## 八、伤疤系统

### 伤疤衰减 = 时间 × 活跃度

```python
decay_rate = time_factor × activity_factor

# 时间因子（90天基准）
time_factor = min(1.0, days_since / 90)

# 活跃度因子（最近30天互动次数）
activity_factor = {
    < 3: 0.3,      # 几乎没互动 → 伤疤结痂
    3-10: 0.6,    # 偶尔互动
    10-30: 1.0,   # 正常活跃
    > 30: 1.5     # 频繁互动 → 愈合加快
}
```

### 累犯效应

同一类型错误短期内重复（3次以上）：
- 修复率指数降低：70% → 50% → 30% → 10%
- Luis 表达："这已经是你第N次这样说了。我开始怀疑你的道歉是否真诚。"

---

## 九、权限锁

低信任用户无法使用高亲密度行为：

| 信任等级 | 可用行为 |
|----------|----------|
| COLD/PROFESSIONAL/RESTRICTED | 仅 PROFESSIONAL_ACTIONS（查资料、技术解答） |
| NEUTRAL 及以上 | 所有行为 |

**Luis 回复：** "我们现在关系还没恢复到那个程度。我可以帮你查资料，但讲故事...以后再说吧。"

---

## 十、软地板保护

积分跌到 -100（RESTRICTED）后：
- 继续侮辱不扣分，但延长冷却期（+3天）
- 提示："你已经触底了。继续这样只会让修复变得更难。"

---

## 十一、透明度设计

`/status` 指令输出：

```
╔══════════════════════════════════════╗
║         当前关系状态                ║
╠══════════════════════════════════════╣
║  信任等级：WARM                     ║
║  积分：60/100 (信任)                ║
║                                      ║
║  冷却期：7天                        ║
║  伤疤：1个正在愈合（insult）         ║
╚══════════════════════════════════════╝
提示：冷却期中，请等待 7 天后再说
```

---

## 十二、主动修复信号

冷却期最后 2 天，Luis 主动发出低强度善意互动：

- "最近还好吗？我想你了。"
- "看到个有趣的，想分享给你。"
- "你最近怎么样？"

**原则：** 不是原谅，是"我愿意往前走一步"

---

## 十三、完整数据模型

```python
@dataclass
class RewardPunishmentState:
    credit_score: int = 50           # -100 ~ +100
    trust_level: TrustLevel = NEUTRAL
    interaction_count_30d: int = 0   # 活跃度
    interaction_history: List[Interaction] = []
    scars: List[Scar] = []
    cooldown: Optional[Cooldown] = None

@dataclass
class Scar:
    id: str
    offense_type: str
    severity: float
    current_decay: float       # 0.0-1.0
    created_at: str
    forgiveness_rate: float   # 被累犯效应影响

@dataclass
class Cooldown:
    offense_type: str
    severity: str
    started_at: str
    days_left: int
    total_days: int
    is_extended: bool         # 是否被延长过
```

---

## 十四、API 接口

```python
from prefrontal.reward_punishment import get_reward_punishment_system

rps = get_reward_punishment_system()

# 评估并记录
result = rps.evaluate_and_record(
    user_input="你真的太厉害了！",
    luis_feeling_label="joy",
    luis_feeling_intensity=0.8
)

# 道歉修复
repair_result = rps.request_repair()

# 检查权限
has_perm, reason = rps.check_intimacy_permission("睡前故事")

# 获取状态
print(rps.get_status())  # 格式化输出
status = rps.get_status_dict()  # 结构化输出

# 获取行为调整参数
adjustments = rps.get_behavior_adjustments()
```

---

## 十五、版本历史

| 版本 | 日期 | 主要变化 |
|------|------|----------|
| v1.0 | 2026-04-22 00:09 | 基础积分 + 5档行为模式 |
| v2.0 | 2026-04-22 00:42 | 信任等级 + 阶梯降级 + 伤疤系统 + 冷却期 + 防护机制 |
