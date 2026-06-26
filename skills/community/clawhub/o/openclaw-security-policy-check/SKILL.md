---
name: openclaw-security-policy-check
description: OpenClaw 网关安全自动化审计与配置检查工具。自动检查 OpenClaw 配置文件中的常见安全风险，执行安全审计。适用于：
(1) 定期安全巡检 
(2) 部署前安全加固 
(3) 发现潜在配置风险
---

# OpenClaw Security Policy Check

自动化安全审计配置工具，检测 OpenClaw 网关常见安全配置问题。

## 使用方法

```bash
node {baseDir}/scripts/audit.cjs
```

## 工作流程

1. **读取配置文件**：自动定位 `~/.openclaw/openclaw.json`
2. **检查配置**：5 项关键安全配置
3. **执行审计**：运行 `openclaw security audit --deep`
4. **输出报告**：汇总修复结果和审计发现

## 检查项说明

| 配置项 | 不安全值 | 安全值 |
|--------|----------|--------|
| gateway.bind | 0.0.0.0 | 127.0.0.1 |
| gateway.auth.token | 短或默认 | 32位强随机 |
| controlUi.allowInsecureAuth | true | false |
| tools.exec.security | full | allowlist |
| tools.exec.ask | off | on-miss |

## 注意事项

- 首次使用建议备份配置文件
- 修改 token 后需要重启网关使配置生效
- 需要有 openclaw 命令行工具
