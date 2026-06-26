# OpenClaw 配置守护 - 运行与维护

> 文档版本：v3.0  
> 最后更新：2026-03-19（大黑 #F_SEC）  
> 对应脚本版本：guardian v3

---

## 1. 服务生命周期

### 1.1 启动

```bash
systemctl daemon-reload
systemctl enable --now openclaw-config-guardian
systemctl status openclaw-config-guardian
# 应显示：active (running)
# 日志应显示：🛡️ guardian v3 started
```

### 1.2 停止 / 重启

```bash
systemctl stop openclaw-config-guardian
systemctl restart openclaw-config-guardian
# 强制重启
systemctl kill -s KILL openclaw-config-guardian && systemctl start openclaw-config-guardian
```

---

## 2. 监控与日志

### 2.1 实时日志

```bash
journalctl -u openclaw-config-guardian -f
journalctl -u openclaw-config-guardian -n 100 --no-pager
```

### 2.2 结构化审计日志（v3 新增）

位置：`/root/.openclaw/backups/config/guardian_audit.log`

格式：
```
<ISO时间> | GUARDIAN_PID=<pid> | ACTION=<事件> | writer=<进程>(pid=<pid>) | <详情>
```

事件类型：
- `GUARDIAN_START` — 守护启动
- `BASELINE_INIT` — 首次创建 baseline
- `VALIDATE_OK` — 验证通过，baseline 已更新
- `VALIDATE_FAIL` — 验证失败，已回滚
- `CIRCUIT_BREAK` — 熔断触发，进入锁定模式
- `LOCKED_REVERT` — 锁定模式下自动撤销写入
- `GATEWAY_RELOAD` — SIGUSR1 已发送至 gateway
- `BASELINE_CORRUPT` — baseline 校验失败
- `BASELINE_RESTORED` — 从历史恢复 baseline

```bash
# 查看最近事件
tail -20 /root/.openclaw/backups/config/guardian_audit.log
# 查找熔断事件
grep CIRCUIT_BREAK /root/.openclaw/backups/config/guardian_audit.log
```

### 2.3 状态文件

```bash
cat /root/.openclaw/backups/config/.guardian_state.json
jq '.attempts, .locked, .last_error' /root/.openclaw/backups/config/.guardian_state.json
```

### 2.4 日志标记速查

| 标记 | 含义 |
|---|---|
| 🛡️ | 守护启动 |
| 🔄 | 检测到变更 / 回滚中 |
| ✅ | 验证通过 |
| ❌ | 验证失败 |
| ⛔ | 熔断锁定 / 自身校验失败 |
| 📦 | baseline 归档到历史 |
| 📡 | SIGUSR1 已发给 gateway |
| ♻️ | 从历史恢复 baseline |
| ⚠️ | 软警告（不停止运行）|

---

## 3. 备份管理

### 3.1 目录结构

```
/root/.openclaw/backups/config/
├── baseline.bak              # 最新有效版本（回滚源）
├── baseline.bak.sha256       # baseline 完整性校验（v3 新增）
├── baseline_history/         # 多版本历史（保留最近 7 个）
│   ├── baseline_20260319_152819.bak
│   └── ...
├── attempts/                 # 每次变更快照（保留最近 20 个）
│   └── openclaw.json.2026-03-19-152819.bak
├── .guardian_state.json      # 守护状态
├── .guardian_checksum        # guardian 脚本自身 SHA256（v3 新增）
└── guardian_audit.log        # 结构化审计日志（v3 新增）
```

### 3.2 从 baseline 历史恢复

```bash
# 查看历史版本
ls -lth /root/.openclaw/backups/config/baseline_history/

# 选择版本恢复
systemctl stop openclaw-config-guardian
cp /root/.openclaw/backups/config/baseline_history/baseline_20260319_XXXXXX.bak \
   /root/.openclaw/openclaw.json
openclaw config validate
openclaw gateway restart
systemctl start openclaw-config-guardian
```

### 3.3 baseline 完整性校验

```bash
sha256sum -c /root/.openclaw/backups/config/baseline.bak.sha256
# OK = 完整
# FAILED = 损坏，guardian 会自动尝试从历史恢复
```

---

