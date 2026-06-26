# 伏笔三元组追踪器

## 目标

将伏笔从"设计时想到"升级为"全程结构化追踪"，确保每个伏笔都能被可靠回收或主动断裂处理。

## 伏笔三元组结构

每个伏笔由三个字段组成：

| 字段 | 说明 | 示例 |
|------|------|------|
| **Cause（埋）** | 伏笔植入的事件、细节或对话 | "第1章出现神秘玉佩" |
| **Promise（约）** | 这个伏笔暗示的后续发展方向 | "暗示主角身世之谜" |
| **Payoff（收）** | 伏笔最终兑现的方式 | "第12章玉佩揭示主角是皇族遗孤" |

三者缺一不可。Cause 是事实，Promise 是预期，Payoff 是兑现结果。

## 伏笔状态

| 状态 | 定义 | 处理方式 |
|------|------|---------|
| `pending` | 伏笔已植入，尚未开始回收 | 正常追踪，等待回收窗口 |
| `fulfilled` | 伏笔已成功兑现 | 标记完成，无需进一步操作 |
| `broken` | 伏笔承诺无法兑现 | 记录断裂原因，考虑处理方式 |
| `expired` | 超出合理回收窗口仍未回收 | 标记过期，评估是否补收或放弃 |

## 触发检查点

### 1. 大纲完成时

**动作**：从 `02_大纲.md` 提取初始伏笔清单，建立三元组。

提取规则：
- 扫描"伏笔"、"暗示"、"铺垫"、"线索"等关键词段落
- 每个伏笔生成 Cause + Promise，Payoff 留空
- 自动分配 `plantedAt` = "大纲"
- 根据情节位置估算 `expectedPayoffRange`

### 2. 每批次 drafting 关闭时

**动作**：扫描本批次正文，检查是否有伏笔进入回收阶段。

检查规则：
- 本批次提及了某个 pending 伏笔的 Cause 细节
- 本批次出现了 Promise 暗示的兑现迹象
- 如果发现 Payoff 触发，更新对应伏笔的 `payoff` 和 `actualPayoffChapter`

### 3. proofreading 时

**动作**：验证 pending 伏笔在当前批次是否有迹可循。

检查规则：
- pending 伏笔的 Promise 方向是否在本批次有情节支撑
- 是否有即将断裂的伏笔（Promise 方向与正文矛盾）
- 生成伏笔健康度报告

### 4. final-review 时

**动作**：整体伏笔健康度评估。

检查规则：
- pending 伏笔数量是否合理（过多说明回收节奏失控）
- broken 伏笔是否都有明确断裂原因
- fulfilled 伏笔的 Payoff 质量评估（是否草率兑现）
- 生成最终伏笔账本

## 项目内账本

伏笔账本文件：`05G_伏笔三元组账本.md`

每次重要更新后覆盖写入。格式见下方账本模板。

## 状态字段

在 `.novel-state.json` 的 `narrativeIntelligence.cfpg` 中维护：

```json
{
  "cfpg": {
    "foreshadowTriples": [
      {
        "id": "fp-001",
        "cause": "第1章出现神秘玉佩",
        "promise": "暗示主角身世之谜",
        "payoff": null,
        "status": "pending",
        "plantedAt": "第1章",
        "expectedPayoffRange": "第10-15章",
        "actualPayoffChapter": null,
        "brokenReason": null
      }
    ],
    "tripleCounts": {
      "total": 12,
      "pending": 8,
      "fulfilled": 3,
      "broken": 1,
      "expired": 0
    },
    "lastUpdatedAt": "2026-03-29T10:00:00Z",
    "lastUpdatedBatch": "第4章-第6章"
  }
}
```

## 断裂处理原则

当伏笔状态变为 `broken` 时，需要判断：

1. **是否必须修复**：broken 是否影响核心情节逻辑
2. **是否可以用新伏笔替代**：补充新的伏笔来修正预期
3. **是否可以主动断裂**：在 final-review 前主动宣布断裂，避免读者感到欺骗

## 过期处理原则

当伏笔状态变为 `expired` 时：

- 超出 `expectedPayoffRange` 后两个批次仍未回收，标记为 expired
- 评估是否补收（修改情节让伏笔合理兑现）或放弃（调整大纲删除该伏笔承诺）

## 质量标准

- 每个伏笔的 Promise 必须是读者可以感知到的方向，不能是模糊的"将来有用"
- fulfilled 的 Payoff 不能比 Promise 弱（草率兑现比不兑现更伤害读者信任）
- pending 伏笔数量不应超过已完成章节数的 30%（过多说明回收节奏失控）
