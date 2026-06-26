# OpenClaw 配置守护方案 - 设计文档

## 1. 背景与目标

### 问题
- 配置修改失误导致 Gateway 无法启动
- 缺乏自动回滚机制
- 多人操作时无法追溯
- 修改失败后不知道具体哪里出错

### 目标
- **被动监控**：任何方式修改 `openclaw.json` 都会被捕获
- **自动验证**：修改后立即调用 `openclaw config validate`
- **即时回滚**：验证失败自动恢复到上一个有效版本
- **错误反馈**：记录具体错误字段与原因
- **熔断机制**：连续 3 次失败后进入**锁定模式**（v3+），监控继续运行，任何写入自动回滚，同时向 Discord + TG 双发告警；不再停止守护
- **版本追溯**：保留每次修改的快照，便于人工审计

---

## 2. 架构设计

### 2.1 核心组件

```
┌─────────────────┐
│ inotifywait     │  监控文件系统事件
│ close_write,    │─────────────┐
│ moved_to        │             │
└─────────────────┘             │
                                ▼
┌─────────────────┐      ┌─────────────────┐
│ 守护主进程      │───→ │ 创建快照         │
│ openclaw-       │      │ attempts/xxx.bak│
│ config-guardian │      └─────────────────┘
└─────────────────┘             │
                                │
                                ▼
                    ┌─────────────────┐
                    │ 验证配置        │
                    │ openclaw config │
                    │ validate        │
                    └─────────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
                ✅ 成功                   ❌ 失败
                    │                       │
                    ▼                       ▼
           更新 baseline.bak          回滚 baseline.bak
           SIGUSR1 → gateway           attempts++
                                        │
                                        ▼
                                attempts >= 3 ?
                                        │
                                ┌───────┴───────┐
                                ▼               ▼
                        write locked=true    继续监控
                        双端告警              重置计数

注：handle_change() 入口先 is_locked()（读磁盘）
    locked=true → do_revert()+SIGUSR1 → return（不走 validate）
```

### 2.2 备份目录结构

```
/root/.openclaw/backups/config/
├── baseline.bak                    # 最新有效版本（回滚源）
├── attempts/
│   ├── openclaw.json.2026-03-12-09-50-22.bak  # 每次变更快照
│   └── openclaw.json.2026-03-12-09-52-11.bak
└── .guardian_state.json           # 守护状态（attempts、错误、锁定）
```

**关键点**：
- `baseline.bak` 永远代表「上一个验证通过版本」，只在验证成功后更新
- `attempts/` 保留所有被验证的修改快照（含成功与失败），保留最近 20 个
- `.guardian_state.json` 记录连续失败次数与锁定状态

---

## 3. 详细流程

### 3.1 守护启动

```bash
# 1. 确保目录存在
mkdir -p /root/.openclaw/backups/config/attempts

# 2. 如果 baseline.bak 不存在，复制当前 openclaw.json 作为基线
if [[ ! -f baseline.bak ]]; then
  cp openclaw.json baseline.bak
fi

# 3. 初始化状态文件（attempts=0）
echo '{"attempts":0,"last_error":null,"last_backup":null,"locked":false}' > .guardian_state.json

# 4. 启动 inotifywait 监控（目录级，覆盖原子替换）
inotifywait -m -e close_write,moved_to --format '%e %f' /root/.openclaw/ |
while read -r evt fname; do
  [[ "$fname" == "openclaw.json" ]] && handle_change
done
```

### 3.2 处理变更事件（v3.2 真状态机）

```bash
handle_change() {
  # 0. 入口先读磁盘 locked 状态（每次都读，不信任内存）
  if is_locked; then
    # 锁定模式：直接 revert，绝不进入 validate
    do_revert "locked_mode"
    reload_gateway  # SIGUSR1 热重载
    return 0
  fi

  # 1. 创建本次变更快照（事后追溯）
  snap=$(snapshot)

  # 2. 验证配置
  if validate_config; then
    # ✅ 成功：更新 baseline + 归档历史 + SIGUSR1
    after_success "$snap"
  else
    # ❌ 失败：回滚到 baseline + SIGUSR1 + attempts++
    after_failure "$snap" "validate_failed"
    # 达到 MAX_RETRIES → write_state locked=true + 双端告警
  fi
}
```

---

## 4. 错误反馈机制

### 4.1 日志输出

所有操作写入 systemd journal：

```bash
journalctl -u openclaw-config-guardian -f
```

示例：
```
Mar 12 09:50:22 guardian[1234]: 🔄 检测到配置变更
Mar 12 09:50:22 guardian[1234]: ❌ 验证失败：agents.defaults.sandbox.mode: invalid value
Mar 12 09:50:22 guardian[1234]: 🔄 已回滚到 baseline.bak
Mar 12 09:50:22 guardian[1234]: 🔢 尝试次数: 1/3
```

### 4.2 状态文件

`/root/.openclaw/backups/config/.guardian_state.json` 实时记录：

```json
{
  "attempts": 1,
  "last_error": "agents.defaults.sandbox.mode: invalid value",
  "last_backup": "/root/.openclaw/backups/config/attempts/openclaw.json.2026-03-12-09-50-22.bak",
  "locked": false,
  "failed_at": null
}
```

### 4.3 双端告警（内置）

熔断触发时通过 `openclaw message send` 自动向 Discord `#报告` + Telegram 双发告警，无需额外配置。

---

## 5. 恢复与调试

### 5.1 手动恢复

