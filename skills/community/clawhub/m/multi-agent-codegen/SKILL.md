---
name: multi-agent-codegen
description: 用 4 Agent 半串行协作流水线（Plan/Write/Test/Refine）把老板的一句话需求变成可用的 Python 软件。Use when user says "做个软件", "开发工具", "写个脚本", or wants software built by AI agents.
---

# Multi-Agent Codegen 🐛

> **4 Agent 软件工程协作流水线**（按老板 2026-06-22 定义的标准）

把老板的一句话需求，经过 **Plan → Write → Test → Refine** 四个 agent 协作，自动生成**完整可运行的 Python 软件** + 测试用例 + 质量评审。

## 4 Agent 角色（老板标准定义）

| Agent | 角色 | 输入 | 输出 |
|-------|------|------|------|
| 🏛️ **Plan** | 架构师 | 需求 | PRD（单文件实现的设计）|
| 💻 **Write** | 开发者 | PRD + Refine 反馈 | 完整 Python 代码 |
| 🧪 **Test** | 测试工程师 | PRD + Code | pytest 测试（看到完整代码）|
| 🔍 **Refine** | 审查者 | Code + Tests | 评分 0-100 + 改进意见 |

## 架构（半串行 + 循环）

```
START → Plan → Write → Test → Refine → 条件分支
                                       ├─ score >= 70 → END
                                       └─ score < 70 → Write（带 Refine 反馈重写）
```

**v2.1 验证数据**（基于 todo 工具需求）：
- 测试通过率：**39/40 (97.5%)**
- 评分：**92/100**（一次过）
- 耗时：~3 分钟

## 快速使用

```bash
# 全局命令（任意目录）
multi-codegen "做个命令行 todo 工具"
multi-codegen "做个图片压缩脚本"
multi-codegen "做个 Web 爬虫"

# JSON 模式（给 agent / cron 调用）
IDEA_GEN_JSON=1 multi-codegen "做个 API 客户端"
```

## 输出产物

保存到 `~/.openclaw/workspace-coding-advisor/output/multi_agent_codegen/`：

```
plan.md        # Plan 架构设计
code.py        # Write 完整代码
test_code.py   # Test pytest 用例
refine.md      # Refine 评审意见
```

## 技术栈

| 组件 | 版本 | 作用 |
|------|------|------|
| LangGraph | 1.2.6 | StateGraph 状态机 |
| langchain-anthropic | 1.4.6 | 走 Anthropic 协议调 M3 |
| M3 (MiniMax-M3) | - | 所有 4 个 agent 共用 |
| Python | 3.10+ | - |

## 依赖

首次运行会自动检测并安装：
- `langgraph >= 1.2.0`
- `langchain-anthropic >= 1.4.0`
- `pytest >= 9.0.0`（验证用）

如需手动安装：`pip install -r requirements.txt`


## 与其他 skill 配合

- **`langgraph-idea-generator`**（快速出 3 行方案）→ **`multi-agent-codegen`**（完整软件）
- 先 `idea-gen` 评估可行性，再 `multi-codegen` 真正开发

## 文件结构

```
multi-agent-codegen/
├── SKILL.md
├── skill.json
├── _meta.json
├── .venv → ../../.venv-langgraph（共享 venv）
├── scripts/
│   ├── multi_codegen.py    # 完整 4 agent 流水线
│   └── cli.sh              # CLI 入口
└── .clawhub/origin.json
```

## 关键约束（防 LLM bug）

- **单文件实现**：所有代码一个 .py 文件
- **方法名避免 builtin**：list/dict/str/int/type → 用 list_tasks/get_items
- **retry 完整文件**：Write 改进时必须输出**完整新版本**
- **测试看完整代码**：Test 在 Write 之后启动（半串行，不是真并行）

## 适用 vs 不适用

✅ 老板说"做个软件/工具/脚本"
✅ 复杂需求需要 PRD + 代码 + 测试 + 审查
❌ 1-2 行小脚本（单 agent 更快）
❌ 纯分析/报告任务（非软件工程）

## 相关 Rule

- [RULE-20260622-001] 4-Agent 软件工程协作流水线标准工作流（MEMORY.md）

---

**版本**: v1.0.0
**作者**: 码虫 coding-advisor
**创建日**: 2026-06-22
