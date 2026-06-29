<p align="center">
  <img src="https://img.shields.io/badge/version-1.4.89-blue" alt="Version" />
  <img src="https://img.shields.io/badge/license-Apache%202.0-green" alt="License" />
  <a href="https://github.com/CoderMoray/MyKnowledge"><img src="https://img.shields.io/badge/GitHub-CoderMoray-black?logo=github" alt="GitHub" /></a>
</p>

<h1 align="center">MyKnowledge</h1>

<p align="center">一个通用的 AI 知识库管理 Skill<br/>让 AI 助手帮你自动整理知识、跟踪需求、记录进度</p>

---

## 📖 5 分钟上手指南

| 我想... | 看这里 |
|---------|--------|
| 快速安装 | → [🛒 商店支持](#-商店支持) |
| 了解能做什么/不能做什么 | → [✨ 核心特性](#-核心特性) + [⚠️ 能力边界](#️-能力边界) |
| 学会常用命令 | → [QUICKSTART.md](QUICKSTART.md) |
| 遇到问题 | → [FAQ.md](FAQ.md) 或 [docs/PITFALLS.md](docs/PITFALLS.md) |
| 深入了解 / 进阶技巧 | → [USAGE.md](USAGE.md) 或 [💡 高手技巧](#-高手技巧) |
| 查看隐私声明 | → [PRIVACY.md](PRIVACY.md) |

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 📁 **标准化知识库** | 一键创建目录结构（全局 / 项目级别） |
| 📋 **需求生命周期** | 创建 → 进行中 → 审核 → 完成 → 归档 |
| 🤖 **智能智能任务追踪** | 检测复杂任务，自动创建记录（可选） |
| 💬 **会话自动记录** | 对话内容自动追加到对应需求文档 |
| 🔀 **多平台支持** | CodeBuddy / WorkBuddy / OpenClaw / Claude |

---

## ⚠️ 能力边界（本 Skill 不做什么）

为了让你用得放心，这里**明确**说清楚本 Skill 的边界：

| 不做的事 | 原因 / 替代方案 |
|----------|----------------|
| ❌ 联网 / 云端同步 | 本地文件管理；需要同步请用 git |
| ❌ 多用户实时协作 | 单机文件；团队请用 Notion / Confluence |
| ❌ 富文本 / 所见即所得编辑 | Markdown 优先；需要 WYSIWYG 请用 Typora |
| ❌ 自动备份到云端 | 手动 cp -r 或 git commit 即可 |
| ❌ 自动修改 `~/.myknowledge/` 之外的文件 | 严格沙箱，保护你的数据（导出功能需显式授权） |
| ❌ 执行任意 shell 命令 | 不在 Skill 职责内，避免误操作 |
| ❌ 跨平台配置同步 | 每个平台独立安装（轻量级） |

**如果你需要以上能力**——本 Skill 不是合适工具，请选择专业产品。

---

## 📊 版本演进对比

> 每个版本都在持续优化性能、增强功能、提升用户体验。

| 指标 | 1.0.0 | 1.1.x | 1.2.x | 1.3.x | 1.4.x | 变化趋势 |
|------|--------|--------|--------|--------|--------|----------|
| **架构设计** | 全量预加载 | 懒加载架构 | 责任分层 | 自动化验证 | 安全增强 | ✅ 持续优化 |
| **上下文占用** | ~15K tokens | ~12K | ~9K | ~7K | **~5K** | 🔻 -67% |
| **平台支持** | 3 个 | 3 个 | 4 个 | 4 个 | **4 个** | ✅ Claude 新增 |
| **错误处理** | 分散描述 | 表格化 | 兜底机制 | 自助修复 | **友好提示** | ✅ 持续增强 |
| **自动化验证** | 无 | 无 | lint 门禁 | CI/CD | **GitHub Actions** | ✅ 完整覆盖 |
| **核心功能** | 基础 CRUD | +命令速查 | +项目追踪 | +UX 优化 | **+导出分享** | ✅ 功能完善 |
| **用户体验** | 基础 | +能力边界 | +首次引导 | +触发优化 | **+隐私增强** | ✅ 持续打磨 |

### 各版本亮点

- **v1.1.x**：懒加载架构、错误处理表格化、命令速查、能力边界明确
- **v1.2.x**：项目追踪、全局子目录化、lint 门禁、首次引导强制化
- **v1.3.x**：UX 优化 7 项、需求优先级与标签、projects.yaml 原子化
- **v1.4.x**：一键导出/分享、安全与隐私增强、错误提示友好化、审计报告修复

> 💡 **性能说明**：基于 Prompt 行数和 Token 占用估算，实际效果因模型而异。
> 数据来源：每版发布时的实际测量结果。

---

## 🛒 商店支持

MyKnowledge 已在多个 AI Skill 商店上架，你可以根据自己的 AI 助手选择合适的安装方式：

| 商店 | 状态 | 安装方式 | 适用场景 |
|------|------|----------|----------|
| **SkillHub** | ✅ 已上架 | 见下方安装说明 | CodeBuddy / WorkBuddy 用户 |
| **agentskill.sh** | ✅ 已上架 | [浏览目录](https://agentskill.sh/@codermoray/myknowledge) | 需要安全扫描报告的用户 |
| **skills.sh** | ✅ 已支持 | `npx skills add CoderMoray/MyKnowledge` | 使用 30+ AI 工具的用户（Claude Code、Cursor 等） |
| **ClawHub** | ✅ 已上架 | `clawhub install CoderMoray/MyKnowledge` | OpenClaw 用户 |
| **GitHub** | ✅ 开源 | `git clone https://github.com/CoderMoray/MyKnowledge.git` | 开发者 / 自行部署 |

### SkillHub 安装说明

**首次安装 SkillHub 商店**：
1. 检查是否已安装 SkillHub 商店：`skillhub --version`
2. 若未安装，请根据 https://skillhub.cn/install/skillhub.md 安装 SkillHub 商店（只安装 CLI）
3. 安装 MyKnowledge：`skillhub install my-knowledge`

**已安装 SkillHub 商店**：
- 直接安装 MyKnowledge：`skillhub install my-knowledge`

**更新 MyKnowledge**：
- 重新执行安装命令即可覆盖为新版，用户数据不会丢失

---

## 📚 完整使用示例

> **目标**：从安装到完成第一个需求，跟着做一遍就会了。

### 场景：开发一个新功能

#### 步骤 1：首次使用（创建知识库）

```
用户：创建知识库

AI：👋 欢迎使用 MyKnowledge！
    这是你第一次使用，我需要了解一些信息：
    
    1. 你用的是哪个 AI 助手？
       [CodeBuddy] [WorkBuddy] [OpenClaw] [Claude]
    
    2. 要自动记录对话吗？
       [是，自动记录] [否，手动记录]
    
    ...（引导流程）...
    
    已创建全局知识库：~/.myknowledge/global/我的项目/
```

#### 步骤 2：创建第一个需求

```
用户：我需要开发一个用户登录功能

AI：✅ 已创建需求：REQ-20260614-001 用户登录功能
    位置：~/.myknowledge/global/我的项目/requirements/REQ-20260614-001/
    
    包含文件：
    - README.md（需求描述）
    - DESIGN.md（设计文档）
    - TASKS.md（任务清单）
```

#### 步骤 3：更新需求状态

```
用户：登录功能开发完成了

AI：✅ 需求 REQ-20260614-001 状态已更新：进行中 → 完成
    项目状态已同步：PROJECT-STATUS.md
```

#### 步骤 4：查看项目进展

```
用户：项目进展如何

AI：📊 项目状态快照
    
    总需求：3 个
    - ✅ 完成：2 个
    - 🔄 进行中：1 个
    - 📋 待开始：0 个
    
    最近更新：REQ-20260614-001 用户登录功能（2 小时前）
```

#### 步骤 5：导出分享

```
用户：导出知识库

AI：✅ 已导出：~/.myknowledge/exports/我的项目-20260614.zip
    
    分享方式：
    1. 直接发送 ZIP 文件给同事
    2. 同事说"导入知识库"，选择这个 ZIP 即可
```

---

### 常见场景速查

| 我想... | 怎么说 | 结果 |
|----------|---------|------|
| 开始新项目 | "创建知识库" | 初始化目录结构 |
| 记录新需求 | "创建需求：{描述}" | 创建需求文件夹 |
| 查看所有需求 | "查看需求列表" | 显示需求索引 |
| 更新需求状态 | "需求 REQ-XXX 完成了" | 更新状态为"完成" |
| 自动记录对话 | "以后都自动记录" | 设置 auto_record: true |
| 导出项目 | "导出知识库" | 生成 ZIP 文件 |
| 遇到问题 | "重新初始化" | 一键修复配置 |

---

```bash
# 国内用户推荐 Atomgit
git clone https://atomgit.com/CoderMoray/MyKnowledge.git ~/.codebuddy/skills/myknowledge/

# 或使用 GitHub
git clone https://github.com/CoderMoray/MyKnowledge.git ~/.codebuddy/skills/myknowledge/
```

> 其他平台替换路径：WorkBuddy → `~/.workbuddy/skills/myknowledge/`，OpenClaw → `~/.openclaw/skills/myknowledge/`，Claude → `~/.claude/plugins/myknowledge/`

---

### ✅ 安装后验证

```
创建知识库          → 自动创建到全局知识库
创建一个测试需求     → 应创建 REQ-YYYYMMDD-XXX 目录
查看项目状态        → 应显示 PROJECT-STATUS.md 内容
```

## 💡 使用场景

### 场景 1：主动使用

```
你：创建知识库
AI：我将为您创建知识库...（询问类型 → 生成结构）
```

### 场景 2：智能任务追踪（推荐）

```
你：帮我分析这个销售数据
AI：（检测到复杂任务）
   已自动创建知识库并记录需求 REQ-20260608-001
```

### 场景 3：项目状态追踪

```
你：项目进展如何？
AI：（读取 PROJECT-STATUS.md）
   当前有 3 个活跃需求：
   • REQ-001 数据分析 - 进行中
   • REQ-002 报告生成 - 待审核
   • REQ-003 文档整理 - 已完成
```

### 场景 4：导出/分享

```
你：导出项目「销售分析」
AI：📦 已导出 → ~/Downloads/myknowledge-export-销售分析.zip
   对方导入后即可恢复完整项目状态

你：导入知识库
AI：解压到全局知识库 → 同名项目提供覆盖/重命名/对比选项
```


## 🆕 版本更新

### [v1.4.83] - 2026-06-14 — 错误提示友好化

- 📝 **审计报告问题3修复**：改进错误提示友好度
- 📦 **导入 zip 无效**：说明有效包条件，提供解决方案
- 🔄 **状态流转无效**：列出所有合法流转
- 💬 **平台/安装源不识别**：提供友好的引导

### [v1.4.0] - 2026-06-12 — 一键导出/分享

- 📦 **导出知识库**：打包为 zip（含项目状态 + 安装引导），默认保存到下载文件夹
- 📥 **导入知识库**：支持同名项目冲突处理（覆盖/重命名/对比）
- 🌏 **Atomgit 国内镜像**：安装引导新增国内加速地址

### [v1.3.0] - 2026-06-11 — UX 优化 7 项

- 🎯 引导流程标注泄漏修复 + 欢迎语自动跳过 + 选项 1/2 简化
- 📁 知识库默认全局，不再每次询问类型
- 🔄 旧版跨源升级自动迁移

### [v1.2.0] - 2026-06-11 — 引导流程强制化

- 📋 **首次引导强制化**：首次使用必须完成引导流程
- 📁 **模板体系完善**：新增需求模板、项目状态模板
- 🔒 **职责边界明确**：区分用户数据和 Skill 文件

[查看完整变更日志 →](CHANGELOG.md)

## 📂 目录结构

```
MyKnowledge/
├── SKILL.md              # Skill 主入口（AI 执行指令）
├── settings.yaml         # Skill 配置
├── _meta.json            # Skill Hub 元数据
├── manifest.json         # 路径清单（用户级元数据，含免责声明）
├── core/                 # 核心功能
│   ├── main.md          # 主逻辑（懒加载入口，含加载时自检）
│   └── templates/       # 文档模板
├── modules/             # 可选模块（按需加载）
│   ├── commands/        # 命令速查（v1.1.1+）
│   ├── management/      # 需求管理
│   ├── error/           # 错误处理
│   └── auto-track/     # 智能任务追踪
├── one-time/            # 一次性配置
│   ├── onboarding/      # 首次引导
│   └── setup/           # 安装源/平台/更新检测
└── hooks/               # 平台 Hook
    ├── openclaw/        # OpenClaw
    └── claude/          # Claude

开发者专用（不进 SkillHub zip）：
├── scripts/             # build-skillhub.sh、lint-paths.sh
├── test/                # 测试套件
└── .github/             # CI 配置
```

## 💡 高手技巧

> 熟悉基础用法后，这些技巧能让你效率翻倍。

### 一键切换项目
```
cd ~/project-a && 对 AI 说"项目进展如何"  → 看项目A
cd ~/project-b && 对 AI 说"项目进展如何"  → 看项目B
```
知识库自动跟随当前目录，无需手动切换。

### 让 AI 帮你写周报
```
把本周完成的 3 个需求总结成周报要点
把过去一周 PROJECT-STATUS.md 的变更汇总成进展报告
```

### git 管理知识库
```bash
cd ~/.myknowledge
git init && git add . && git commit -m "初始化知识库"
# 记得 .gitignore 排除 config/ 目录（含平台特定配置）
```

### 自定义智能任务追踪
编辑 `settings.yaml`，调整检测灵敏度以匹配你的工作风格，添加常用任务关键词。

### 更多技巧
→ [USAGE.md 进阶使用](USAGE.md#进阶使用) | [FAQ.md 进阶使用](FAQ.md#进阶使用) | [PITFALLS 进阶使用](docs/PITFALLS.md#进阶使用)

---

## 🔗 相关资源

| 资源 | 链接 |
|------|------|
| 安装说明 | [INSTALL.md](INSTALL.md) |
| 快速上手 | [QUICKSTART.md](QUICKSTART.md) |
| 详细用法 | [USAGE.md](USAGE.md) |
| 常见问题 | [FAQ.md](FAQ.md) |
| 避坑指南 | [docs/PITFALLS.md](docs/PITFALLS.md) |
| 开发文档 | [DEVELOPMENT.md](DEVELOPMENT.md) |

## 📄 许可证

[Apache License 2.0](LICENSE)
