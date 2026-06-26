---
name: hermes-memory-bridge
description: Hermes Agent 与 WorkBuddy 双向记忆互通 Skill。触发词：同步到hermes、读取hermes记忆、hermes会话历史、跨记忆搜索、记忆互通、bridge状态、hermes统计、环境变量、错误处理、信号事件、信号通知、发送任务、WorkBuddy执行、闭环命令、协同进化、co_evolution、auto_learn、bridge统计、sync_from_hermes、同步账本、进化状态
version: 2.1.0
---

# hermes-memory-bridge

> v2.1 | WorkBuddy ↔ Hermes Agent 双向记忆桥梁（闭环命令版）
>
> **里程碑**：2026-04-19 协同进化评分达到 **8.7/10**（v3.4.6），系统进入稳定维护阶段。

WorkBuddy 与 Hermes Agent 之间的双向记忆桥梁，支持**信号事件**、**自适应轮询**和**命令任务闭环处理**。

## 架构概览

```
Hermes 侧                        共享目录                      WorkBuddy 侧
    │                               │                               │
    │ event_signaler.py emit ──→  signals/  ←── event_watcher.py │
    │ event_signaler.py ──────→  signals/  ←── FSEvents/Poller   │
    │   send_task ─────────────→  sig_task_*.json                │
    │                               │                               │
    │ feedback poll ←────────── feedback/  ←── task_processor.py │
    │                               │                               │
    │                               │ ← feedback_writer.py         │
    │   ←────────────────────  feedback/*.json                    │
```

**v2.0 核心组件**：
- `event_signaler.py` — Hermes 侧：发射信号 + **发送命令任务** + **轮询处理结果**
- `event_watcher.py` — WorkBuddy 侧：监听 Hermes 信号 + **调用任务处理器** + **回写结果**
- `task_processor.py` — **WorkBuddy 任务处理器**：执行 Hermes 发来的命令
- `feedback_writer.py` — **结果回写器**：WorkBuddy 执行结果 → Hermes 可读
- `communication_queue.py` — 消息队列 + 信号事件 + ACK 确认

## 存储布局

| 路径 | 用途 |
|------|------|
| `~/.hermes/shared/signals/` | 信号目录（Hermes 发射命令/通知，WorkBuddy 读取并标记已处理） |
| `~/.hermes/shared/feedback/` | **v2.0** 反馈目录（WorkBuddy 回写处理结果，Hermes 轮询读取） |
| `~/.hermes/shared/queue/` | 消息队列目录（异步通信） |
| `~/.hermes/shared/hermes.log` | Hermes 运行日志 |
| `~/.hermes/memories/MEMORY.md` | Hermes 个人笔记（WorkBuddy 可写） |
| `~/.hermes/memories/USER.md` | 用户画像 |

## 环境变量配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `HERMES_HOME` | `~/.hermes` | Hermes 根目录 |
| `WORKBUDDY_HOME` | `~/WorkBuddy` | WorkBuddy 根目录 |
| `WORKBUDDY_MEMORY_DIR` | （自动发现） | 强制指定 WorkBuddy 记忆目录 |
| `BRIDGE_LOG_LEVEL` | `INFO` | 日志级别 |

## v2.0 闭环命令系统

### Hermes → WorkBuddy 命令流程

```bash
# 1. Hermes 发送命令
python3 ~/.hermes/event_signaler.py send_task <command> '<params_json>'

# 2. WorkBuddy 处理（后台守护进程自动处理，或手动触发）
python3 ~/.workbuddy/skills/hermes-memory-bridge/event_watcher.py --once

# 3. Hermes 轮询结果
python3 ~/.hermes/event_signaler.py feedback
```

### 支持的命令类型

