---
name: openclaw-smartness-eval
description: OpenClaw 智能度综合评伌技能。围绕 14 个维度（含规划能力、幻觉控制）输出综合评分、证据、风险与趋势。对齐 CLEAR/T-Eval/Anthropic 行业标准。
triggers:
version: "0.3.2"
status: beta
updated: 2026-03-16
provides: ["smartness-evaluation", "capability-audit", "self-eval", "benchmark-aggregation", "trend-analysis"]
os: ["darwin", "linux"]
clawdbot: {"emoji": "🎯", "category": "evaluation", "priority": "high"}
---

# OpenClaw Smartness Eval

用于评估 OpenClaw 是否真的“更聪明”，而不是只看单次回答是否看起来不错。

## 适用场景

- **版本升级后回归**：确认能力是否真的提升
- **每周 / 每月自评**：输出结构化能力报告
- **发现退化**：查看哪个维度下降最快
- **准备对外展示**：生成统一口径的能力评估结果

## 命令

### 1) 标准评估

```bash
python3 skills/openclaw-smartness-eval/scripts/eval.py --mode standard
```

### 2) 快速评估

```bash
python3 skills/openclaw-smartness-eval/scripts/eval.py --mode quick
```

### 3) 深度评估

```bash
python3 skills/openclaw-smartness-eval/scripts/eval.py --mode deep --compare-last
```

### 4) 只输出 Markdown

```bash
python3 skills/openclaw-smartness-eval/scripts/eval.py --mode standard --format markdown
```

### 5) 健康检查

```bash
python3 skills/openclaw-smartness-eval/scripts/check.py
```

## 输出内容

评估结果将写入：

- `state/smartness-eval/runs/<timestamp>.json`
- `state/smartness-eval/reports/<date>.md`
- `state/smartness-eval/history.jsonl`

输出结果包含：

- `overall_score`
- `grade`
- `dimension_scores`
- `expanded_scores`
- `evidence`
- `risk_flags`
- `upgrade_recommendations`
- `trend_vs_last`

### 6) LLM Judge 主观评分

```bash
python3 skills/openclaw-smartness-eval/scripts/eval.py --mode standard --llm-judge
```

需设置 `DEEPSEEK_API_KEY` 或 `OPENAI_API_KEY` 环境变量。
该功能会发起外部 API 请求，默认不开启，仅在显式传入 `--llm-judge` 时启用。

## 输出新增字段 (v0.2)

- `dimension_spread` — 维度间离散度
- `trend_vs_last.dimension_deltas` — 各维度分数变化
- `trend_vs_last.degradation_alert` — 退化超过 5 分的维度
- `pass_at_k` — deep 模式下各测试的 pass@k 可靠性
- `llm_judge` — LLM 裁判主观评分和评语

## 数据来源

- `state/response-latency-metrics.json`
- `state/error-tracker.json` (时间窗口过滤)
- `state/pattern-library.json`
- `state/cron-governor-report.json`
- `state/benchmark-results/history.jsonl`
- `state/v5-orchestrator-log.json`
- `state/v5-finalize-log.json`
- `state/message-analyzer-log.json` (真实日志抽样)
- `state/reflection-reports/` (反思报告)
- `state/alerts.jsonl` (告警日志)
- `state/rule-candidates.json`
- `.reasoning/reasoning-store.sqlite` (推理知识库)
- `scripts/regression-metrics-report.py` (回归指标)
- 任务集中的 34 项规则测试命令
- 随机探针测试 (反作弊)

## 模式说明

- `quick` — 小样本 + 关键日志，~10 个测试
- `standard` — 默认周度评估，~25 个测试 + 2 个随机探针
- `deep` — 全部测试 x2 重复运行 + pass@k + 30天窗口 + 趋势对比

## 安全声明 / Security Declaration

本技能被设计为**只读评估工具**，以下是完整的行为声明：

### 文件读取（只读）

本技能**只读取**以下工作区状态文件，**不修改任何现有文件**：

| 文件 | 用途 | 写入？ |
|------|------|--------|
| `state/response-latency-metrics.json` | 延迟 P50/P95 计算 | ❌ 只读 |
| `state/error-tracker.json` | 错误修复率统计 | ❌ 只读 |
| `state/pattern-library.json` | 模式库健康度 | ❌ 只读 |
| `state/cron-governor-report.json` | Cron 任务状态 | ❌ 只读 |
| `state/benchmark-results/history.jsonl` | 基准测试通过率 | ❌ 只读 |
| `state/v5-orchestrator-log.json` | 编排器使用量 | ❌ 只读 |
| `state/v5-finalize-log.json` | Finalize 审批率 | ❌ 只读 |
| `state/message-analyzer-log.json` | 真实交互采样 | ❌ 只读 |
| `state/reflection-reports/` | 自省报告数量 | ❌ 只读 |
| `state/alerts.jsonl` | 告警频率统计 | ❌ 只读 |
| `.reasoning/reasoning-store.sqlite` | 推理深度查询 | ❌ 只读 |

### 文件写入（仅限自身输出目录）

本技能**仅写入** `state/smartness-eval/` 目录下的评估结果：

- `state/smartness-eval/runs/<timestamp>.json` — 完整评估 JSON
- `state/smartness-eval/reports/<date>.md` — Markdown 报告
- `state/smartness-eval/history.jsonl` — 历史评分记录

### 命令执行

本技能通过 `subprocess` 运行 `task-suite.json` 中定义的测试命令：

- **所有命令都经过白名单校验**（`validate_command()` 函数）
- **禁止**：内联 Python/Shell 代码、绝对路径、管道操作、危险系统命令
- **只允许**：以 `python3 scripts/`、`cat state/`、`sqlite3 .reasoning/` 等安全前缀开头的命令
- 命令执行超时限制为 30 秒

### 网络访问

- **默认无网络访问**
- 仅在用户显式传入 `--llm-judge` 参数时，会调用 DeepSeek/OpenAI API（需用户自行配置 API Key）
- 除此之外，本技能完全离线运行

### 无持久化副作用

- 不修改 OpenClaw 配置
- 不安装任何依赖
- 不修改系统文件
- 不发送遥测数据
- 仅使用 Python 标准库

---

## 文件结构

```text
openclaw-smartness-eval/
├── SKILL.md
├── _meta.json
├── config/
│   ├── config.json
│   ├── rubrics.json
│   └── task-suite.json
└── scripts/
    ├── eval.py
    └── check.py
```
