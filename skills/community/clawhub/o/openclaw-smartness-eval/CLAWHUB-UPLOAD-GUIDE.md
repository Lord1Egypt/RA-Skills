# ClawHub 上传指导文档 — openclaw-smartness-eval

## 前置条件

1. **OpenClaw Gateway 在线** — ClawHub 操作需要 Gateway 运行
2. **已登录 ClawHub** — 确认 `clawhub whoami` 返回你的账号信息
3. **技能目录完整** — 运行健康检查确认：
   ```bash
   python3 skills/openclaw-smartness-eval/scripts/check.py
   ```

## 目录结构确认

上传前确保以下文件存在且内容正确：

```text
skills/openclaw-smartness-eval/
├── SKILL.md              # 技能描述文档（ClawHub 展示页面内容）
├── _meta.json            # 技能元数据（slug, version, description）
├── config/
│   ├── config.json       # 评估配置（权重、模式、窗口）
│   ├── rubrics.json      # 12 维度 0-5 量表
│   └── task-suite.json   # 28 项测试定义
└── scripts/
    ├── eval.py           # 核心评估引擎 (v0.2.0)
    └── check.py          # 健康检查脚本
```

## 上传步骤

### Step 1: 验证元数据

确认 `_meta.json` 中的字段：

```json
{
  "ownerId": "your-clawhub-id",     // ← 改为你的 ClawHub ID
  "slug": "openclaw-smartness-eval",
  "version": "0.2.0",
  "name": "OpenClaw Smartness Eval",
  "description": "..."
}
```

> **注意**: `ownerId` 需要改为你在 ClawHub 上的实际 ID，不是 `local-openclaw`。
> 用 `clawhub whoami` 查看你的 ID。

### Step 2: 本地测试

```bash
# 快速评估确认无报错
python3 skills/openclaw-smartness-eval/scripts/eval.py --mode quick --no-probes

# 标准评估（推荐上传前跑一次）
python3 skills/openclaw-smartness-eval/scripts/eval.py --mode standard --format markdown
```

### Step 3: 发布到 ClawHub

```bash
clawhub publish skills/openclaw-smartness-eval
```

如果是首次发布，ClawHub 会自动创建新技能页面。
如果是更新，确保 `_meta.json` 中的 `version` 已递增。

### Step 4: 验证上传

```bash
clawhub info openclaw-smartness-eval
```

确认版本号、描述、文件列表正确。

## 版本管理

每次更新后上传：

1. 修改 `_meta.json` 中的 `version`（遵循 semver）
2. 同步修改 `config/config.json` 中的 `version`
3. 更新 `SKILL.md` 中 frontmatter 的 `version`
4. 重新运行 `clawhub publish`

版本号规则：
- **patch** (0.2.0 → 0.2.1): 修复 bug、微调公式权重
- **minor** (0.2.0 → 0.3.0): 新增维度、新数据源、新测试
- **major** (0.2.0 → 1.0.0): 评分体系重构、不向后兼容

## 依赖说明

此技能依赖以下 OpenClaw 组件（不随技能上传，需目标环境已有）：

| 依赖 | 用途 | 必需? |
|------|------|-------|
| `scripts/message-analyzer-v5.py` | 意图识别测试 | 是 |
| `scripts/multi-step-reasoning-v5.py` | 推理模板测试 | 是 |
| `scripts/self-audit.py` | 自审能力测试 | 是 |
| `scripts/benchmark.py` | Benchmark 测试 | 标准/深度模式 |
| `scripts/security-config-audit.py` | 安全审计测试 | 标准模式 |
| `scripts/cron-governor.py` | Cron 状态测试 | 标准模式 |
| `scripts/proactive-iteration-engine-v5.py` | 迭代引擎测试 | 标准模式 |
| `scripts/reasoning-structured-store-v5.py` | 推理库统计 | 标准模式 |
| `scripts/regression-metrics-report.py` | 回归指标 | 标准模式 |
| `.reasoning/reasoning-store.sqlite` | 推理知识库 | 推荐 |
| `state/error-tracker.json` | 错误追踪 | 推荐 |
| `state/response-latency-metrics.json` | 延迟指标 | 推荐 |

> 在缺少某些依赖时，评估不会崩溃，但对应维度的分数会使用 fallback 默认值。

## 常见问题

### Q: `clawhub publish` 报 "not authenticated"
```bash
clawhub login
```

### Q: 上传后别人安装报脚本找不到
此技能的测试命令引用了 `scripts/` 目录下的脚本，这些脚本属于 OpenClaw 核心，
不会随技能一起分发。安装此技能的用户需要有完整的 OpenClaw V5 环境。

### Q: 如何让别人只看到评估报告
运行后分享 `state/smartness-eval/reports/<date>.md` 即可，该文件为独立 Markdown。

### Q: LLM Judge 功能需要什么
需要设置环境变量 `DEEPSEEK_API_KEY` 或 `OPENAI_API_KEY`，并加 `--llm-judge` 参数。
不设置时此功能自动跳过，不影响其他评分。
