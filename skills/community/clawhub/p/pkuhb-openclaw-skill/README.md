# 🦞 OpenClaw使用入门指南

> 基于北京大学肖睿团队《OpenClaw001：龙虾使用入门》课件

## 什么是OpenClaw？

OpenClaw是一个**自托管的本地优先AI助手平台**，代表第五代AI（自主Agent平民化时代）的到来。

## 快速开始

### 1. 部署环境

```bash
# macOS
brew install openclaw
openclaw setup

# Windows (WSL)
wsl --install
npm install -g openclaw
openclaw setup

# Docker
docker pull openclaw/core
docker-compose up -d
```

### 2. 配置工作区

```bash
openclaw configure
# 或
openclaw setup
```

### 3. 核心文件

| 文件 | 必须 | 说明 |
|------|------|------|
| `SOUL.md` | ✅ | Agent人格定义 |
| `USER.md` | ✅ | 用户画像 |
| `MEMORY.md` | 建议 | 长期记忆 |

## 常用命令

```bash
openclaw --version          # 检查版本
openclaw configure          # 配置向导
openclaw setup              # 初始化工作区
openclaw gateway restart     # 重启网关
openclaw skills list        # 列出Skills
openclaw skills install <id> # 安装Skill
```

## 安装Skills

```bash
# 命令行安装
openclaw skills install <skill-id>

# 手动安装
# 1. 创建目录: skills/<name>/
# 2. 放入SKILL.md
# 3. openclaw gateway restart
```

## 安全建议

1. 🔒 开启Dashboard认证
2. 📁 最小化目录挂载
3. 🛡️ 设置Shell白名单
4. 🔄 定期更新与审计

## 模型推荐

| 场景 | 推荐模型 |
|------|----------|
| 日常主力 | Step 3.5 Flash / M2.5 Flash |
| 复杂规划 | Claude Opus 4.6 |
| 深度研究 | Kimi K2.5 |
| 视觉任务 | Qwen视觉版 |

## 相关链接

- 🌐 [OpenClaw官网](https://openclaw.ai)
- 🛒 [ClawHub市场](https://clawhub.ai)
- 🐟 [OpenClawmp](https://openclawmp.stepfun.com)

---

*本指南基于北京大学2026年课件整理*
