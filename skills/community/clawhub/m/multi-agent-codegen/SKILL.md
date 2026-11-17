---
name: multi-agent-codegen
description: 用 4 Agent 半串行协作流水线（Plan/Write/Test/Refine）把老板的一句话需求变成可用的 Python 软件。全程飞书通知，不再是黑盒。Use when user says "做个软件", "开发工具", "写个脚本", or wants software built by AI agents. Trigger: 用户说"做个软件"、"开发工具"、"写个脚本"时使用。
---

# Multi-Agent Codegen 🐛

> **4 Agent 软件工程协作流水线 v3.3.0**（2026-06-22 初版定义，2026-07-20 v3.0 飞书通知，2026-09-23 v3.1 L4 Verify 接入，2026-09-23 晚 v3.2 SyntaxError hard retry，2026-09-23 深夜 v3.3 Test Verify 接入）

把老板的一句话需求，经过 **Plan → Write → L4 Verify → Test → Refine** 四个 agent 协作，自动生成**完整可运行的 Python 软件** + 测试用例 + 质量评审。

**v3.0 重大升级：全程飞书通知** — 每个 Agent 完成后立即推送飞书消息，老板在微信上实时看到进度，不再是黑盒：

| Agent | 完成通知内容 |
|-------|-------------|
| 🏛️ Plan | 产出字数 + 设计要点摘要 |
| 💻 Write | 文件数 + 代码行数 + 方法数 |
| 🛡️ **L4 Verify (v3.1)** | 5 步规则检查结果 + 不通过时反馈问题给 Write retry |
| 🧪 Test | 测试用例数 + 代码行数 |
| 🔍 Refine | 评分 + critical/major/minor 问题统计 |
| 🚀 结束 | 最终评分 + 总耗时 + 产物目录 |

