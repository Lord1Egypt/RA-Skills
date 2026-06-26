# 📚 OpenClaw 官方文档查询 - OpenClaw 技能

指导 AI 如何访问和查询 OpenClaw 官方文档 (https://docs.openclaw.ai/)，获取准确、权威的产品信息。

## ✨ 核心功能

- **🎯 精准查询** - 访问官方文档获取准确信息
- **📖 来源追溯** - 提供文档链接和引用位置
- **✅ 信息验证** - 确保答案可验证、可追溯
- **📋 结构输出** - 清晰的查询结果格式

## 🚀 快速开始

### 安装

```powershell
# 复制到 OpenClaw 技能目录
xcopy /E /I openclaw-docs %USERPROFILE%\.openclaw\skills\openclaw-docs

# 重启 Gateway
openclaw restart
```

### 使用

直接询问 OpenClaw 相关问题：

- "OpenClaw 支持哪些聊天平台？"
- "如何配置 Gateway？"
- "技能怎么开发？"
- "如何排查连接问题？"

## 📁 目录结构

```
openclaw-docs/
├── SKILL.md      # 技能定义
├── CLAUDE.md      # 核心执行指令（五要素框架）
├── README.md     # 本文件
└── EXAMPLES.md   # 使用示例
```

## 🎯 五要素框架

本技能严格遵循五要素设计：

| 要素 | 说明 |
|-----|------|
| **WHEN** | 用户询问 OpenClaw 功能、配置、使用方法时触发 |
| **WHAT** | 输出基于官方文档的准确答案，附带来源引用 |
| **HOW** | 识别意图 → 访问文档 → 提取信息 → 结构输出 |
| **REFERENCE** | 必须访问文档验证，不得凭记忆回答 |
| **LIMITS** | 必须提供文档链接，必须标注信息时效性 |

## 💬 使用示例

**你问：** "如何配置 OpenClaw Gateway？"

**AI 回答：**
```
📋 查询结果

## 核心答案
OpenClaw Gateway 配置通过 `config.yaml` 文件完成。

## 操作步骤
1. 定位配置文件：`~/.openclaw/gateway/config.yaml`
2. 修改配置参数
3. 重启服务：`openclaw restart`

## 📖 来源引用
- 文档链接：https://docs.openclaw.ai/configuration/gateway
- 章节位置：Configuration → Gateway Setup

## ⚠️ 注意事项
- 修改配置后必须重启服务
- 配置文件使用 YAML 格式
```

## 🔗 常用文档链接

| 文档类型 | URL |
|---------|-----|
| 主页 | https://docs.openclaw.ai/ |
| 快速开始 | https://docs.openclaw.ai/getting-started |
| Gateway 配置 | https://docs.openclaw.ai/configuration/gateway |
| 技能开发 | https://docs.openclaw.ai/skills |
| API 参考 | https://docs.openclaw.ai/api |
| 故障排查 | https://docs.openclaw.ai/troubleshooting |

## ⚠️ 重要限制

- ✅ 必须访问官方文档验证信息
- ✅ 必须提供可点击的文档链接
- ✅ 必须标注信息的时效性
- ❌ 不得凭记忆或推测回答技术问题
- ❌ 不得使用模糊不可操作的表述

---

**新技能已创建成功！** 🎉

📝 注意：
- 本技能需要网络访问能力
- 查询结果以官方文档为准
- 建议定期更新文档知识
