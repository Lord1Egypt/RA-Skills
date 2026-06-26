---
name: openclaw-obsidian-memory
description: "OpenClaw + Obsidian Vault 永久记忆体系搭建技能。当用户需要：(1) 搭建本地知识库记忆系统 (2) 将 OpenClaw 的记忆检索与 Obsidian Vault 结合 (3) 实现双通道记忆检索（Vault 优先 + memory 补充）(4) 配置每日/每周自动记忆归档 (5) 管理 Obsidian Vault 笔记和双向链接时使用此技能。触发词：obsidian、vault、知识库、永久记忆、记忆体系、双向链接、知识管理。"
---

# OpenClaw + Obsidian Vault 永久记忆体系

用 Obsidian 风格的本地知识库增强 OpenClaw 的记忆能力，实现双通道检索 + 自动归档。

**兼容平台**：Linux / macOS / Windows（Node.js 跨平台，无需 bash）

## ⚡ 一键初始化（首次使用必读）

**用户只需说**：

> "帮我搭建 obsidian 记忆体系"
> "配置 openclaw vault 知识库"
> "启用双通道记忆"

**AI 收到后，自动按以下步骤完成所有配置，无需用户手动操作**：

### Step 1：确认 Vault 路径

询问用户 Obsidian Vault 的位置。如果用户不知道，使用默认路径：

| 平台 | 默认路径 |
|------|----------|
| Linux / macOS | `$HOME/.obsidian-vault` |
| Windows | `%USERPROFILE%\.obsidian-vault` 或 WSL 下 `$HOME/.obsidian-vault` |

如果用户的 Vault 已经存在（比如已有的 Obsidian 库），直接使用该路径。

### Step 2：创建目录结构

```bash
VAULT="<用户确认的路径>"
mkdir -p "$VAULT/notes/areas" "$VAULT/notes/projects" "$VAULT/notes/daily"
mkdir -p "$VAULT/references/ai-chats" "$VAULT/references/web-clips" "$VAULT/references/books"
mkdir -p "$VAULT/templates" "$VAULT/scripts"
```

### Step 3：部署脚本

将技能自带的脚本复制到 Vault：

```bash
# 技能安装后的 scripts 目录（OpenClaw 自动解压到 skills 下）
SKILL_DIR="$(dirname "$(dirname "$0")")"  # 技能根目录
cp "$SKILL_DIR/scripts/obsidian-search.js" "$VAULT/scripts/"
cp "$SKILL_DIR/scripts/obsidian-links.js" "$VAULT/scripts/"
```

### Step 4：创建初始永久笔记

在 `notes/areas/` 下创建以下笔记（参考 `references/templates.md` 中的模板）：

| 笔记文件 | 内容 |
|----------|------|
| `user-preferences.md` | 从当前 AGENTS.md / USER.md / SOUL.md 中提取用户偏好 |
| `system-config.md` | 从当前 MEMORY.md 中提取系统配置信息 |
| `installed-skills.md` | 列出当前已安装的技能 |
| `known-issues.md` | 从当前 MEMORY.md 中提取已知问题 |

每篇笔记必须包含：
- 至少一个 `[[双向链接]]` 到其他笔记
- 标签（如 `#永久笔记`）

### Step 5：更新 AGENTS.md 记忆规则

在 AGENTS.md 中**追加或替换**记忆规则部分为以下内容：

```markdown
## 记忆规则

### 检索机制（双通道，按需触发）

**不是会话开始盲搜，而是根据用户问题按需检索：**

1. **先检索 Obsidian Vault**：提取用户问题中的关键词，执行
   `exec node <VAULT路径>/scripts/obsidian-search.js <关键词>`
2. **再检索本地 memory**：`memory_search` 最近 3 天记忆
3. 两步结果合并，优先使用 Vault 中的知识内容

**触发时机**：
- 用户提出知识性、概念性问题时
- 用户询问历史决策、偏好、配置时
- 任务完成后需要记录结论时
- 每次重要对话结束时（对话存档）

### 写入机制（双写 + 去重）

**任务完成后，同时写入两个位置：**

1. **Obsidian Vault**：写入对应分类笔记
   - 知识/概念 → notes/areas/<主题>.md
   - 项目进展 → notes/projects/<项目>.md
   - 每日思考 → notes/daily/YYYY-MM-DD.md
2. **本地 memory**：写入 memory/YYYY-MM-DD.md，更新 MEMORY.md 索引

**写入前必须去重**：先用检索检查 Vault 和 memory 是否已有类似记录，有则合并更新，不重复堆积。

### 笔记规范（Obsidian 风格）

- **双向链接**：新建笔记时至少链接到 1 个已有笔记（[[笔记名]]），避免孤立
- **标签**：每篇笔记必须有标签（#永久笔记、#项目/xxx、#daily 等）
- **原子化**：一个笔记只记录一个主题，不混杂
- **上下文**：写结论时不写过程，只写最终答案和关键依据

### 对话存档

每次重要对话结束时，将摘要存入 references/ai-chats/YYYY-MM-DD-slug.md：
- 提取关键结论、决策、待跟进事项
- 不复制原始对话，只写加工后的摘要
- 加上标签和双向链接

### 维护规则

- 定期用 node <VAULT路径>/scripts/obsidian-links.js --orphans 检查孤立笔记，补充链接
- 每周 cron 自动归纳 7 天笔记，去重合并到永久笔记
```