**v3.1 重大升级：L4 Verify Agent 接入主流水线** — Write Agent 完成后立即跑 5 步确定性规则检查（长度/完整性/占位符/语法/密度），不通过自动 retry Write，节省 token（不再在不合格的代码上跑 Test/Refine）。遵循 [RULE-20260701-001](https://my.feishu.cn/docx/Nw3RdgXR0oKVpSxyQRLcUG9nnm2) 终极根治 LLM retry 缩水。

**v3.2 重大升级：SyntaxError hard fail retry** — 区分 hard fail（语法错误，绝对不能放过）与 soft fail（长度/占位符，达到上限放过）。SyntaxError 走独立计数器 `syntax_retry_count`，无视 `max_verify_retries` 上限，强制修复直到通过或达到 `max_hard_retries=5`。同时提 `max_verify_retries` 默认值 2 → 3，给 LLM 软错误更多机会。

**v3.3 重大升级：Test Verify Agent 接入** — 给 `test_code.py` 加 L4 Verify 保护！Test Agent 完成后立即跑 5 步规则验证（test_code.py 默认 5000 字硬下限），不通过 → 注入失败原因 → 立即 retry Test，同样区分 hard/soft 错误。实战发现 v3.2 只保护 code.py，test_code.py 也有 SyntaxError 漏出（pytest 一跑就崩）。v3.3 补齐 test_code.py 的防护。

---

## 1. 快速使用

```bash
# 基本用法
multi-codegen "做个命令行 todo 工具"

# 指定输出目录
multi-codegen "做个 Web 爬虫" --output /path/to/output

# 环境变量（API Key）
EM_API_KEY="your-key" multi-codegen "做个 API 客户端"
```

### Python 调用

```python
import subprocess
result = subprocess.run(
    ["python3", "scripts/multi_codegen.py", "做个天气查询工具"],
    capture_output=True, text=True,
    env={**os.environ, "EM_API_KEY": "your-key"}
)
print(result.stdout)
```

---

## 2. 4 Agent + 1 Verify 角色

| Agent | 角色 | 输入 | 输出 |
|-------|------|------|------|
| 🏛️ **Plan** | 架构师 | 需求 | 架构设计（单文件实现思路） |
| 💻 **Write** | 开发者 | 架构设计 + Verify/Refine 反馈 | 完整 Python 代码 |
| 🛡️ **L4 Verify (v3.1)** | 确定性规则验证 | Write 产出代码 | 通过/不通过（5 步规则：长度/完整性/占位符/语法/密度） |
| 🧪 **Test** | 测试工程师 | 架构设计 + 代码 | pytest 测试用例 |
| 🔍 **Refine** | 审查者 | 代码 + 测试 | 评分 0-100 + 改进意见 |

**v3.1 关键改进**：Write 后立即跑 L4 Verify，不通过 → 注入失败原因 → Write retry（最多 2 次）→ 不阻塞流水线（达到上限仍继续 Test）。

---

## 3. 流水线架构（v3.1）

```
START
  │
  ▼
┌─────────┐   完成通知    ┌─────────┐   完成通知    ┌─────────┐   完成通知    ┌─────────┐
│ 🏛️ Plan │ ──────────▶ │ 💻 Write │ ──────────▶ │ 🛡️ L4 Verify │ ──────▶ │ 🧪 Test  │ ──────────▶ │ 🔍 Refine │
└─────────┘   飞书推送    └─────────┘   飞书推送    └─────────┘   飞书推送    └─────────┘   飞书推送    └─────────┘
                                                                              │
                                          ┌──────────────────────────────────┘
                                          │  verify 不通过  &  retries ≤ 2
                                          ▼
                                    ┌───────────┐
                                    │ Write retry│ ◀─────────────────┐
                                    └───────────┘                   │
                                          │                          │
                                          │ verify 通过                │
                                          ▼                          │
                              ┌───────────┐                       │
                              │   Test   │                       │
                              └───────────┘                       │
                                          ┌─────────────────────────┘
                                          │  score < 70  &  retries ≤ 2
                                          ▼
                                    ┌───────────┐
                                    │  重写循环   │ ◀──────────────────┐
                                    └───────────┘                    │
                                          │                            │
                                          │ score ≥ 70                  │
                                          ▼                            │
                                    ┌───────────┐                    │
                                    │   结束    │ ───────────────────┘
                                    └───────────┘

飞书通知节点（v3.1 - 每个 Agent 完成立即推送）：
  🚀 流水线启动 → 🏛️ Plan 完成 → 💻 Write 完成 → 🛡️ L4 Verify 完成 → 🧪 Test 完成 → 🔍 Refine 完成 → 🚀 流水线结束
```

---

## 4. 输出产物

保存到 `--output` 指定的目录（默认 `~/.openclaw/workspace-coding-advisor/output/multi_agent_codegen/`）：

```
plan.md        # Plan 架构设计
code.py        # Write 完整代码
test_code.py   # Test pytest 测试用例
refine.md      # Refine 评审意见
```

---

## 5. 技术栈

| 组件 | 作用 |
|------|------|
| LangChain Anthropic | 调用 MiniMax-M3（Anthropic 协议） |
| MiniMax-M3 | 所有 4 个 Agent 共用 |
| Python | 3.10+ |

---

## 6. 关键约束（防 LLM bug）

- **单文件实现**：所有代码一个 .py 文件
- **方法名避免 builtin**：list/dict/str/int/type → 用 list_tasks/get_items
- **retry 输出完整文件**：Write 改进时必须输出完整新版本，不是改动片段
- **Test 看到完整代码**：Test 在 Write 之后启动，不是并行

---

## 7. 飞书通知机制（v3.0 新增，v3.1 增强）

### 通知触发点

| 触发时机 | 通知函数 | 内容 |
|---------|---------|------|
| 流水线启动 | `notify_pipeline_start` | 需求摘要 + 执行顺序（含 v3.1 L4 Verify 节点） |
| Plan 完成 | `notify_plan_done` | 产出字数 + 下一步预告 |
| Write 完成 | `notify_write_done` | 文件数 + 代码行数 + 方法数 |
| **Verify 完成 (v3.1)** | `notify_verify_done` | 通过 / 不通过 + 失败原因前 3 项 + 下一步 |
| Test 完成 | `notify_test_done` | 测试用例数 + 下一步预告 |
| Refine 完成 | `notify_refine_done` | 评分 + 问题统计 + 重写判定 |
| 流水线结束 | `notify_pipeline_end` | 最终评分 + 总耗时 + 产物路径 |

### 关闭通知

```python
# 在 multi_codegen.py 中设置
NOTIFY_ENABLED = False  # 设为 False 关闭飞书通知
```

### 接收者配置

```python
# 默认发送给老板
FEISHU_USER_OPEN_ID = "ou_991021547578f722d08533accc83651d"
```

---

## 8. 适用 vs 不适用

✅ 老板说"做个软件/工具/脚本"  
✅ 复杂需求需要架构设计 + 代码 + 测试 + 审查  
✅ 老板希望全程透明可见（飞书通知）  
❌ 1-2 行小脚本（单 agent 更快）  
❌ 纯分析/报告任务（非软件工程）  

---

## 9. 已知问题

- 依赖 langchain-anthropic，首次运行需安装（cli.sh 自动处理）
- `--output` 参数必须写在最后（`multi-codegen "需求" --output /path`）

## 10. 健康检查

```bash
# 跑 6 维度健康检查
cd ~/.openclaw/workspace-coding-advisor/skills/multi-agent-codegen
.venv/bin/python scripts/validate_skill.py
```

检查项：文件结构 / 依赖完整性 / 代码 import / 配置 / dry-run / Verify Agent

## 11. 版本历史

| 版本 | 日期 | 变化 |
|------|------|------|
| v2.0 | 2026-06-22 | 初版 4-Agent 流水线 |
| **v3.0** | **2026-07-20** | **全程飞书通知（6 节点）** |
| **v3.1** | **2026-09-23** | **L4 Verify Agent 接入主流水线 + 版本号统一** |
| **v3.2** | **2026-09-23 晚** | **SyntaxError hard fail retry（独立计数器）+ max_verify_retries 2→3** |
| **v3.3** | **2026-09-23 深夜** | **Test Verify Agent 接入（test_code.py 加 L4 Verify 保护）** |

---

*版本: v3.3.0*  
*作者: 码虫 coding-advisor*  
*创建日: 2026-06-22 | 升级: 2026-07-20（v3.0 飞书通知） / 2026-09-23（v3.1 L4 Verify 接入 + 版本号统一）/ 2026-09-23 晚（v3.2 SyntaxError hard retry）/ 2026-09-23 深夜（v3.3 Test Verify 接入）*
