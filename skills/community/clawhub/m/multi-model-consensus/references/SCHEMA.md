# 多模型决策委员会 — 状态文件 Schema（已归档）

> ⚠️ **V1.6.0 说明**：本文档描述的状态文件 Schema 已归档。V1.6.0 起不再使用持久化状态文件，改用「轻量级状态跟踪」（会话上下文变量）。本文件保留供历史参考。

## 状态文件字段

| 字段 | 类型 | 必填 | 说明 |
|:---|:---|:---:|:---|
| `state` | string | ✅ | 当前状态：IDLE / ROUND_0 / ROUND_1 / ROUND_2 / ROUND_3 / COMPLETE |
| `config` | object | ✅ | 评委配置 |
| `config.models` | array | ✅ | 评委模型列表，如 ["模型A", "模型B", "模型C"] |
| `config.rounds` | integer | ✅ | 决策轮数，2-6，默认3 |
| `config.threshold` | number | ✅ | 通过阈值，0-1，如 0.9 |
| `round0` | object | — | 准备阶段汇总内容 |
| `round1` | object | — | 第1轮结果（含 judges[].used_subagent） |
| `round2` | object | — | 第2轮结果 |
| `round3` | object | — | 第3轮结果（仅在有分歧时） |
| `report` | object | — | 最终6段式共识报告 |

---

## 版本演进规则

1. **不得单方面升版**：任何 Schema 变更必须经过委员会评审通过
2. **向后兼容**：新版本应尽可能兼容旧版本数据格式
3. **升版记录**：每次升版须在 CHANGELOG.md 中详细记录变更内容
