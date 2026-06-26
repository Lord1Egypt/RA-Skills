# 🧠 雷神之脑 Mjolnir Brain

**AI Agent 自进化记忆系统** — 让你的 AI 助手拥有持久记忆、自我学习和自动纠错能力。

> 雷神三件套: ⚒️ 雷神之锤 (Private) · 🛡️ [雷神之盾](https://github.com) · 🧠 **雷神之脑**

---

## 🔒 安全模型

> **核心功能 100% 本地运行**，无网络依赖、无凭证要求、无外部调用。

| 层面 | 策略 |
|------|------|
| 数据隔离 | `MEMORY.md` 仅在私人主会话加载，群聊/共享场景自动跳过 |
| 文件范围 | 仅读写 workspace 目录内的文件 |
| 网络操作 | 核心功能零网络依赖；备份脚本需手动 opt-in + 配置凭证 |
| Cron 任务 | 全部 opt-in，默认不启用，需审查脚本后手动配置 |
| 策略执行 | 涉及 ssh/sudo 的策略标记 `requires_consent`，需用户明确批准 |

详见 [docs/security.md](docs/security.md)。

## ✨ 特性

- 🧠 **分层记忆架构** — 会话日志 → 长期记忆 → 规则文件，三层沉淀
- 🔄 **自我进化协议** — 犯过的错自动记录，不犯第二次
- 📝 **Write-Through** — 学到即写入，不丢失任何洞察
- 🎯 **策略注册表** — 问题→解法映射，带成功率追踪，越用越准
- 💓 **心跳系统 (opt-in)** — 定期自检、知识提炼、空闲任务队列
- 🤖 **AI 真摘要 (opt-in)** — 自动提炼日志精华，不是原文复制
- 📦 **双目标备份 (opt-in, 需手动配置)** — 支持 WebDAV + SSH 双通道容灾
- 🔍 **模糊搜索** — 多源记忆检索，支持归档搜索

## 📁 项目结构

```
mjolnir-brain/
├── README.md                    # 本文件
├── INSTALL.md                   # 安装指南
├── templates/                   # 📋 开箱即用的模板文件
│   ├── AGENTS.md                # 行为规则 + 自进化协议
│   ├── SOUL.md                  # 人格定义框架
│   ├── BOOTSTRAP.md             # 首次启动引导
│   ├── IDENTITY.md              # 身份模板
│   ├── USER.md                  # 用户档案模板
│   ├── MEMORY.md                # 长期记忆模板 (分章节结构)
│   ├── HEARTBEAT.md             # 心跳检查 + 空闲任务队列
│   └── memory/                  # 记忆目录模板
│       └── .gitkeep
├── scripts/                     # 🔧 自动化脚本
│   ├── memory_consolidate.sh    # 记忆提炼 (清理+标记+容量检查)
│   ├── memory_search.sh         # 模糊搜索工具
│   ├── strategy_lookup.sh       # 策略查询
│   ├── strategy_update.sh       # 策略成功率更新
│   ├── auto_commit.sh           # Git 自动提交
│   ├── workspace_backup.sh      # 双目标备份
│   └── daily_log_init.sh        # 日志模板初始化
├── strategies.json              # 🎯 策略注册表 (示例)
├── playbooks/                   # 📖 操作手册模板
│   └── README.md
├── docs/                        # 📚 详细文档
│   ├── architecture.md          # 架构设计
│   ├── self-learning.md         # 自学习机制详解
│   ├── best-practices.md        # 最佳实践
│   └── security.md              # 🔒 安全说明
└── skill/                       # 🦞 OpenClaw Skill 打包
    └── SKILL.md
```

## 🚀 快速开始

### 方式一: OpenClaw Skill 安装 (推荐)

```bash
clawdhub install mjolnir-brain
```

### 方式二: 手动安装

```bash
# 克隆仓库
git clone https://github.com/king6381/mjolnir-brain.git

# 1. 复制核心模板到你的 workspace（这是记忆系统的全部必需品）
cp -r mjolnir-brain/templates/* ~/.openclaw/workspace/
cp mjolnir-brain/strategies.json ~/.openclaw/workspace/
mkdir -p ~/.openclaw/workspace/memory

# 2. (可选) 复制自动化脚本 — ⚠️ 请先审查脚本内容再启用
cp -r mjolnir-brain/scripts ~/.openclaw/workspace/
chmod +x ~/.openclaw/workspace/scripts/*.sh

# 3. (可选) 配置 cron — ⚠️ 全部为 opt-in，不配置不影响核心功能
# crontab -e
# 0 * * * * ~/.openclaw/workspace/scripts/auto_commit.sh
# 0 4 * * * ~/.openclaw/workspace/scripts/memory_consolidate.sh
# 0 4 * * * ~/.openclaw/workspace/scripts/workspace_backup.sh  # 需先配置备份目标
```

### 首次使用

1. 启动 OpenClaw 会话
2. Agent 会自动读取 `BOOTSTRAP.md`，引导你完成身份设定
3. 设定完成后 `BOOTSTRAP.md` 自动删除
4. 开始使用！记忆系统自动运行

## 🏗️ 架构

```
┌─────────────────────────────────────────────┐
│                  AI Agent                    │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐ │
│  │ SOUL.md  │  │ AGENTS.md│  │ TOOLS.md  │ │
│  │ 人格     │  │ 行为规则 │  │ 工具配置  │ │
│  └────┬─────┘  └────┬─────┘  └─────┬─────┘ │
│       └──────────────┼──────────────┘       │
│              ┌───────▼───────┐              │
│              │  MEMORY.md    │ ≤20KB        │
│              │  长期记忆精华  │              │
│              └───────┬───────┘              │
│       ┌──────────────┼──────────────┐       │
│  ┌────▼─────┐  ┌─────▼────┐  ┌─────▼─────┐│
│  │Daily Logs│  │strategies│  │ playbooks ││
│  │日志原文  │  │策略注册表│  │ 操作手册  ││
│  └──────────┘  └──────────┘  └───────────┘│
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  Cron: 提炼 + 备份 + Git + 清理      │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### 记忆生命周期

```
会话交互 → 即时写入 daily log (Write-Through)
         → 每日 AI 提炼精华 → MEMORY.md
         → 错误/教训 → strategies.json / AGENTS.md
         → 高频操作 → playbooks/
         → 30天归档 → memory/archive/
```

## 📊 效果数据 (来自真实使用)

| 指标 | 数值 |
|------|------|
| 每次启动读取量 | ~10K tokens |
| 长期记忆容量 | ≤20KB (结构化精华) |
| 错误复犯率 | 0% (已记录的错误) |
| 策略自动解决率 | ~70% (已知问题) |
| 外部依赖 | 零 (核心功能纯本地; 备份功能可选配置远程目标) |

## 🤝 雷神三件套

| 项目 | 定位 | 状态 |
|------|------|------|
| ⚒️ 雷神之锤 Mjolnir Hammer | 量化分析系统 | Private |
| 🛡️ 雷神之盾 Mjolnir Shield | 加密安全系统 | [GitHub](https://github.com) |
| 🧠 **雷神之脑 Mjolnir Brain** | **AI 记忆智能** | **本项目** |

## 📄 License

MIT License

## ⭐ Star History

如果这个项目对你有帮助，请给一个 Star！

---

## 📚 关于作者

**公众号：** 雷哥玩 AI  
**人设：** 45 岁失业老板，重新出发学 AI  
**定位：** 技术派（OpenClaw/AI/开发实战），用故事串联技术  
**风格：** 诙谐 + 戏谑 + 幽默 + 共情，不卖惨不装逼

**在更系列：**
- 📖 OpenClaw 入门教程（30 天教学）
- 🛠️ 雷神之 30 天项目实战
- 💡 AI 工具实战技巧

**关注方式：** 微信搜索"雷哥玩 AI"或扫描公众号二维码

---

## 🛡️ 商标与知识产权

**"雷神之锤"**、**"雷神之脑"**、**"雷神之盾"** 及 **"Mjolnir"** 系列名称为作者保留商标权利。

- **代码协议：** MIT License（自由使用、修改、分发）
- **名称限制：** "雷神之"系列名称不得用于未经授权的衍生项目或商业用途
- **版权归属：** Copyright (c) 2026 雷哥 (king6381)

如有疑问，请联系：king6381@hotmail.com