```bash
# 恢复 baseline（v3+ 自动 SIGUSR1 热重载，guardian 检测到变更后自动同步 gateway）
cp /root/.openclaw/backups/config/baseline.bak /root/.openclaw/openclaw.json
# 如需完整重启（补救选项）：
# openclaw gateway restart
```

### 5.2 查看历史尝试

```bash
ls -lht /root/.openclaw/backups/config/attempts/
# 找到失败当天的快照，用 diff 对比
diff -u baseline.bak attempts/openclaw.json.2026-03-12-09-50-22.bak
```

### 5.3 重启守护

```bash
# 修复配置后（确保 baseline.bak 有效）
systemctl start openclaw-config-guardian
# 或重启
systemctl restart openclaw-config-guardian
```

---

## 6. 注意事项

1. **权限**：守护以 root 运行，确保能读写 `/root/.openclaw/`
2. **基线依赖**：`baseline.bak` 必须存在且有效，否则回滚失败
3. **监控范围**：仅监控 `openclaw.json`，不监控其他配置文件（如 `plugins/` 独立文件）
4. **inotify 限制**：极端高频写入可能丢事件，但配置修改频率低，无影响
5. **Gateway 热重载**：v3+ 验证通过/回滚后自动发 SIGUSR1 给 gateway 触发热重载，无需人工干预。

---

## 7. 扩展建议

- 结合 Git：守护前/后自动 `git add/commit`，提供完整版本历史
- 多文件监控：扩展监控 `plugins/*.json`、`agents/*.json` 等
- Webhook 通知：失败时调用外部 API（如 Slack、Discord）
- 自动 Gateway 重启：回滚成功后自动 `openclaw gateway restart`（需评估风险）

---

文档版本：v3.2  
最后更新：2026-03-19（大黑 #F_SEC，对齐 guardian v3.2）

## 8. v3 / v3.1 加固变更摘要

| 优先级 | 项目 | 版本 | 状态 |
|---|---|---|---|
| P0 | 熔断后锁定模式（不停监控）+ 双端告警 | v3 | ✅ |
| P0 | inotifywait MOVED_TO 覆盖原子替换 | v2已有 | ✅ |
| P0 | 锁定态回滚后补发 SIGUSR1 | v3.1 | ✅ |
| P1 | 验证/回滚后 SIGUSR1 触发 Gateway 重载 | v3 | ✅ |
| P1 | 多版本 baseline 历史（保留7个）| v3 | ✅ |
| P1 | 去掉 create 事件，只保留 close_write,moved_to | v3.1 | ✅ |
| P2 | baseline.bak SHA256 校验保护 | v3 | ✅ |
| P2 | 结构化审计日志 | v3 | ✅ |
| P3 | guardian 自身 SHA256 完整性自检（fail-closed）| v3.1 | ✅ |

## 10. v3.2 真状态机锁定修复

| 变更 | v3.1 | v3.2 |
|---|---|---|
| 锁定检测 | 进程内布尔变量（已废弃）| 每次从磁盘读 `locked` 字段 |
| 锁定持久性 | 进程重启后失效 | 持久化磁盘，重启后仍有效 |
| 锁定路径逻辑 | 进入 after_failure 内部判断 | handle_change() 入口提前 return |
| 解锁方式 | 手动改 state.json | `openclaw-config-guardian unlock`（内置 validate）|

### handle_change() 流程（v3.2）

```
handle_change()
  │
  ├─ is_locked()? ──读磁盘──► locked=true
  │    │
  │    └─► do_revert() + reload_gateway() → return  ← 绝不进入 validate
  │
  └─ locked=false
       │
       ├─ snapshot()
       ├─ validate_config()
       │    ├─ OK  → after_success()
       │    └─ FAIL → after_failure() → do_revert() → [达到MAX_RETRIES → write locked=true]
       └─ (监控继续)
```

### 解锁命令

```bash
openclaw-config-guardian unlock
# 1. 执行 validate_config()
# 2. 通过 → write_state locked=false, attempts=0 → update_baseline → reload_gateway
# 3. 不通过 → 打印原因，exit 1，拒绝解锁
```

## 9. v3.1 闭环修复详情

### 9.1 锁定态自解锁 bug（高风险，已修复 v3.2）

**问题**：锁定态执行 `cp baseline -> openclaw.json` 会再次触发 inotify，下一轮 handle_change() 验证通过后 after_success() 将 locked 重置为 false，锁定自动解除。

**v3.2 终版修法（方案 A：真状态机）**：
- `handle_change()` 入口第一件事调用 `is_locked()`，**每次从磁盘读取** `.guardian_state.json` 中的 `locked` 字段
- `locked=true` 时：直接执行 `do_revert()` + `reload_gateway()`，**绝不进入 validate / after_success 流程**，直接 return
- 锁定状态完全持久化于磁盘，guardian 崩溃重启后仍然有效

### 9.2 锁定态回滚后补 SIGUSR1

锁定态 auto-revert 完成后增加 `reload_gateway` 调用，确保 gateway 内存与磁盘配置同步。

### 9.3 去掉 create 事件

inotifywait 从 `close_write,moved_to,create` 改为 `close_write,moved_to`，减少不必要的触发面（create 事件在新文件创建时触发，与 openclaw.json 覆盖场景无关，且可能引发额外的误触发）。

### 9.4 self-check 改为 fail-closed

checksum 文件缺失时不再静默跳过，改为拒绝启动并发告警。任何环境部署必须先生成 checksum 才能运行 guardian。
