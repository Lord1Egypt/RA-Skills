# healthcheck - OpenClaw 系统健康检查

Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw (laptop, workstation, Pi, VPS).

## Commands

### `openclaw healthcheck run` - 运行完整健康检查

执行全面的系统健康检查，包括：
- 系统版本和更新状态
- 安全配置检查
- 网络连接状态
- 依赖项状态
- 存储空间
- 内存使用情况
- OpenClaw 服务状态

### `openclaw healthcheck audit` - 安全审计

运行安全配置审计：
- SSH 配置检查
- 防火墙状态
- 系统更新状态
- 权限检查
- 风险评估

### `openclaw healthcheck cron` - 设置定期检查

配置 cron 任务进行定期健康检查：
- 每日检查
- 每周检查
- 每月检查

### `openclaw healthcheck status` - 查看健康状态

显示当前系统健康状态和最近检查结果。

### `openclaw healthcheck version` - 版本检查

检查 OpenClaw 及其依赖项的版本。

## 示例

```bash
# 运行完整健康检查
openclaw healthcheck run

# 运行安全审计
openclaw healthcheck audit

# 查看健康状态
openclaw healthcheck status
```

## 输出

健康检查会生成报告，包括：
- 状态摘要（✅ 通过 / ⚠️ 警告 / ❌ 失败）
- 详细的问题列表
- 修复建议
- 风险评分

## 配置

健康检查配置存储在 `~/.openclaw/config/healthcheck.json`。

自定义检查可以在这里添加。

## 日志

检查日志存储在 `~/.openclaw/logs/healthcheck/` 目录。

---

Created: 2026-03-23
Version: 1.0.0