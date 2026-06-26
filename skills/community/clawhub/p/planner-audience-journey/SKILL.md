---
name: planner-audience-journey
description: "观众旅程设计：设计观众的情感弧线（不是故事弧线），定义观众在每个关键时间点应该感受到什么。触发词：观众旅程、audience journey、观众情感弧线、观众体验设计。"
metadata:
  tier1_summary: "Downstream Development完成后、IP Registration前强制执行：设计观众情感弧线，输出Audience Journey Map，作为策划-编辑桥梁"
---

# Planner Audience Journey（观众旅程设计）

**触发条件**：Downstream Development（节点 6）完成后，IP Registration（节点 7）之前。

**核心使命**：设计**观众的情感弧线**——不是故事的弧线，是观众经历故事时的弧线。

---

## 为什么需要 Audience Journey？

**故事弧线 vs 观众弧线**：
- 故事弧线：角色经历了什么 → 创作者视角
- 观众弧线：观众经历了什么 → 接收者视角

**皮克斯标准**：皮克斯做的是 audience-first storytelling。他们设计的不只是故事弧线，更是观众在每个时间点的情感状态——第 1 分钟应该好奇，第 3 分钟应该紧张，第 7 分钟应该心碎，第 10 分钟应该满足。

**如果没有 Audience Journey Map**：
- 编辑的 `story_architecture.emotional_arc` 只能猜策划意图
- 张力曲线（`tension_curve`）只有强度没有方向——高张力可以是兴奋也可以是焦虑
- 场景画师（`editor-scene-painter`）无法判断"这个场景应该给观众什么感受"

---

## 执行步骤

### Step 1: 读取项目全量信息

1. 读取 Theme Lock（`theme-lock.md`）
2. 读取 Pitch（`01-pitch/`）
3. 读取角色小传（`02-角色/`）
4. 读取世界观（`03-世界/`）
5. 读取 World-Character Sync（`03-世界/world-character-sync.md`）
6. 读取 Pilot 大纲（`05-pilot/`）
7. 读取季线设计（`04-季线/`）

### Step 2: 定义系列级 Audience Promise

**"看完这个系列，观众会带着什么情感离开？"**

这不是 Theme Statement（故事相信什么），而是 Theme Statement 对观众的情感影响：

| Theme Statement | Audience Promise |
|----------------|-----------------|
| "被需要是比被制造更重要的存在理由" | "你会在一个看似无用的存在身上找到最深的感动" |
| "悲伤和快乐一样重要" | "你会先心碎，然后理解心碎是必要的" |
| "谁都不配定义你的天花板" | "你会为小人物的每一步突破而振奋" |

验证：Audience Promise 是否与 Emotional Promise（pitch 中定义的）一致？如果不一致 → 回到 Pitch 修正 Emotional Promise。

### Step 3: 设计 Pilot 的观众情感弧线

对 Pilot 的每一个关键时间点，定义观众应该感受到什么：

```json
{
  "pilot_audience_journey": [
    {
      "time_marker": "0:00-0:30",
      "target_emotion": "好奇+轻微不安",
      "how": "开场画面建立陌生世界的视觉冲击，但有一个违和的细节暗示危险",
      "anti_emotion": "无聊、困惑",
      "narrative_tool": "视觉钩子 + 未解之谜"
    },
    {
      "time_marker": "0:30-3:00",
      "target_emotion": "代入+关心",
      "how": "通过主角的 Wound 建立共情——观众理解他为什么是现在这样",
      "anti_emotion": "无感、看不懂",
      "narrative_tool": "Wound 展示 + 日常困境"
    },
    {
      "time_marker": "3:00-6:00",
      "target_emotion": "紧张+期待",
      "how": "核心戏剧问题建立，主角被迫面对与 Wound 相关的挑战",
      "anti_emotion": "松懈、走神",
      "narrative_tool": "冲突升级 + 不可逆选择"
    },
    {
      "time_marker": "6:00-8:00",
      "target_emotion": "心碎或震撼",
      "how": "主角的 Want 与 Need 碰撞，必须牺牲一个",
      "anti_emotion": "无动于衷",
      "narrative_tool": "Want/Need 冲突 + 失去"
    },
    {
      "time_marker": "8:00-10:00",
      "target_emotion": "释然+渴望更多",
      "how": "一个暂时的和解，但留下更大的悬念",
      "anti_emotion": "满足后无牵挂、失望",
      "narrative_tool": "小胜利 + 大悬念"
    }
  ]
}
```