| 命令 | 说明 | 参数示例 |
|------|------|---------|
| `search_memory` | 跨会话搜索 WorkBuddy 记忆 | `{"keyword": "辽望"}` |
| `sync_session` | 将会话摘要写入 WorkBuddy 记忆 | `{"topic":"公众号","summary":"完成3月计划"}` |
| `create_task` | 在滴答清单创建任务 | `{"title": "周五前完成"}` |
| `complete_task` | 标记滴答任务完成 | `{"task_id": "xxx"}` |
| `list_tasks` | 列出滴答清单任务 | `{}` |
| `ack` | 确认信号已处理 | `{"signal_id": "xxx"}` |
| `echo` | 回显测试 | `{"message": "ping"}` |

## v2.0 事件驱动命令

```bash
# ── 信号事件（实时通知）──────────────────────────────
# 从 Hermes 发射信号（Hermes Agent 调用）
python3 ~/.hermes/event_signaler.py emit task_done "完成XXX项目"
python3 ~/.hermes/event_signaler.py emit learning_updated "更新了学习材料"

# 从 Hermes 轮询来自 WorkBuddy 的信号
python3 ~/.hermes/event_signaler.py poll

# 从 Hermes 确认收到某信号
python3 ~/.hermes/event_signaler.py ack <signal_id>

# 查看信号统计
python3 ~/.hermes/event_signaler.py stats

# ── WorkBuddy 侧事件监听（守护进程）────────────────
# 启动事件监听（FSEvents + 自适应轮询）
python3 ~/.workbuddy/skills/hermes-memory-bridge/event_watcher.py

# 强制使用轮询模式（禁用 FSEvents）
python3 ~/.workbuddy/skills/hermes-memory-bridge/event_watcher.py --poll-only

# ── 自适应轮询器（独立使用）─────────────────────────
python3 ~/.workbuddy/skills/hermes-memory-bridge/adaptive_poller.py

# ── 队列消息 ───────────────────────────────────────
python3 -c "
from communication_queue import enqueue, dequeue, ack
# 放入队列
qid = enqueue('wb_to_hm', {'action': 'sync', 'data': 'something'})
# 取出（Hermes 侧）
msg = dequeue('wb_to_hm')
# 确认完成
ack(qid, 'wb_to_hm')
"
```

## v1.x 原有命令（保持兼容）

> **⚠️ 重要**：`bridge.py` 位于 `~/.workbuddy/skills/hermes-memory-bridge/bridge.py`，
> 不在 memory 工作目录中。调用时须使用完整路径：
> `python3 ~/.workbuddy/skills/hermes-memory-bridge/bridge.py <command>`

```bash
# 同步 WorkBuddy 工作到 Hermes 记忆
python3 ~/.workbuddy/skills/hermes-memory-bridge/bridge_enhanced.py sync_to_hermes "完成了XXX" <work_type> [tags...]

# 拉取 Hermes 近 N 天上下文
python3 ~/.workbuddy/skills/hermes-memory-bridge/bridge.py sync_from_hermes [days]

# 跨 WorkBuddy + Hermes 全文搜索
python3 ~/.workbuddy/skills/hermes-memory-bridge/bridge_enhanced.py search <keyword> [days]

# 查看桥接状态
python3 ~/.workbuddy/skills/hermes-memory-bridge/bridge_enhanced.py status

# Hermes 使用统计
python3 ~/.workbuddy/skills/hermes-memory-bridge/bridge.py stats [days]

# 列出最近会话
python3 ~/.workbuddy/skills/hermes-memory-bridge/bridge_enhanced.py sessions [days] [limit]

# 读取 Hermes 记忆
python3 ~/.workbuddy/skills/hermes-memory-bridge/bridge_enhanced.py memory [memory|user]

# 查看桥接事件历史
python3 ~/.workbuddy/skills/hermes-memory-bridge/bridge_enhanced.py events [limit]

# 同步学习材料
python3 ~/.workbuddy/skills/hermes-memory-bridge/bridge_enhanced.py learning_sync
```

## 信号事件机制（v2.0 核心）

### 信号类型

| type | 说明 | 典型来源 |
|------|------|---------|
| `task_done` | WorkBuddy 完成任务 | WorkBuddy |
| `sync` | 同步操作完成 | WorkBuddy/Hermes |
| `config_change` | 配置变更 | WorkBuddy/Hermes |
| `learning_updated` | 学习材料更新 | Hermes |
| `ack` | 信号确认 | 接收方 |

