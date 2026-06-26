# OpenClaw 安全卫士（openclaw-safety-guard）🛡️

OpenClaw 安全卫士的 Clawhub 发布 slug 为 `openclaw-safety-guard`，内部技术代号仍为 `openclaw-watchdog`。它是 OpenClaw 项目全链路健康监控工具，默认工作日自动扫描 7 个维度，生成本地 dashboard 和 JSON 日志，并通过飞书私信发送简报。即使没有 Cursor，也可以直接看 dashboard、下载 JSON、交给本地编辑器或后续 fix 流程处理。

## 扫描维度

| 维度 | 说明 |
|---|---|
| 安全 | plist 权限、git 密钥泄露、exec approvals 状态 |
| 心跳 | heartbeat 配置合理性、lightContext、模型成本 |
| 定时任务 | cron job 状态、连续失败、时区配置 |
| 记忆 | MEMORY.md 新鲜度、跨 workspace 冲突、孤儿引用 |
| 共享文件 | shared/DECISIONS.md 传播一致性 |
| 通讯 | 飞书账号配置、binding 完整性 |
| 代码规范 | CLAUDE.md 更新频率、skill 路径规范 |

## 安装

### 前置条件

1. OpenClaw Gateway 已运行
2. `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 已配置在 Gateway plist 的 `EnvironmentVariables` 中
3. 本机已安装 `node`（首次 build frontend 需要）

### Mac 一键安装（适合同事本地装，不想找隐藏目录）

如果你已经拿到这个仓库压缩包，不想自己去找 `~/.openclaw`，直接双击仓库根目录里的：

```bash
install-openclaw-safety-guard.command
```

安装器会自动：

1. 扫描这台 Mac 上的 OpenClaw 项目
2. 让你选择要安装到哪一个 workspace
3. 把 `openclaw-safety-guard` 复制到正确的 `skills/` 目录
4. 打开安装结果目录，并提示下一步初始化方式

如果你更习惯终端，也可以这样运行：

```bash
bash install-openclaw-safety-guard.command /你的/OpenClaw项目路径 techops
```

### 安装命令（在飞书对 Agent 说）

```
帮我安装 openclaw-safety-guard
```

Agent 会执行：

```bash
clawhub install openclaw-safety-guard
python3 {baseDir}/scripts/setup.py --receive_id <你的 Feishu open_id>
```

**30 秒内你会收到第一份飞书健康报告。**

> ⚠️ 安装完成后重启 Gateway 使每日 cron 生效：
> ```bash
> openclaw gateway restart
> ```

## 使用

- **自动**：默认工作日 10:00（Asia/Shanghai）自动扫描并发送报告
- **手动**：对 Agent 说 `体检` 或 `生成健康大盘`

## 配置

安装后 `config.json` 自动生成。参考 `config.example.json` 了解全部配置项。

常用自定义项：

```json
{
  "notify": {
    "score_recovery_threshold": 3
  },
  "memory": {
    "checks": [{
      "id": "cross_workspace_conflict",
      "tracked_concepts": [
        {
          "name": "你的概念名",
          "keywords": ["关键词1", "关键词2"],
          "authority": "shared/DECISIONS.md"
        }
      ]
    }]
  },
  "security": {
    "checks": [{
      "id": "knowledge_freshness",
      "enabled": true,
      "target": ".openclaw/workspace-techops/skills/your-knowledge-dir"
    }]
  }
}
```

## Dashboard

每次扫描生成以下产物：

- `data/dashboard.html`：本地 dashboard，用浏览器直接打开
- `data/latest_status.json`：聚合后的完整扫描结果，龙虾优先读取这个
- `data/latest_heartbeat.json` / `latest_cron.json` / ...：各维度原始扫描结果，排查时按需读取
- `data/logs/YYYY-MM-DD_HH-MM/`：每次运行归档快照

dashboard Header 提供 JSON 下载入口：

- 主入口：`latest_status.json`
- 二级入口：7 个维度原始 JSON 白名单

如果同事也是本地安装，且龙虾和 watchdog 在同一个本地项目里，龙虾通过脚本就能读取这些文件，不依赖 Cursor。

---

## Installation (English)

### Prerequisites

1. OpenClaw Gateway running
2. `FEISHU_APP_ID` and `FEISHU_APP_SECRET` set in Gateway plist `EnvironmentVariables`
3. `node` installed (for first-time frontend build)

### Install via clawhub

Tell your OpenClaw agent in Feishu:

```
Please install openclaw-safety-guard
```

The agent will run:

```bash
clawhub install openclaw-safety-guard
python3 {baseDir}/scripts/setup.py --receive_id <your Feishu open_id>
```

You'll receive your first health report within 30 seconds.

Restart Gateway to activate the daily cron job:

```bash
openclaw gateway restart
```
