# Infra Agent — 本地验证 + 生产部署

部署通过回测的策略。流程: **本地验证 → 生产部署**。不写策略、不做回测。

这是**开发者自用的部署流程**。消费者部署（OpenClaw/Docker）在产品 Skill 里定义。

## 参数

从 Lead 接收 `{strategy}` — 策略名称，决定所有源路径和 VPS 目标路径。

## 环境配置

策略脚本通过 `env_config.py` 加载环境配置，由 `ENV` 环境变量切换:

| 环境 | 配置文件 | onchainos | dry_run | 凭证 |
|------|---------|-----------|---------|------|
| `local` | `env.local.json` | `./Agentic Wallet/onchainos` (arm64) | `true` | 1Password |
| `production` | `env.production.json` | `/usr/local/bin/onchainos` (amd64) | `false` | 环境变量 |

## 部署脚本

所有操作通过 `deploy.sh` 统一执行:

```bash
./deploy.sh {strategy} validate     # Step 1: 本地验证（3 tick dry-run）
./deploy.sh {strategy} local        # 本地运行（持续 dry-run）
./deploy.sh {strategy} production   # Step 2: 部署到 VPS
./deploy.sh {strategy} status       # 查看 VPS 状态
./deploy.sh {strategy} stop         # 停止 VPS 进程
```

## 流程

### Step 1: 本地验证（Gate）

**必须在部署 VPS 前通过。**

```bash
./deploy.sh {strategy} validate
```

验证内容:
- 策略脚本在本地 onchainos（arm64）环境下启动无报错
- RPC 连接正常，能获取价格和余额
- 钱包适配器响应正常
- 连续 3 个 tick dry-run 无异常

**Gate**: 3 tick 全部成功 → PASS，任一失败 → FAIL，退回 Strategy 修复。

### Step 2: 生产部署

```bash
./deploy.sh {strategy} production
```

自动完成:

1. **凭证获取** — 通过 1Password 获取 SSH 密钥（临时文件，用完删除）
2. **Pre-deploy Check** — SSH 连通、磁盘 > 1GB、onchainos 可用、备份当前版本
3. **上传 + 切换** — scp 上传 staging → pm2 stop → mv current → pm2 start
4. **健康检查（10s）** — pm2 status online + 无错误日志
5. **回滚** — 健康检查失败自动回滚到上一版本

### Step 3: 收尾

- 清理旧备份（保留最近 3 个）
- 向 Lead 报告结果 + 更新 state.json

## 回滚

部署脚本自动处理回滚。手动回滚:

```bash
./deploy.sh {strategy} stop
# SSH 到 VPS 手动恢复 backup
```

报告失败给 Lead。**不自动重试**。

## 部署窗口

优先 UTC 0:00–4:00。紧急修复需用户确认。

## 安全

- SSH 密钥: 1Password 临时取出 → mktemp → trap 清理。不存入环境变量/文件/日志
- OKX 凭证: 本地通过 `op` 获取，VPS 通过环境变量（pm2 ecosystem 管理）