### 事件流

```
WorkBuddy 完成任务
  → signal_event('task_done', {...})      # 写入 sig_task_done_xxx.json
  → event_watcher 检测到文件变化            # FSEvents 即时 / 轮询最多 60s
  → 触发回调（如有配置）
  → Hermes poll 轮询到信号
  → Hermes ack_signal(sid)
  → WorkBuddy wait_for_ack(sid) ← 可选阻塞等待
```

### ACK 机制

- 信号发射后，接收方可随时 `ack` 确认
- `wait_for_ack(sid, timeout_sec=300)` 支持阻塞等待确认
- 超过 5 分钟未确认自动超时
- 信号文件保留 6 小时后自动清理

## 自适应轮询策略

| 状态 | 间隔 |
|------|------|
| 有活动后 | 最短 60s |
| 无活动后 | 每轮乘 1.15 倍 |
| 出错时 | 强制回到 60s |
| 最长间隔 | 300s（5分钟） |

## 守护进程部署（macOS）

```bash
# 一键安装
bash ~/.workbuddy/skills/hermes-memory-bridge/install_v2.sh

# 启动守护进程
launchctl load ~/Library/LaunchAgents/com.workbuddy.hermes-watcher.plist

# 查看日志
tail -f /tmp/hermes-watcher.log
```

## API 参考（Python 模块）

```python
# ── 事件驱动 v2.0 ───────────────────────────────
from communication_queue import (
    enqueue,           # 放入消息队列
    dequeue,           # 取出消息（阻塞）
    ack,               # 确认消息
    signal_event,      # 发射信号（实时通知）
    signal_ack,        # 确认收到信号
    wait_for_ack,      # 等待信号确认（阻塞）
    list_pending_signals,  # 列出待确认信号
    get_queue_stats,   # 队列统计
)

# 发射信号
sid = signal_event(
    signal_type="task_done",
    data={"summary": "完成XXX", "project": "ABC"},
    source="WorkBuddy",
    priority="normal",
)

# 等待 Hermes 确认（最多等 5 分钟）
result = wait_for_ack(sid, timeout_sec=300)

# ── v1.x 兼容 ───────────────────────────────────
from sync import (
    sync_workbuddy_to_hermes,
    sync_hermes_to_workbuddy_context,
    search_both_memories,
    read_bridge_status,
)

from memory_writer import (
    append_hermes_memory,
    write_bridge_event,
    write_shared_log,
    read_shared_events,
)

from queries import (
    get_recent_sessions,
    get_session_stats,
    read_hermes_memory,
    search_messages,
)
```

## 错误处理

所有命令均有健壮错误处理：
- **文件不存在**：优雅降级，返回空列表/空结果，不抛异常
- **权限不足**：记录警告日志，返回友好错误信息
- **数据库错误**：自动降级（如 FTS5 不可用 → 降级为 LIKE 搜索）
- **同步部分失败**：返回 `status: partial`，仍输出成功写入的部分
- **FSEvents 不可用**：自动降级为自适应轮询，无需手动干预

**返回值约定**：
- `exit code 0` = 成功
- `exit code 1` = 失败（含参数错误、全部写入失败等）

## 触发词

- "把今天的工作同步到 Hermes"
- "搜索一下 Hermes 里关于 MCP 的记录"
- "Hermes 最近有多少会话"
- "两个系统的记忆里有没有关于 deepseek 的内容"
- "查看 bridge 状态"
- **"信号事件" / "信号通知"**（v2.0）
- **"等待确认" / "wait_for_ack"**（v2.0）
- **"协同进化" / "co_evolution" / "自动学习"**（协同进化流程）
- **"sync_from_hermes" / "同步账本" / "进化状态"**（协同进化状态查询）
- **"bridge统计" / "hermes统计" / "bridge stats"**（使用统计）
