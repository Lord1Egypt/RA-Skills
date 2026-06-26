# 🦞 龙虾守护者 (Lobster-Guardian) 灾备系统设计方案

## 1. 设计目标
为 **OpenClaw (龙虾指挥官)** 建立一套生产级的离线状态监测、配置自动归位与故障自愈机制，解决由于任务过载、模型断连或代码变动导致的服务挂起问题。

## 2. 核心架构 (双重自愈环)
*   **L1 (软修复 - 心跳检测)**: 
    - 间隔: 30 分钟 (正常态) / 1 分钟 (重试态)。
    - 逻辑: 通过 `openclaw gateway health` 探测 API。若失败，重试 3 次，依然失败则执行 `openclaw gateway restart`。
*   **L2 (硬重置 - 配置回滚)**:
    - 场景: 软修复无效或配置文件损坏 (config syntax error)。
    - 逻辑: 从最近的原子快照目录 (`~/.openclaw/backups/daily/`) 恢复 `openclaw.json` 与 `auth-profiles.json`，执行强力冷启动。

## 3. 风险化解机制 (Robustness Safeguards)
| 风险点 | 化解措施 |
| :--- | :--- |
| **循环重启** | 设定“故障冷冻期”：15 分钟内连续失败 3 次重启，则停止自动操作，通过飞书拉响红色预警。 |
| **配置污染** | **原子写策略**: 所有备份与恢复均通过 `tmp` 中转并校验 MD5，确保不会出现半截损坏的配置。 |
| **脑裂冲突** | 重启前强制执行端口占用清理 (`lsof -ti:18789 | xargs kill -9`)。 |
| **备份回退循环** | 循环保留 7 天快照，支持逐级向前追溯恢复。 |

## 4. 实施阶段 (Implementation Phases)
### 第一阶段：自动化快照 (Snapshot)
- **任务**: 编写并部署 `lobster-snapshot.sh`。
- **目标**: 每日 4:00 AM 执行全量 `~/.openclaw` 核心文件备份至 `backups/` 目录。
- **文件检查点**: `openclaw.json`, `auth-profiles.json`, `workspace/` 核心配置。

### 第二阶段：守护进程部署 (Guardian)
- **任务**: 编写 `lobster-guardian.sh` 并注册为 `macOS LaunchAgent`。
- **目标**: 实现常驻内存监控，并对接飞书消息推送接口。

### 第三阶段：破坏性压力测试 (Stress Test)
- **场景**: 模拟 PID 消失、配置乱码、端口僵死。
- **验证**: 确保符合 TC-01 至 TC-05 测试用例预期。

## 6. 双保险：强制熔断机制 (The Terminator)
为防止监控程序在某些极端情况下干扰大规模调试或系统升级，设计了“龙虾终结者”一键熔断脚本。

### 6.1 熔断逻辑
- **原子卸载**: 从 `launchctl` 彻底注销守护服务。
- **进程截杀**: 强制杀死内存中的 `lobster-guardian` 脚本及子进程。
- **缓存排空**: 删除所有 `.log` 运行日志及临时诊断序列。

### 6.2 一键清理指令
指令路径：`~/.openclaw/workspace/scripts/lobster-terminate.sh`
```bash
/Users/maxleolee/.openclaw/workspace/scripts/lobster-terminate.sh
```

## 5. 任务与代谢逻辑优化 (Metabolic Updates)
*   **Session 清理策略更新 (2026-03-05)**: 
    - **修改原因**: 频繁的无差别 Session 清理可能导致活跃任务中断或状态丢失。
    - **更新逻辑**: 移除维护模式下的 `openclaw sessions cleanup --enforce` 指令。
    - **新策略**: 仅清理“超长时间不活跃（>48小时）”或“由异常中断产生的僵尸 Session”。指令对齐为 `openclaw sessions cleanup --inactive-hours 48 --clean-zombies`。

---
*文档更新日期: 2026-03-05*  
*由 龙虾指挥官 (Agent: main) 自动生成并归档。*
