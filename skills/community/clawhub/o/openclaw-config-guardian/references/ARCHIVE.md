# 方案归档索引

## 项目：OpenClaw 配置守护（Config Guardian）

**归档日期**：2026-03-12（最后更新：2026-03-19）
**当前版本**：v3.1
**作者**：小七（OpenClaw 主控）/ 大黑 #F_SEC（加固实施）
**目标用户**：系统管理员、OpenClaw 运维人员

---

## 文件清单

| 文件 | 路径 | 说明 |
|------|------|------|
| `DESIGN.md` | `common_assets/Library/config-guardian/DESIGN.md` | 原理与架构设计 |
| `USAGE.md` | `common_assets/Library/config-guardian/USAGE.md` | 使用说明（安装、日常操作）|
| `OPERATION.md` | `common_assets/Library/config-guardian/OPERATION.md` | 运行维护与故障排除 |
| 本文件 | `common_assets/Library/config-guardian/ARCHIVE.md` | 归档索引 |

---

## 关联文件（已部署）

| 类型 | 路径 | 说明 |
|------|------|------|
| 守护脚本 | `/usr/local/bin/openclaw-config-guardian` | 主程序 v3.1，可执行 |
| systemd 服务 | `/etc/systemd/system/openclaw-config-guardian.service` | 系统服务单元 |
| 状态文件 | `/root/.openclaw/backups/config/.guardian_state.json` | 运行时状态（自动生成）|
| 基线备份 | `/root/.openclaw/backups/config/baseline.bak` | 最新有效配置（自动更新）|
| 基线校验 | `/root/.openclaw/backups/config/baseline.bak.sha256` | baseline SHA256（v3+）|
| 历史基线 | `/root/.openclaw/backups/config/baseline_history/` | 最近 7 个有效版本（v3+）|
| 快照目录 | `/root/.openclaw/backups/config/attempts/` | 历史变更快照（最近 20 个）|
| 审计日志 | `/root/.openclaw/backups/config/guardian_audit.log` | 结构化审计日志（v3+）|
| 自检 checksum | `/root/.openclaw/backups/config/.guardian_checksum` | guardian 脚本 SHA256（v3+）|
| 加固方案 | `common_assets/Protocols/CONFIG_GUARDIAN_HARDENING_V1.md` | 加固设计文档 |

---

## 部署状态

- [x] 脚本已写入 `/usr/local/bin/`
- [x] systemd 服务已写入 `/etc/systemd/system/`
- [x] 服务已 enable 并 active (running)
- [x] 文档已写入 `common_assets/Library/config-guardian/`
- [x] guardian v3.1 加固全部实施完成

---

## 版本历史

| 版本 | 日期 | 说明 | 操作人 |
|------|------|------|--------|
| v1.0 | 2026-03-12 | 初始版本，单文件监控、验证、回滚、3次限制后停止 | 小七 |
| v2.0 | 2026-03-12 | 目录级监控，覆盖原子替换（close_write,moved_to,create）| 大黑 |
| v3.0 | 2026-03-19 | 锁定模式熔断、7版本baseline历史、SIGUSR1、SHA256、审计日志、自身完整性 | 大黑 |
| v3.1 | 2026-03-19 | 修复锁定态自解锁bug、补SIGUSR1、去掉create事件、self-check fail-closed | 大黑 |

---

## 备注

- 本方案仅保护 `openclaw.json`，不覆盖技能安装、文件删除等其他操作。
- 更新 guardian 脚本后必须刷新 checksum，否则 fail-closed 自检拒绝启动。
- 建议结合 Git 做更完整的版本控制。

---

**归档完成** ✅
