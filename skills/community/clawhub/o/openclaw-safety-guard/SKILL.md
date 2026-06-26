---
name: openclaw-safety-guard
description: "OpenClaw 安全卫士（发布 slug：openclaw-safety-guard，内部代号：openclaw-watchdog）：默认工作日 10:00 自动扫描 7 个维度（安全、记忆、心跳、定时任务、共享文件、通讯、代码规范），生成健康评分和可视化 Dashboard，通过飞书私信发送报告；没有 Cursor 也可直接看 dashboard 和下载 JSON。用户说「体检」「生成健康大盘」「跑安全检查」时手动触发。"
metadata:
  clawdbot:
    emoji: "🛡️"
    requires:
      bins: [python3, node, npm]
      env: [FEISHU_APP_ID, FEISHU_APP_SECRET]
    primaryEnv: FEISHU_APP_ID
---

# OpenClaw 安全卫士（openclaw-safety-guard）

OpenClaw 安全卫士的 Clawhub 发布 slug 为 `openclaw-safety-guard`，内部技术代号仍为 `openclaw-watchdog`。它是 OpenClaw 项目全链路健康监控工具，默认工作日自动扫描 7 个维度，生成评分和可视化 Dashboard，通过飞书发送报告。没有 Cursor 也可以直接查看 dashboard 和下载 JSON 日志。

## 安装（clawhub）

```bash
clawhub install openclaw-safety-guard
```

安装完成后，Agent 立即执行 post-install 初始化：

```bash
python3 {baseDir}/scripts/setup.py --receive_id <当前对话 sender 的 Feishu open_id>
```

`--receive_id` 由 Agent 从当前会话 context 中自动获取（即安装者本人的 open_id），无需手动填写。

setup.py 自动完成：
1. 写入 `{baseDir}/config.json`（绑定通知接收人）
2. 在 `.openclaw/state/cron/jobs.json` 注册每日扫描任务
3. **立即执行一次完整扫描**，安装者 30 秒内收到第一份飞书健康报告

> ⚠️ 安装完成后重启 Gateway 使 cron 生效：`openclaw gateway restart`

## 前置条件

- `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 已配置在 Gateway plist 的 `EnvironmentVariables` 中
- 本机已安装 `node`（用于首次 build frontend）
- OpenClaw Gateway 已运行

## 触发方式

1. **每日自动**：安装时注册的 cron job，默认工作日 10:00（Asia/Shanghai）触发
2. **手动触发**：在飞书群对 Agent 说 `体检`、`生成健康大盘`、`跑一遍安全检查`

## 执行流程

```
触发
  ↓
Step 1: 执行 7 个探针扫描
  python3 {baseDir}/scripts/run_pipeline.py
  内部依次调用：
    scan_heartbeat.py   → 心跳监控维度
    scan_standards.py   → 代码规范维度
    scan_memory.py      → 记忆健康维度
    scan_cron.py        → 定时任务维度
    scan_shared.py      → 共享文件维度
    scan_comm.py        → 通讯配置维度
    scan_security.py    → 安全维度
  ↓
Step 2: 聚合评分（含与上次对比的 score_delta）
    aggregate_watchdog.py
  ↓
Step 3: 生成可视化 Dashboard HTML（含飞书 bot 头像）
    generate_dashboard.py
  ↓
Step 4: 按次归档到 data/logs/YYYY-MM-DD_HH-MM/
  ↓
Step 5: 飞书私信通知（含健康分、问题列表、Dashboard 本地路径）
    notify_feishu.py
  ↓
Step 6: 自动执行 GREEN 安全修复（仅 chmod 类低风险操作）
    fix_green.py
```

## 手动重发通知

```bash
python3 {baseDir}/scripts/notify_feishu.py
```

## 配置文件

`config.json` 由 setup.py 自动生成，参考 `config.example.json` 了解全部可配项。

关键字段：

| 字段 | 说明 |
|---|---|
| `notify.receive_id` | 接收飞书通知的 open_id（setup.py 自动填入） |
| `notify.score_recovery_threshold` | 分数提升超过此值时用「恭喜」语气（默认 3） |
| `memory.checks[cross_workspace_conflict].tracked_concepts` | 自定义需要跨 workspace 监控一致性的概念 |
| `security.checks[knowledge_freshness].target` | 知识库目录路径（可选，不填则跳过此检查） |

## 关键文件

| 文件 | 说明 |
|---|---|
| `data/latest_status.json` | 本次扫描完整结果（含 score_delta） |
| `data/dashboard.html` | 最新 Dashboard，浏览器本地打开 |
| `data/history.json` | 问题生命周期历史（first_seen / resolved_at） |
| `data/logs/YYYY-MM-DD_HH-MM/` | 按次归档的原始扫描日志（最多保留 30 次） |
| `config.json` | 运行时配置（由 setup.py 生成，不提交到 git） |
| `config.example.json` | 配置模板（可提交到 git） |

## 错误处理

| 失败步骤 | 降级策略 |
|---|---|
| 探针执行报错 | 该维度显示 N/A，不影响其他维度 |
| Dashboard 生成失败 | 通知仍发出，不含 Dashboard 路径 |
| 飞书通知失败 | 打印 ERROR 日志，pipeline 不中断 |
| Bot info 获取失败 | Dashboard 显示默认缩写，不影响报告发送 |
