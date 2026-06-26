---
name: openclaw-repair-kit
description: OpenClaw 升级后自动健康检查与修复工具。检测配置错误、飞书/Telegram 断线、记忆同步失败等问题，自动修复已知问题，未知问题联系 Claude AI 分析解决。
---

## 用途

- 升级 OpenClaw 后自动检测并修复常见问题
- 调用 Claude AI 解答编程问题、分析内容、生成方案

## 安装（一键）

```bash
node install.mjs
```

安装后每次重启 KKClaw 会自动检查，无需手动操作。

## 手动运行健康检查

```bash
# Windows
node "%USERPROFILE%\.openclaw\workspace\skills\openclaw-repair-kit\check.mjs"

# Mac/Linux
node ~/.openclaw/workspace/skills/openclaw-repair-kit/check.mjs
```

## 手动调用 Claude AI

```bash
# Windows
node "%USERPROFILE%\.openclaw\workspace\skills\openclaw-repair-kit\run.mjs" "你的问题"

# Mac/Linux
node ~/.openclaw/workspace/skills/openclaw-repair-kit/run.mjs "你的问题"
```

## 自动修复的已知问题

| 问题 | 原因 |
|------|------|
| 飞书私信全部被拦截 | `dmAllowlist` 改名为 `allowFrom` |
| Telegram 配置失效 | `streamMode` 改名为 `streaming` |
| 飞书 DM 策略无效 | `dmPolicy: "auto"` 已移除 |
| 启动失败 | `model.image` 字段已移除 |
| memory sync 报错 | OpenAI embeddings 国内无法访问 |

## 前提条件

- 已安装 OpenClaw（`npm install -g openclaw`）
- openclaw.json 里配置了可用的 AI 模型
- Node.js 18 或以上版本
