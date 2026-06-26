---
name: openclaw-ref
description: OpenClaw 配置、CLI、排错、模型管理完整参考手册。修改 openclaw.json、执行 CLI 命令、排查问题时必须查阅此 Skill。
metadata:
  openclaw:
    emoji: "📖"
---

# OpenClaw 参考手册 (Skill)

> Astral 助手的 OpenClaw 操作手册。所有配置、排错、CLI 操作必须参考此文档。

## 使用方法
1. 先读本文件定位目标文档
2. 用 `read` 读取对应文件获取详细信息
3. 配置修改前必须查阅 `core/config-fields.md` 确认字段路径和类型

## 文件索引

### core/ — 核心参考 (最常用)
| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `config-fields.md` | 扁平化字段速查表（路径→类型→默认值） | 修改 openclaw.json 时(最重要) |
| `config.md` | 完整配置示例+常见模式+遗漏字段补充 | 需要完整配置参考或示例时 |
| `cli.md` | 所有 CLI 命令速查表 | 需要执行 openclaw 命令时 |
| `models.md` | 模型管理、提供商配置、故障转移、扫描 | 添加/切换模型、配置提供商时 |
| `gateway.md` | 网关管理、网络、安全、认证、服务 | 网关配置、远程访问、多实例时 |
| `concepts.md` | 核心概念（会话、压缩、记忆、多Agent、系统提示） | 理解系统行为、调优时 |
| `nodes.md` | 节点管理（配对、Camera、Canvas、Screen、Exec） | 管理节点设备时 |

### channels/ — 渠道配置
| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `overview.md` | 渠道通用配置、路由、配对、群组行为 | 配置任何渠道时先读 |
| `telegram.md` | Telegram 完整配置(Bot/群组/反应/流式) | 配置 Telegram 时 |
| `discord.md` | Discord 完整配置(服务器/频道/权限) | 配置 Discord 时 |
| `whatsapp-signal.md` | WhatsApp + Signal 配置 | 配置 WhatsApp/Signal 时 |
| `others.md` | Slack/BlueBubbles/iMessage/GoogleChat/飞书/Mattermost/LINE/Matrix等 | 配置其他渠道时 |

### automation/ — 自动化
| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `cron.md` | 定时任务(创建/调度/投递/JSON模式) | 管理定时任务时 |
| `heartbeat.md` | 心跳系统(配置/提示/可见性) | 配置心跳时 |
| `hooks-webhooks.md` | Hooks + Webhooks + Gmail + 认证监控 + 投票 | 配置事件自动化时 |

### providers/ — 模型提供商
| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `overview.md` | 所有提供商配置(内置+自定义+认证+常见示例) | 添加/配置任何提供商时 |

### tools/ — 工具系统
| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `overview.md` | 工具策略、Exec、Browser、子Agent、Skills、插件 | 配置工具权限/行为时 |

### setup/ — 安装部署
| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `install.md` | 安装、更新、Docker、迁移、卸载、环境变量、目录结构 | 安装/更新/迁移/环境问题时 |

### troubleshooting/ — 排错指南
| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `general.md` | 通用排错(快速分类/常见问题/核选项) | 遇到问题时先读 |
| `channels-gateway-nodes.md` | 渠道+网关+节点问题排错表 | 特定组件问题时 |

### reference/ — 参考资料
| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `api-security.md` | HTTP API(OpenAI+OpenResponses+Tools) + 安全 + 沙箱 | 配置API/安全/沙箱时 |
| `workspace-templates-webui.md` | 工作区文件映射 + 模板 + Web UI | 创建/修改工作区或配置WebUI时 |

## 关键原则
- **配置前必查**: 修改 `openclaw.json` 前必须查阅 `config-fields.md`
- **严格验证**: OpenClaw 拒绝未知字段，配置错误导致网关无法启动
- **备份优先**: 修改配置前备份 `~/.openclaw/openclaw.json`
- **用 doctor 修复**: 配置问题先跑 `openclaw doctor --fix`
- **环境变量**: API Key 用 `${VAR_NAME}` 引用，不硬编码
- **查日志**: `openclaw logs --follow` 是最佳信号源

## 源文档覆盖
本知识库覆盖了源仓库 docs/zh-CN/ 下所有14个目录(308个文件/55000+行)的核心内容:
cli, concepts, gateway, channels, automation, providers, tools, install, nodes, platforms, web, reference, help, security
