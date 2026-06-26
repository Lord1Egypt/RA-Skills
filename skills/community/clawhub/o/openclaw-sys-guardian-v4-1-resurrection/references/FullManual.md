# 🦞 openclaw-Sys Guardian V4.0 (Elastic Pulse Edition)

## 1. 全量系统架构设计 (Universal Architecture)
本系统是为 OpenClaw 构建的**闭环高可用 (High Availability)** 保护盾。它通过独立的“心跳探测-弹性响应-物理复活”三层结构，确保 Agent 在任何软件、配置或物理负载冲击下均能快速自愈。

---

## 2. 核心机制：弹性心跳 (Elastic Pulse)

### 2.1 指数退避算法 (Exponential Backoff) —— V4.0 核心更新
为了不给高负荷状态下的系统“雪上加霜”，V4.0 放弃了固定间隔探测，引入阶梯式冷却观察期：
- **故障 1 次**：冷却 60 秒。
- **故障 2 次**：冷却 180 秒（3 分钟）。
- **故障 3 次**：冷却 300 秒（5 分钟）。
- **故障 4 次**：冷却 600 秒（10 分钟）。
- **收益**：有效避开瞬时网络抖动或突发 CPU 峰值，给予宿主系统物理上的喘息空间。

### 2.2 多级分层自愈体系
1.  **L1 - 进程级修复**：强杀占用端口的僵尸进程 -> 执行 `gateway restart --force`。
2.  **L1.5 - 系统清创**：修复成功后自动追加 `sessions cleanup`，排除冗余任务。
3.  **L2 - 配置级回滚**：重启失败则从 `Vault 保险库` 恢复凌晨 4:00 的纯净配置镜像。
4.  **L3 - 物理级涅槃 (Resurrection)**：全链路失效时，触发交互式脚本，执行**内核重装协议**。

---

## 3. 风险预估与漏洞防范 (Neutral Risk Assessment)

| 风险项 | 潜在冲突 | V4.0 化解对策 |
| :--- | :--- | :--- |
| **无限循环自愈** | 若代码 Bug 导致回滚也失败。 | **硬断电逻辑**：V4.0 在 L2 失败后会立即主动退出进程，并锁定 `EXIT 1`，绝不重复垃圾操作。 |
| **看板指标风暴** | 频繁上报导致的飞书 API 熔断。 | **增量上报原则**：仅记录“心跳异常”或“重大延迟波动”。 |
| **权限死锁** | 加载 LaunchAgent 时权限过高无法修改。 | **用户域锁定**：所有脚本存放在 `~/` 用户根目录下，无需 sudo 即可维护。 |

---

## 4. 管理员实操手册 (Admin Cheat Sheet)

| 指令 | 目标 | 执行路径 |
| :--- | :--- | :--- |
| **物理重装** | 彻底崩溃时的一键涅槃 | `~/openclaw-backups-vault/scripts/lobster-resurrect.sh` |
| **一键熔断** | 彻底卸载所有监控 | `~/.openclaw/workspace/scripts/lobster-terminate.sh` |
| **强制快照** | 即刻备份当前灵魂 | `~/openclaw-backups-vault/scripts/lobster-snapshot.sh` |

---
*编撰：龙虾指挥官 (Lobster Commander)*
*版本日期：2026-03-03 (Updated v4.0)*
*状态：全量闭环上线 | 监测延迟：Active*
