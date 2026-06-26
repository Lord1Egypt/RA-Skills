# OpenClaw 配置守护 - 使用说明

## 1. 安装与启用

### 1.1 检查依赖

```bash
# inotify-tools（监控文件事件）
apt-get update && apt-get install -y inotify-tools

# jq（状态文件读写，可选，脚本内置 fallback）
apt-get install -y jq
```

### 1.2 启用守护

```bash
# 1. 复制脚本（已自动完成）
#    脚本位置：/usr/local/bin/openclaw-config-guardian
#    systemd 服务：/etc/systemd/system/openclaw-config-guardian.service

# 2. 重载 systemd
systemctl daemon-reload

# 3. 启用并启动
systemctl enable --now openclaw-config-guardian

# 4. 检查状态
systemctl status openclaw-config-guardian
```

### 1.3 初始化备份目录

守护启动会自动创建：
```
/root/.openclaw/backups/config/
├── baseline.bak              （首次启动时从当前配置生成）
├── baseline.bak.sha256       （baseline 完整性校验，v3+）
├── baseline_history/         （最近 7 个有效 baseline，v3+）
├── attempts/                 （变更快照，保留最近 20 个）
├── .guardian_state.json      （状态文件：attempts/locked/failed_at）
├── .guardian_checksum        （guardian 脚本自身 SHA256，v3+）
└── guardian_audit.log        （结构化审计日志，v3+）
```

---

## 2. 日常使用

### 2.1 修改配置

**任何方式都可以**：

```bash
# 方式1：openclaw config set（推荐）
openclaw config set agents.defaults.sandbox.mode all

# 方式2：直接编辑
vim /root/.openclaw/openclaw.json

# 方式3：复制替换
cp new-config.json /root/.openclaw/openclaw.json
```

守护会自动：
1. 创建快照到 `attempts/`
2. 验证配置
3. 若成功 → 更新 `baseline.bak`，日志记录
4. 若失败 → 回滚到 `baseline.bak`，记录错误，计数+1

### 2.2 查看状态

```bash
# 查看守护状态
systemctl status openclaw-config-guardian

# 查看实时日志
journalctl -u openclaw-config-guardian -f

# 查看守护状态文件（JSON）
cat /root/.openclaw/backups/config/.guardian_state.json
```

### 2.3 查看备份

```bash
# 最新基线（有效版本）
ls -lh /root/.openclaw/backups/config/baseline.bak

# 所有变更快照（按时间倒序）
ls -lht /root/.openclaw/backups/config/attempts/

# 对比某次失败的修改
diff -u baseline.bak attempts/openclaw.json.2026-03-12-09-50-22.bak
```

---

## 3. 失败处理

### 3.1 单次失败

守护会自动回滚，日志会显示：
```
❌ 配置无效，已回滚到 baseline。
错误：agents.defaults.sandbox.mode: invalid value
尝试次数：1/3
```

**操作**：
- 检查错误描述，修正配置
- 重新修改（守护会继续处理）

### 3.2 连续 3 次失败 → 锁定模式（v3+ 行为）

守护**不停止**，进入锁定模式，日志：
```
⛔ reached max failures (3); entering LOCK MODE (monitoring continues)
```
同时向 Discord #报告 + TG 双发告警。

锁定模式行为：
- 监控继续运行
- 任何写入 openclaw.json 的操作都会被自动回滚到 baseline
- 不再尝试验证，直到人工解锁

**解锁流程**（v3.2+ 专用解锁命令）：
1. 通过官方通道修复配置：
   ```bash
   openclaw config.patch ...
   # 或直接编辑后确保配置有效
   ```
2. 执行解锁命令（内置 validate，通过才解锁）：
   ```bash
   openclaw-config-guardian unlock
   ```
   - 若配置仍无效：打印错误，拒绝解锁，需继续修复
   - 若配置有效：自动清除 locked 状态、更新 baseline、发 SIGUSR1 给 gateway
3. 确认解锁成功：
   ```bash
   jq '.locked' /root/.openclaw/backups/config/.guardian_state.json
   # 应输出 false
   systemctl status openclaw-config-guardian
   ```

**注意**：锁定状态持久化在磁盘（`.guardian_state.json`），guardian 崩溃重启后锁定依然有效。

---

## 4. 维护操作

### 4.1 临时禁用守护

```bash
systemctl stop openclaw-config-guardian
# 修改配置后手动重启
```

### 4.2 清理旧快照

```bash
# 脚本自动保留最近 20 个，手动清理更多
find /root/.openclaw/backups/config/attempts -type f -mtime +30 -delete
```

### 4.3 重置状态

若 `attempts` 计数需要重置（锁定已解除后正常重启即可）：

```bash
# 重启守护（验证成功后自动重置 attempts=0）
systemctl restart openclaw-config-guardian
```

**解除锁定请使用专用命令**（不要手改 state.json）：

```bash
openclaw-config-guardian unlock
```

### 4.4 强制恢复基线

```bash
cp /root/.openclaw/backups/config/baseline.bak /root/.openclaw/openclaw.json
# v3+ 已自动 SIGUSR1 热重载，无需手动 gateway restart
# 如需完整重启：openclaw gateway restart
```

---

## 5. 告警配置

告警通过 `openclaw message send` 内置实现，无需额外配置环境变量。熔断触发时自动向 Discord `#报告` 频道 + Telegram 双发告警。

---

## 6. 注意事项

1. **基线必须有效**：守护启动时如果 `openclaw.json` 已无效，`baseline.bak` 也会无效，后续回滚无意义。请在启动前先确保配置正确。
2. **Gateway 自动热重载**：v3+ 回滚/验证通过后会自动发 SIGUSR1 给 gateway 触发热重载，无需手动重启。若需完整重启仍可执行 `openclaw gateway restart`。
3. **监控单一文件**：仅 `openclaw.json`，其他配置变更（如技能配置）不受保护。
4. **权限要求**：守护以 root 运行，确保 `openclaw` 命令在 root PATH 中。

---

## 7. 故障排除

| 问题 | 可能原因 | 解决 |
|------|---------|------|
| 守护无法启动 | inotifywait 未安装 | `apt install inotify-tools` |
| 修改后无响应 | 监控路径错误 | 检查 `CONFIG_FILE` 变量 |
| 回滚失败 | baseline.bak 不存在 | 手动复制一个有效版本到 `backups/config/baseline.bak` |
| 日志不输出 | journald 未运行 | `systemctl status systemd-journald` |

---

文档版本：v3.0  
最后更新：2026-03-19（大黑 #F_SEC，对齐 guardian v3.2）
