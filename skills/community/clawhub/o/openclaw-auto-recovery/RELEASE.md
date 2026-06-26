# openclaw-auto-recovery Release Notes

## Version 1.0.7 — 2026-04-07

### 修复：CPU 检测改用 vmstat（彻底解决 locale 问题）

**问题描述**

`top -bn1 | awk 'NR==3 {print $4}'` 在不同 Linux 发行版和 locale 下，`top` 第 3 行的列位置不固定，导致 `$4` 在某些中文环境下拿到的是错误的字段名，算出的 CPU 使用率是乱值。

**修复方案**

改用 `vmstat 1 1`，其列输出格式固定为英文，`NR==3` 的第 15 列（idle）始终可靠：

```bash
# 修复后（不依赖 top 列位置）
check_cpu() {
    vmstat 1 1 | awk 'NR==3 {printf "%.1f\n", 100-$15}'
}
```

**关于飞书错误码 99992361**

这是飞书消息接口的**频率限制**错误（QPS 限流），非代码 bug。可能原因：
- 短时间内有多条告警同时触发（如 CPU + 内存 + 磁盘同时超阈值）
- 重启恢复通知等连续告警
- 建议检查 alert 发送频率是否集中在短时间窗口内

---

## Version 1.0.6 — 2026-04-07

### 修复：中文 locale 兼容性问题

**问题描述**

在非英文 locale 环境下（如中文 Linux），`free` 命令输出第一列为 `内存:` 而非 `Mem:`，`top` 命令的 CPU 行标签也可能被翻译。导致：

- `check_memory`：调用 `free | grep Mem` 匹配失败，命令返回空，在 `set -euo pipefail` 下脚本直接退出
- `check_cpu`：调用 `top -bn1 | grep "Cpu(s)"` 在某些中文环境下标签不一致，同样导致 grep 失败

**修复内容**

- `check_memory`：改用 `free | awk 'NR==2 {printf "%.0f\n", $3/$2 * 100}'`，不依赖英文标签
- `check_cpu`：改用 `top -bn1 | awk 'NR==3 {printf "%.1f\n", 100-$4}'`，`$4` 是 idle 值，100减去得到实际 CPU 使用率，不依赖 `Cpu(s)` 等英文标签

---

## Version 1.0.2 — 2026-04-07

### 核心修复：回滚逻辑缺陷（Critical Fix）

**问题描述**

在 v1.0.1 及之前版本中，当 Gateway DOWN 且重启失败时，回滚逻辑存在致命缺陷：

```
Gateway DOWN → backup_config() 保存当前（坏）配置为 abc
             → restart 失败
             → rollback_config() → ls -t 取最新 → 命中最新的 abc（还是那份坏配置）
             → 回滚到坏配置，无任何意义
```

核心问题：触发备份和回滚使用的是**同一套文件命名规则**，`ls -t` 取到的"最新备份"就是刚保存的那份坏文件。

**修复方案：last-good 锚点机制**

引入独立的健康配置锚点文件，与普通备份完全隔离：

- **只在 Gateway UP 时保存**：每次检测到 Gateway 在线，才更新 `openclaw.json.last-good.{1,2,3}`
- **MD5 去重**：配置内容未变化时不重复保存，避免锚点被坏配置覆盖
- **回滚只读锚点**：`rollback_config()` / `rollback_one()` 只回滚到 `last-good.N`，不用 `ls -t` 动态查找

### 新增功能

#### 1. 多版本回滚（最多 3 个版本）

重启失败后，不再只尝试一份配置，而是依次尝试：

```
last-good.1 → restart → check
    ↓ DOWN     last-good.2 → restart → check
    ↓ DOWN     last-good.3 → restart → check
    ↓ DOWN     → 失败计数+1，告警"需人工介入"
```

每次尝试都是完整的"覆盖配置 → 重启 → sleep 60 → 验证 UP/DOWN"循环。

#### 2. `rollback_one()` — JSON 无效专用

当 `validate_json()` 发现配置文件格式已损坏（JSON 语法错误），调用 `rollback_one()`：

- 行为：只回滚配置，**不回滚、不重启**
- 原因：JSON 格式错误时首要目标是换掉坏文件，重启让后续流程统一处理
- 分工明确：`rollback_one()` 专注 JSON 损坏场景，`rollback_config()` 专注重启失败场景

#### 3. 启动时健康锚点保存

心跳守护进程启动时，若 Gateway 已在线，立即保存 `last-good.1`，确保服务重启后锚点可用。

#### 4. MD5 去重保存

`save_last_good()` 在保存前对比 MD5，配置内容无变化时跳过保存，保持锚点队列有真正的历史版本。

### 其他改进

- `heartbeat-daemon.sh` 脚本结构重组：函数定义更清晰，注释更完善
- 所有示例 App ID 改为占位符（`cli_xxxxxxxxxxxxxxxxxxxxxxxxxxxx`），避免隐私泄露

---

## Version 1.0.1 — 2026-04-06

- 将安装脚本和配置文档中的示例 App ID 替换为占位符，防止真实凭证随 skill 扩散

---

## Version 1.0.0 — 2026-04-04

- 初始发布
- 功能：Gateway WebSocket 检测 + 自动重启（最多 3 次连续失败）
- 主机监控：磁盘 / 内存 / CPU / 进程，超阈值飞书告警
- 配置备份回滚：基于 `ls -t` 的简单备份策略
- systemd 托管进程保活