## 4. 熔断与锁定模式（v3 行为）

### v3 与 v2 的关键区别

| 行为 | v2 | v3 |
|---|---|---|
| 熔断后 | `exit 1`，停止监控 | 进入锁定模式，**监控继续** |
| 锁定期间写入 | 无保护（裸奔） | 自动回滚，不验证 |
| 熔断通知 | 无 | Discord #报告 + TG 双发告警 |
| 解锁方式 | 手动重置状态+重启 | 同左（不允许自动解锁）|

### 锁定模式解除流程

```bash
# 1. 用官方通道修复配置
openclaw config.patch ...

# 2. 验证配置有效
openclaw config validate

# 3. 手动解锁状态文件
jq '.locked = false | .attempts = 0' \
  /root/.openclaw/backups/config/.guardian_state.json > /tmp/state_fix.json \
  && mv /tmp/state_fix.json /root/.openclaw/backups/config/.guardian_state.json

# 4. 重启守护
systemctl restart openclaw-config-guardian
```

---

## 5. Gateway 自动重载（v3 新增）

守护在以下时机自动发送 `SIGUSR1` 给 `openclaw-gateway` 进程：
- 验证通过，baseline 更新后
- 回滚成功后

**注意**：SIGUSR1 触发的是 gateway **热重载**（内存配置同步），而非重启。若需完整重启仍需手动执行：
```bash
openclaw gateway restart
```

---

## 6. Guardian 自身完整性（v3 新增）

```bash
# 查看当前 checksum
cat /root/.openclaw/backups/config/.guardian_checksum

# 手动验证
sha256sum -c /root/.openclaw/backups/config/.guardian_checksum

# 合法更新脚本后，必须刷新 checksum
sha256sum /usr/local/bin/openclaw-config-guardian > \
  /root/.openclaw/backups/config/.guardian_checksum
systemctl restart openclaw-config-guardian
```

**重要**：每次更新 guardian 脚本后必须刷新 checksum，否则下次启动自检失败会拒绝运行。

---

## 7. 故障场景速查

### 守护无法启动
```bash
journalctl -u openclaw-config-guardian -n 50 --no-pager
# 常见原因: inotify-tools 未装、openclaw.json 不存在、checksum 校验失败
```

### 守护启动失败：自身校验失败
```bash
# 合法更新后刷新 checksum
sha256sum /usr/local/bin/openclaw-config-guardian > \
  /root/.openclaw/backups/config/.guardian_checksum
systemctl restart openclaw-config-guardian
```

### baseline 损坏
```bash
# guardian 会自动从 baseline_history/ 恢复
# 如需手动:
ls -t /root/.openclaw/backups/config/baseline_history/
cp /root/.openclaw/backups/config/baseline_history/baseline_XXXXXX.bak \
   /root/.openclaw/backups/config/baseline.bak
sha256sum /root/.openclaw/backups/config/baseline.bak > \
   /root/.openclaw/backups/config/baseline.bak.sha256
```

### 误删 backups 目录
```bash
systemctl stop openclaw-config-guardian
mkdir -p /root/.openclaw/backups/config/attempts \
         /root/.openclaw/backups/config/baseline_history
cp /root/.openclaw/openclaw.json /root/.openclaw/backups/config/baseline.bak
sha256sum /root/.openclaw/backups/config/baseline.bak > \
          /root/.openclaw/backups/config/baseline.bak.sha256
sha256sum /usr/local/bin/openclaw-config-guardian > \
          /root/.openclaw/backups/config/.guardian_checksum
echo '{"attempts":0,"last_error":null,"last_backup":null,"locked":false,"failed_at":null}' > \
  /root/.openclaw/backups/config/.guardian_state.json
touch /root/.openclaw/backups/config/guardian_audit.log
systemctl start openclaw-config-guardian
```

---

## 附录 A：版本历史

| 版本 | 时间 | 内容 |
|---|---|---|
| v1.0 | 2026-03-12 | 初版（单文件监控）|
| v2.0 | 2026-03-12 | 目录级监控，覆盖原子替换 |
| v3.0 | 2026-03-19 | 锁定模式熔断、7版本baseline历史、SIGUSR1、SHA256校验、审计日志、自身完整性自检 |
