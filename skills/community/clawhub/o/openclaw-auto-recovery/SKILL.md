---
name: openclaw-auto-recovery
description: OpenClaw 基础设施心跳监控与自动恢复。用于：部署/卸载心跳守护进程、配置主机监控（Gateway/磁盘/内存/CPU/进程）、设置飞书告警、自动重启故障 Gateway。当用户提到"心跳监控"、"heartbeat daemon"、"服务器告警"、"自动重启"、"健康检查"、"auto recovery"时触发。
version: 1.0.7
changelog: |
  - 1.0.7: 修复 CPU 检测精度：改用 vmstat 1 1（列15固定为idle），替代 top 避免中文locale下列位置不稳定问题；99992361为飞书API频率限制非代码bug，建议检查alert发送频率
  - 1.0.6: 修复中文locale兼容性问题：check_memory改用awk NR==2；check_cpu原方案(top/grep)有缺陷已废弃
  - 1.0.4: 修复log语句中全角字符导致的bash语法错误
  - 1.0.3: 新增RELEASE.md完整升级历史文档
  - 1.0.2: 修复回滚逻辑缺陷：重启失败时依次尝试last-good.1/2/3，避免回滚到刚保存的坏文件；MD5去重保存；新增rollback_one()
  - 1.0.1: 将示例App ID改为占位符，避免泄露真实值
---

# infra-heartbeat

OpenClaw 基础设施心跳守护进程，负责：

- **Gateway 监控**：WebSocket 连通性检测，DOWN 时自动重启（最多连续 3 次）
- **主机资源**：磁盘 / 内存 / CPU / 进程监控，超阈值飞书告警
- **配置安全**：变更前自动备份，JSON 损坏时自动回滚
- **进程保活**：由 systemd 托管，崩溃自动重启，不依赖 nohup

## 快速开始

### 首次安装

```bash
bash ~/.openclaw/extensions/infra-heartbeat/scripts/install-heartbeat.sh
```

交互式安装向导会要求填写必填配置（飞书 App ID/Secret、Gateway Token、通知目标）。

### 常用操作

```bash
# 查看状态
systemctl --user status heartbeat-daemon

# 查看日志
tail -f ~/.openclaw/workspace-infra/heartbeat.log

# 重启服务
systemctl --user restart heartbeat-daemon

# 卸载
bash ~/.openclaw/extensions/infra-heartbeat/scripts/uninstall-heartbeat.sh
```

## 配置

配置文件：`~/.config/infra-heartbeat/config.env`

详细配置参数见 [references/configure.md](references/configure.md)。

### 关键参数速查

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `FEISHU_APP_ID` | ✅ | — | 飞书应用 App ID |
| `FEISHU_APP_SECRET` | ✅ | — | 飞书应用 App Secret |
| `GATEWAY_TOKEN` | ✅ | — | Gateway 访问令牌 |
| `TARGET_OPEN_ID` | ✅ | — | 通知目标 open_id |
| `CHECK_INTERVAL` | — | 180s | 检测间隔 |
| `DISK_THRESHOLD` | — | 80% | 磁盘告警阈值 |
| `MEM_THRESHOLD` | — | 85% | 内存告警阈值 |
| `CPU_THRESHOLD` | — | 60% | CPU 告警阈值 |

### 修改配置后生效

```bash
systemctl --user restart heartbeat-daemon
```

## 部署到新机器

1. 将 `infra-heartbeat/` skill 目录复制到新机器 `~/.openclaw/extensions/`
2. 运行 `bash install-heartbeat.sh`
3. 填写新机器的 `GATEWAY_TOKEN`、`TARGET_OPEN_ID` 等参数

无需修改脚本，配置全部外部化。

## 自动恢复逻辑

```
锚点机制：
  - 每次检测到 Gateway UP → 若配置 MD5 有变化 → 保存 last-good.1/.2/.3（最多3份，轮转）
  - last-good.N 之间 MD5 均不同，确保每份都是真实变更过的配置

Gateway DOWN
  ├─ 连续失败 < 3 次
  │   ├─ 备份当前配置（仅供历史记录，不用于回滚）
  │   ├─ 校验 JSON → INVALID → rollback_one（仅回滚，不重启）
  │   ├─ restart → sleep 60 → check
  │   │   ├─ UP   → 成功，清零计数，下次 UP 时更新 last-good
  │   │   └─ DOWN → rollback_config() 依次尝试：
  │   │               last-good.1 → restart → check
  │   │               ↓ DOWN      last-good.2 → restart → check
  │   │               ↓ DOWN      last-good.3 → restart → check
  │   │               ↓ DOWN      → 失败计数+1，告警"需人工介入"
  │   └─ 连续 ≥ 3 次 → 停止自动重启
  │
  └─ 连续失败 ≥ 3 次 → 停止自动重启 → 发"需人工介入"通知
```

## 与 cron 健康检查的区别

- **Heartbeat Daemon**：3 分钟间隔，发现故障自动恢复，systemd 进程保活
- **Cron `daily-health-check`**：每天一次，纯告警，不自动恢复

两者互为补充，生产环境建议同时运行。

## 获取当前配置参考值

```bash
# Gateway Token
cat ~/.openclaw/openclaw.json | jq -r '.gateway.auth.secret'

# 查看当前运行的配置
systemctl --user show heartbeat-daemon --property=ExecStart
```
