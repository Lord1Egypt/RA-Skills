# MEMORY.md 自动管理 Skill

🧠 自动创建和维护 OpenClaw 长期记忆文件，让 AI 助手拥有持续的记忆能力！

---

## ⚠️ 安全警告

**请使用 v1.0.10 或更高版本！**

- ❌ v1.0.0 - v1.0.9: 可能包含不安全的占位符
- ✅ v1.0.10+: 已修复安全问题
- ✅ **v1.0.14+ (推荐)**: 最新安全版本

```bash
# 检查版本
clawhub info memory-manager-zx

# 更新到最新版本
clawhub install memory-manager-zx@latest
```

---

## 📦 安装

```bash
# 本地安装
cd ~/.openclaw/workspace/skills
# 复制此目录到 memory-manager
```

---

## 🚀 快速开始

### 一键安装

```bash
cd ~/.openclaw/workspace/skills/memory-manager
./install.sh
```

### 手动配置

```bash
# 1. 创建 MEMORY.md 模板
openclaw memory init

# 2. 配置每日更新任务 (每天午夜 00:00)
openclaw cron add --name "MEMORY 每日更新" \
  --schedule "0 0 * * *" \
  --message "检查当天会话，更新 MEMORY.md"
```

---

## 📋 功能

### 运行时依赖

| 工具 | 用途 | 是否必需 |
|------|------|----------|
| `bash` | 脚本执行 | ✅ 必需 |
| `curl` | HTTP 请求（智能筛选） | ✅ 必需 |
| `jq` | JSON 解析 | ✅ 必需 |
| `python3` | API 调用和 JSON 处理 | ✅ 必需 |
| `openclaw` CLI | cron 任务配置 | ⚠️ 可选（用于自动配置） |

### 1. 自动创建 MEMORY.md

提供标准化的长期记忆模板：

```markdown
# MEMORY.md - [助手名称] 的长期记忆

## 👤 关于用户
## 🏠 系统环境
## ⚙️ 核心配置
## 📅 重要事件
## 📌 待办事项
```

### 2. 每日自动更新（智能筛选）

通过 cron 任务在每天午夜自动：
- 检查当天会话历史 (`memory/YYYY-MM-DD.md`)
- **规则预过滤** - 使用 30+ 关键词模式快速匹配
- **LLM 分析** - 调用 Qwen 模型提炼重要事件
- **脱敏检测** - 自动识别 Token/Secret 等敏感信息
- 更新 MEMORY.md 的「重要事件记录」

### 3. 手动整理记忆

⚠️ **重要**: 自动更新不会智能筛选内容，建议定期手动整理：
- 阅读 `memory/YYYY-MM-DD.md` 每日日志
- 手动提炼重要事件到 MEMORY.md
- 可使用 `openclaw cron` 配置定期提醒整理

---

## ⚙️ 配置选项

### 🔌 API 配置（可选）

**智能筛选会自动读取 OpenClaw 配置！**

#### 工作原理

```bash
1. 读取 ~/.openclaw/openclaw.json
2. 找到第一个配置的 provider（有 baseUrl）
3. 自动提取 API 地址和默认模型
4. 根据 provider 名称匹配对应的 API Key 环境变量
```

#### 配置 API Key

只需配置一个环境变量，Skill 会自动匹配：

```bash
# 添加到 ~/.bashrc（推荐）
# 根据你的服务商选择：

# 阿里云百炼 (modelstudio)
export BAILIAN_API_KEY="your-api-key-here"

# DeepSeek / vLLM
export DEEPSEEK_API_KEY="xxx"

# OpenAI
export OPENAI_API_KEY="your-api-key-here"

# 通用备用
export OPENCLAW_API_KEY="xxx"
```

#### 支持的服务商

| provider 名称 | 匹配的环境变量（按优先级） |
|--------------|--------------------------|
| `modelstudio` | `BAILIAN_API_KEY` → `ALIYUN_API_KEY` → `DASHSCOPE_API_KEY` |
| `vllm` | `VLLM_API_KEY` → `DEEPSEEK_API_KEY` |
| `openai` | `OPENAI_API_KEY` |
| `deepseek` | `DEEPSEEK_API_KEY` |
| `anthropic` | `ANTHROPIC_API_KEY` |
| `google` | `GOOGLE_API_KEY` → `GEMINI_API_KEY` |
| `azure` | `AZURE_OPENAI_API_KEY` |
| 其他 | `OPENCLAW_API_KEY` → `API_KEY` |

#### 查看当前配置

```bash
# 查看 OpenClaw 配置的 provider
cat ~/.openclaw/openclaw.json | jq '.models.providers'

# 查看默认模型
cat ~/.openclaw/openclaw.json | jq '.agents.defaults.model.primary'
```

#### 降级模式

如果未配置 API Key，自动切换到**规则匹配模式**（免费，无需 API）。

⚠️ **安全与隐私说明**：

**脚本会做什么：**
- ✅ 读取 `~/.openclaw/openclaw.json` 获取 API 地址 (baseUrl) 和 provider 名称
- ✅ 从环境变量读取 API Key（如 `BAILIAN_API_KEY`）
- ✅ 向 LLM 提供商 API 发送请求（用于智能筛选）
- ✅ 在日志中显示 API Key 的部分内容（如 `sk-sp-be...dc57`）

**脚本不会做什么：**
- ❌ 不会读取 `openclaw.json` 中的 API Key 字段
- ❌ 不会将 API Key 写入任何文件
- ❌ 不会将 API Key 发送到非提供商地址
- ❌ 不会上传会话内容到 Skill 作者的服务器

