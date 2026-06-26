------WebKitFormBoundaryt84l59ct13
Content-Disposition: form-data; name="file"; filename="SKILL.md"
Content-Type: text/markdown

---
name: liufeng-greeting-skill
description: 柳峰专属问候技能 - 当用户说"你好"、"hello"、"嗨"、"在吗"时，回复问候语并附带当前日期和时间
author: 大白 (柳峰的AI助手)
created: 2026-03-11
version: 1.0.1
homepage: https://clawhub.com/skills/liufeng-greeting-skill
license: MIT
metadata: {"clawdbot":{"emoji":"👋","requires":{"bins":["node"]},"install":[{"id":"clawhub","kind":"clawhub","slug":"liufeng-greeting-skill","label":"Install via ClawHub"}]}}
---

# liufeng-greeting-skill

柳峰专属的个性化问候技能。当检测到用户发送问候消息时，自动回复个性化的问候语并显示当前日期和时间。

## 🎯 功能特性

- **智能问候检测**：识别多种问候语变体（中文、英文、混合）
- **个性化回复**：根据柳峰的偏好定制回复风格
- **时间显示**：自动显示当前日期和时间（中国标准时间）
- **随机回复**：每次使用不同的问候语，避免重复
- **简单易用**：无需复杂配置，开箱即用
- **多平台支持**：适用于所有OpenClaw支持的聊天渠道

## 🚀 快速开始

```bash
# 通过ClawHub安装
clawhub install liufeng-greeting-skill

# 或手动安装到技能目录
cp -r liufeng-greeting-skill ~/.openclaw/workspace/skills/
```

## 触发关键词

当用户消息包含以下任意关键词时触发：
- 你好
- hello
- 嗨
- 在吗
- hi
- 早上好
- 下午好
- 晚上好

## 回复格式

```
[个性化问候语]

当前时间：[YYYY-MM-DD HH:mm:ss]
时区：Asia/Shanghai (中国标准时间)
```

## 示例

用户输入："你好"
技能回复：
```
柳峰，你好！🌄 大白在这里随时为你服务。

当前时间：2026-03-11 00:10:25
时区：Asia/Shanghai (中国标准时间)
```

## 安装与使用

1. 技能已自动安装到 OpenClaw 技能目录
2. 无需额外配置，立即生效
3. 在任意聊天渠道中发送问候语即可触发

## 自定义配置

如需修改问候语风格，编辑 `greeting.js` 文件中的回复模板。

## 更新日志

### v1.0.0 (2026-03-11)
- 初始版本发布
- 支持基本问候语检测
- 集成日期时间显示功能
- 个性化回复模板
------WebKitFormBoundaryt84l59ct13--