**关键字段说明**：
- `target_emotion`：观众**应该**感受到什么（设计目标）
- `how`：用什么叙事手段达到
- `anti_emotion`：观众**不应该**感受到什么（反面指标，用于质检）
- `narrative_tool`：使用的叙事工具（对应编辑侧的具体 skill）

### Step 4: 设计第一季的观众情感弧线

对第一季的每个关键节点，定义观众的宏观情感状态：

```json
{
  "season_audience_journey": [
    {
      "episode_range": "EP01-03",
      "phase_name": "建立契约",
      "target_emotion": "好奇→代入→信任",
      "emotional_contract": "观众信任这个故事会兑现 Emotional Promise",
      "risk": "如果前3集没有建立信任，观众不会给第4集机会"
    },
    {
      "episode_range": "EP04-08",
      "phase_name": "深化困境",
      "target_emotion": "关心→焦虑→心疼",
      "emotional_contract": "观众对角色的关心从表面同情升级为深层理解",
      "risk": "如果困境不升级，观众会疲劳"
    },
    {
      "episode_range": "EP09-12",
      "phase_name": "中点裂变",
      "target_emotion": "震惊→怀疑→重新审视",
      "emotional_contract": "观众意识到之前的理解可能被颠覆",
      "risk": "如果中点没有转折，故事后半段失去动力"
    },
    {
      "episode_range": "EP13-20",
      "phase_name": "终章加速",
      "target_emotion": "屏息→心碎→升华",
      "emotional_contract": "观众经历最强烈的情感冲击后获得 Theme Statement 的兑现",
      "risk": "如果终章减速或情感兑现不足，整个系列的情感投资打了水漂"
    }
  ]
}
```

### Step 5: 验证 Audience Journey 的内在一致性

1. **情感连贯性**：相邻时间点的 target_emotion 是否有过渡？不允许情感跳变（从好奇直接跳到心碎）
2. **承诺兑现性**：最终的 target_emotion 是否兑现了 Emotional Promise？
3. **反情感规避性**：每个 anti_emotion 是否有对应的防范措施？
4. **主题回响性**：Audience Journey 是否在情感层面探讨了 Theme Statement？

### Step 6: 输出 Audience Journey Map

将 Step 2-4 的结果整合为 `audience-journey-map.md`：

```markdown
# Audience Journey Map

## 项目：{项目名}

## 系列 Audience Promise
{Step 2 的结果}

## Pilot 观众情感弧线
{Step 3 的完整数据}

## 第一季观众情感弧线
{Step 4 的完整数据}

## 一致性验证
{Step 5 的验证结果}

## 关键设计决策
- {为什么在某处安排特定情感，而不是其他选择}
- {哪些情感节点是不可修改的（与 Theme Statement 绑定），哪些可以微调}
```

写入 `CLAW_WORKSPACE/99-汇总/audience-journey-map.md`

---

## 与上下游的关系

| 上下游 | 关系 |
|-------|------|
| Downstream Development（上游） | Journey 的输入：世界观、角色、pilot、季线 |
| IP Registration（下游） | Audience Journey Map 是 Series Bible Skeleton 的核心组件 |
| Theme Lock | Audience Promise 从 Theme Statement 派生 |
| editor-story-architect（编辑侧） | `story_architecture.emotional_arc` 以 Journey Map 为输入 |
| editor-tension-mapper（编辑侧） | `tension_curve` 的方向由 Journey Map 的 target_emotion 决定 |
| editor-scene-painter（编辑侧） | 视觉记忆点的设计与 Journey Map 的 target_emotion 对齐 |
| editor-adversarial-reviewer（编辑侧） | Hook Audit 和 Emotional Manipulation Detection 以 Journey Map 为评判标准 |

---

## 硬规则

1. **Audience Journey Map 是 IP Registration 的必要输入**——没有 Journey Map 的项目不完整
2. **target_emotion 必须有对应的 anti_emotion**——知道不该给观众什么感受，和知道该给什么一样重要
3. **Pilot 的前 3 分钟必须有明确的 target_emotion**——这是 Hook Audit 的设计依据
4. **第一季必须有至少一个情感转折点**——观众弧线不能是单向的
5. **Audience Promise 必须与 Emotional Promise 一致**——如果不一致，说明承诺和体验脱节
6. **不允许用"震撼"代替具体的 target_emotion**——"震撼"是结果不是设计，必须说清楚震撼的原因和方向