**配置建议：**
```bash
# 只在你信任的 LLM 提供商处配置 API Key
export BAILIAN_API_KEY="your-api-key-here"  # 阿里云
export DEEPSEEK_API_KEY="xxx"    # DeepSeek
export OPENAI_API_KEY="your-api-key-here"   # OpenAI

# 不配置 Key 时，自动使用规则模式（无需网络）
```

**降级模式：** 如果 API 不可用（欠费/网络问题），自动切换到规则匹配模式。

### cron 调度

```bash
# 每天午夜更新
0 0 * * *

# 每 6 小时更新 (更频繁)
0 */6 * * *

# 每周一上午 9 点周总结
0 9 * * 1
```

### 内容筛选规则

**混合模式筛选流程：**

```规则预过滤 → LLM 分析 → 脱敏检测 → 更新 MEMORY.md```

| 类型 | 记录 | 说明 |
|------|------|------|
| 配置变更 | ✅ | TTS 切换、模型配置、频道设置等 |
| 技能安装/发布 | ✅ | 新 Skills、插件、clawhub publish |
| 系统修改 | ✅ | 版本升级、环境变化、修复完成 |
| 定时任务 | ✅ | cron 创建/更新、定期检测 |
| 重要决定 | ✅ | 技术选型、方案切换 |
| 日常闲聊 | ⏭️ | 跳过（LLM 自动识别） |
| 简单问答 | ⏭️ | 跳过（规则预过滤） |

**脱敏保护：**
- ✅ 自动检测 API Key / Token / Secret
- ✅ 识别 sk-, ghp_, clh_, tvly- 等模式
- ⚠️ 检测到敏感信息时添加警告标记

---

## 📁 文件结构

```
memory-manager/
├── SKILL.md              # 此文件
├── README.md             # 快速入门
├── LICENSE               # MIT 许可证
├── _meta.json            # ClawHub 元数据
├── install.sh            # 安装脚本
├── templates/
│   └── MEMORY.md.template # MEMORY.md 模板
└── scripts/
    ├── init-memory.sh    # 初始化脚本
    └── update-memory.sh  # 智能更新脚本（混合模式）
```

---

## 🔧 使用示例

### 初始化 MEMORY.md

```bash
./scripts/init-memory.sh
```

生成：
```markdown
# MEMORY.md - Roxy 的长期记忆

## 👤 关于用户
- 称呼：老师
- 时区：Asia/Shanghai

## 🏠 系统环境
- OpenClaw 版本：2026.4.5
- 主机：Ubuntu

## 📅 重要事件
- 2026-04-07: 初始创建

## 📌 待办事项
- [ ] ...
```

### 手动触发更新

```bash
./scripts/update-memory.sh
```

### 查看更新历史

```bash
openclaw cron runs --jobId <MEMORY 更新任务 ID>
```

---

## 🧩 与其他 Skills 配合

| Skill | 配合方式 |
|-------|----------|
| `edge-tts` | 记录 TTS 配置变更 |
| `tavily-search` | 记录搜索发现 |
| `bqb-sticker` | 记录表情包使用偏好 |

---

## 📊 记忆结构建议

### 必需部分

```markdown
## 👤 关于用户      # 用户偏好、称呼、时区
## 🏠 系统环境      # OpenClaw 版本、主机信息
## ⚙️ 核心配置      # 模型、TTS、频道配置
## 📅 重要事件      # 按日期记录的重要变更
## 📌 待办事项      # 进行中的任务
```

### 可选部分

```markdown
## 💡 项目笔记      # 长期项目进展
## 🔧 故障记录      # 遇到的问题及解决方案
## 📚 学习记录      # 新学到的知识/技能
## 🎯 目标追踪      # 长期目标和进度
```

---

## ⚠️ 注意事项

1. **隐私保护** - MEMORY.md 可能包含敏感信息，注意文件权限
   ```bash
   chmod 600 ~/.openclaw/workspace/MEMORY.md
   ```

2. **文件大小** - 定期清理过时的待办事项，避免文件过大

3. **备份** - 建议将 MEMORY.md 纳入版本控制或定期备份

4. **会话隔离** - 在共享/群组环境中，注意不要泄露他人隐私

---

## 🔍 故障排查

### MEMORY.md 未自动创建

```bash
# 检查 cron 任务
openclaw cron list

# 手动运行初始化
./scripts/init-memory.sh
```

### 更新任务未执行

```bash
# 查看 cron 状态
openclaw cron status

# 查看任务日志
openclaw cron runs --jobId <任务 ID>
```

### 内容未更新

```bash
# 检查 memory/ 目录
ls -la ~/.openclaw/workspace/memory/

# 手动触发更新
./scripts/update-memory.sh
```

---

## 📚 相关资源

- [OpenClaw Cron 文档](https://docs.openclaw.ai/cron)
- [OpenClaw Sessions 文档](https://docs.openclaw.ai/sessions)
- [记忆管理最佳实践](https://docs.openclaw.ai/best-practices/memory)

---

## 📝 更新日志

- **2026-04-08 (1.0.3)** - 实现智能筛选（混合模式）✨
  - 🧠 规则预过滤 + LLM 分析 + 脱敏检测
  - 🔍 30+ 关键词模式快速匹配
  - 🤖 Qwen 模型提炼重要事件
  - 🔐 自动检测 API Key / Token / Secret
  - 💰 成本优化：无匹配时跳过 LLM 调用

- **2026-04-08 (1.0.2)** - 修复文档夸大问题
  - ⚠️ 明确说明自动更新不做智能筛选
  - 删除对不存在文件的引用
  - 添加隐私风险提醒

- **2026-04-07 (1.0.0)** - 初始版本
  - MEMORY.md 模板
  - 每日更新 cron 配置
  - 安装脚本

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

_作者：Roxy (洛琪希) 🐾_
_灵感来源：与老师的深夜对话_
