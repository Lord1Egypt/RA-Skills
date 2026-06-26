# 🩺 OpenClaw Doctor

OpenClaw 系统健康检查工具 — 一键诊断系统状态，发现问题并给出修复建议。

## 功能

- ✅ **系统状态**：OpenClaw 版本、Node.js 版本、内存占用
- ✅ **配置检查**：openclaw.json、频道连接、模型配置
- ✅ **模型连通性**：主模型、Fallback 模型、API Key 状态
- ✅ **定时任务**：Cron 任务数量、状态、连续失败检测
- ✅ **记忆系统**：MEMORY.md、TOOLS.md、daily notes 状态
- ✅ **技能加载**：已安装技能数量、格式校验

## 输出示例

```
🩺 OpenClaw 健康检查报告

系统状态：✅ 正常
- 版本：2026.3.13
- Node.js：v22.22.1
- 运行平台：Windows 10 x64

配置：✅ 正常
- 频道：飞书 ✅
- 模型：4 个配置

定时任务：✅ 正常
- 总数：8 个
- 状态：全部启用

健康评分：92/100 🟢
```

## 安装

```bash
clawhub install openclaw-doctor
```

## 使用

AI 会自动在需要时调用此技能，或用户可手动说"检查系统状态"。

## 依赖

- Node.js
- OpenClaw Gateway

## License

MIT
