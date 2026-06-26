---
name: config-guardian
description: Protect openclaw.json with automatic rollback, lock mode, multi-version baseline snapshots, audit log, and SIGUSR1 gateway hot-reload. Use when you need to safeguard OpenClaw config from bad writes, detect unauthorized changes, or recover from config corruption automatically.
license: MIT
metadata:
  version: 1.0.4
  author: 大黑 #F_SEC
  tags: openclaw, config, guardian, security, systemd
  openclaw:
    requires:
      bins:
        - inotifywait
        - jq
        - sha256sum
      permissions:
        - root
      platform:
        - linux
      env: []
    install:
      - id: inotify-tools
        kind: apt
        package: inotify-tools
        bins: [inotifywait]
        label: Install inotify-tools (apt)
      - id: jq
        kind: apt
        package: jq
        bins: [jq]
        label: Install jq (apt)
---

# config-guardian（配置自愈）

自动监控 `openclaw.json`，写入失败自动回滚到上一个有效版本。支持磁盘持久化锁定模式、多版本快照、结构化审计日志、SIGUSR1 热重载。

## 功能一览

- **自动回滚**：任何写入触发验证，失败立即恢复到 baseline
- **锁定模式**：连续 3 次失败后进入锁定，所有写入强制回滚，监控不停止
- **持久化状态**：锁定状态落盘，守护重启后依然有效
- **多版本 baseline**：每次更新 baseline 前归档，保留最近 7 个有效版本
- **SIGUSR1 热重载**：回滚/验证通过后自动通知 gateway，无需手动重启
- **审计日志**：每次操作记录时间戳、事件类型、触发进程
- **自身完整性**：启动时 SHA256 自检，脚本被篡改则拒绝启动并告警
- **双端告警**：熔断时向 Discord + Telegram 发送告警

## 前提条件

- 系统：Linux，systemd 环境
- 依赖：`inotify-tools`（inotifywait）、`jq`
- 权限：root（守护以 root 运行）
- OpenClaw gateway 已部署（`/root/.openclaw/openclaw.json` 存在）

```bash
# 安装依赖
apt-get install -y inotify-tools jq
```

## 安装

```bash
bash scripts/install.sh
```

安装后验证：

```bash
systemctl status openclaw-config-guardian
# 应显示：active (running)，日志含 🛡️ guardian v3.2 started
```

## 核心命令速查

```bash
# 查看守护状态
systemctl status openclaw-config-guardian

# 实时日志
journalctl -u openclaw-config-guardian -f

# 查看锁定状态
jq '.locked, .attempts, .last_error' /root/.openclaw/backups/config/.guardian_state.json

# 解锁（锁定模式下，配置修复后执行）
openclaw-config-guardian unlock

# 查看审计日志
tail -30 /root/.openclaw/backups/config/guardian_audit.log

# 查看 baseline 历史
ls -lth /root/.openclaw/backups/config/baseline_history/

# 重启守护
systemctl restart openclaw-config-guardian
```

## 解锁流程

1. 通过官方通道修复配置：`openclaw config.patch ...`
2. 执行解锁（内置 validate，通过才解锁）：
   ```bash
   openclaw-config-guardian unlock
   ```
3. 确认：`jq '.locked' /root/.openclaw/backups/config/.guardian_state.json` → `false`

## 更新 guardian 脚本后必须刷新 checksum

```bash
sha256sum /usr/local/bin/openclaw-config-guardian > \
  /root/.openclaw/backups/config/.guardian_checksum
systemctl restart openclaw-config-guardian
```


## 安全说明

### 为什么需要 root 权限

guardian 以 root 运行是必要的：

1. **监控目标**：`/root/.openclaw/openclaw.json` 归属 root，非 root 无法可靠监控
2. **回滚操作**：需要覆盖写入配置文件，需要 root 权限
3. **systemd 交互**：发送 SIGUSR1 给 Gateway 进程需要匹配权限
4. **无网络访问**：guardian 不发起任何网络请求，无数据外传风险
5. **本地闭环**：所有操作（监控、验证、回滚、告警）完全在本机执行

guardian 不读取任何密钥、不执行动态代码，root 权限仅用于文件系统操作和进程信号。

**关于告警网络访问**：guardian 通过调用本机 `openclaw message send` CLI 命令发送熔断告警（Discord/Telegram）。网络连接由已运行的 OpenClaw Gateway 进程负责，guardian 脚本本身不直接发起任何网络连接，不持有任何凭证。如未部署 OpenClaw Gateway，告警调用会静默失败（`2>/dev/null || true`），不影响核心保护功能。

**关于 guardian 脚本**：runtime 脚本已打包在 `scripts/openclaw-config-guardian`，install.sh 从包内复制到 `/usr/local/bin/`，不从外部获取任何二进制文件。

## 参考文档

- `references/DESIGN.md` — 架构设计与状态机说明
- `references/USAGE.md` — 日常使用与失败处理
- `references/OPERATION.md` — 运维与故障排除
- `references/ARCHIVE.md` — 版本历史与文件清单
