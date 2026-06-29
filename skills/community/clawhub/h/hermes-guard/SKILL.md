---
name: hermes-guard
description: 主动式 AI Agent 质量守护系统 — 核验闸+逃生舱+自修正闭环。监控 Agent 输出质量，自动纠错，工具不够时自己造。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    homepage: https://github.com/lybang972314/hermes-guard
    emoji: 🛡️
---

# Hermes Guard 🛡️

**不是又一个 Agent 框架。是 Agent 的质量守护层。**

市场上不缺能调用工具的 Agent（CrewAI、LangChain、OpenAI Assistants）。但缺一个**知道自己什么时候该闭嘴、工具不够时会自己造、犯了错会自动写进规则不重犯**的 Agent。

## 核心三件套

| 组件 | 做什么 | 为什么值钱 |
|------|--------|-----------|
| **核验闸** (Completion Gate) | 输出前四维质量评分，低质量自动拦截 | LLM 会幻觉，这个闸门接在任何 Agent 输出后 |
| **逃生舱** (Escape Pod) | 工具不够时自动生成存根+注册，不硬上 | Agent 不会因为缺工具而崩溃或编造结果 |
| **自修正** (CORRECTION-as-Code) | 犯错自动写规则→固化进 AGENTS.md→下次不重犯 | 唯一有"学习能力"的 Agent 运维工具 |

## 架构

```
输入 → 三层分类器(80%<1ms) → 工具调用 / 直接回答
                                    ↓
                              四维质量评分(0-3)
                              ↓              ↓
                           分高→输出      分低→自动写CORRECTION规则
```

## 竞品对比

| | Hermes Guard | LangSmith | Arize | Guardrails AI |
|------|:---:|:---:|:---:|:---:|
| 输出质量评分 | ✅ 四维 | ⚠️ 延迟 | ⚠️ 延迟 | ❌ |
| 自动纠错闭环 | ✅ | ❌ | ❌ | ❌ |
| 工具健康巡检 | ✅ 每日 | ❌ | ❌ | ❌ |
| 逃生舱(自动补工具) | ✅ | ❌ | ❌ | ❌ |
| 零外部依赖 | ✅ 本地 | ❌ SaaS | ❌ SaaS | ❌ |

## 快速接入

```bash
pip install hermes-guard
hermes-guard audit    # 3秒出报告
```

```python
from hermes_guard import CompletionGate

gate = CompletionGate()
result = gate.check(agent_output)
if result.passed:
    return result.content
else:
    # 自动触发 CORRECTION 规则写入
    gate.correct(result)
```

## 谁在用

- Hermes 多 Agent 系统（产线运行）
- 每日 04:00 自动工具体检 + 04:35 跨系统互训

---

**[GitHub](https://github.com/lybang972314/hermes-guard)** · MIT License · **Enterprise → [Contact](https://github.com/lybang972314)**