> ⚠️ 替换 `<VAULT路径>` 为 Step 1 中确认的实际路径。

### Step 6：精简 MEMORY.md

将 MEMORY.md 精简为以下内容（详细内容写入 Vault）：

```markdown
# 记忆索引

> 轻量索引，详细内容见 Obsidian Vault（<VAULT路径>）

## 数据存储
- **Obsidian Vault**: <VAULT路径>
- **本地 memory**: memory/ 目录（近3天热记忆）
- **检索顺序**: 先 Vault → 再 memory → 合并结果
```

### Step 7：配置定时归档（询问用户）

询问用户是否需要自动归档：

> "是否需要配置自动记忆归档？每天凌晨自动整理对话记录到 Vault。"

如果用户同意，创建两个 cron 任务：

**每日归档**：
```
openclaw cron add \
  --name "daily-memory-archive" \
  --cron "0 2 * * *" \
  --tz "Asia/Shanghai" \
  --timeout-seconds 120 \
  --session "isolated" \
  --no-deliver \
  --message "每日记忆归档：总结过去24小时会话，写入 Vault/notes/daily/YYYY-MM-DD.md 和 memory/YYYY-MM-DD.md"
```

**每周归纳**：
```
openclaw cron add \
  --name "weekly-memory-summary" \
  --cron "0 3 * * 1" \
  --tz "Asia/Shanghai" \
  --timeout-seconds 180 \
  --session "isolated" \
  --no-deliver \
  --message "每周记忆归纳：汇总7天笔记，去重合并写入 Vault/notes/areas/ 永久笔记"
```

### Step 8：完成提示

初始化完成后，告知用户：

```
✅ Obsidian 记忆体系已搭建完成！

Vault 路径：<路径>
脚本位置：<路径>/scripts/
笔记目录：<路径>/notes/
对话存档：<路径>/references/ai-chats/

现在你可以：
- 直接问我任何问题，我会自动检索 Vault 中的知识
- 任务完成后我会自动记录到 Vault
- 重要对话结束我会自动存档

手动检索：告诉我"搜索 Vault 中的 xxx"
```

---

## 日常使用

配置完成后，**用户正常对话即可**，AI 会自动：

| 场景 | AI 行为 |
|------|---------|
| 知识性问题 | 自动搜索 Vault + memory，合并回答 |
| 任务完成 | 自动写入 Vault 对应笔记 + memory |
| 重要对话结束 | 自动存档到 `references/ai-chats/` |
| 用户说"搜索 xxx" | 手动触发 Vault 检索 |

## 检索命令参考

```bash
# 基础检索
node <VAULT>/scripts/obsidian-search.js "关键词"

# 自定义 Vault 路径
OBSIDIAN_VAULT=/path/to/vault node <VAULT>/scripts/obsidian-search.js "关键词"

# 多关键词（AND 语义）
node <VAULT>/scripts/obsidian-search.js "关键词1" "关键词2"

# 调整结果数和上下文
node <VAULT>/scripts/obsidian-search.js "关键词" --limit 5 --context 3

# 链接图谱
node <VAULT>/scripts/obsidian-links.js

# 孤立笔记检测
node <VAULT>/scripts/obsidian-links.js --orphans
```

## 笔记规范

### 双向链接
```markdown
## 关联笔记
- [[系统配置]]
- [[用户偏好]]
```

### 标签
```markdown
#永久笔记 #系统配置 #openclaw
```

### 笔记类型

| 类型 | 目录 | 说明 |
|------|------|------|
| 永久笔记 | `notes/areas/` | 经过加工的核心知识 |
| 项目笔记 | `notes/projects/` | 项目相关记录 |
| 每日笔记 | `notes/daily/` | 每日思考摘要 |
| 对话存档 | `references/ai-chats/` | AI 对话摘要（只存结论） |
| 文献笔记 | `references/` | 外部资料加工 |
