---
name: lobster-skill-radar
display_name: 龙虾Skill雷达
description: >
  智能扫描用户电脑中的 WorkBuddy Skill 资产，
  自动发现散落在各处的 Skill，卡片式展示后支持多选，
  无缝对接 Skill矩阵分发助手 一键上传六大平台。
  解决"做了 N 个 Skill 却找不到"的核心痛点。
  内置隐私授权弹窗，确保用户数据主权。
version: "1.1.0"
author: 青木会江湖
tags: [skill, 资产发现, 扫描, 分发, 龙虾, 雷达, 隐私授权]
icon: "🦞"
category: productivity
language: zh-CN
license: MIT
entry:
  type: conversation
  trigger: ["找skill", "扫描skill", "我的skill在哪", "skill资产", "帮我找skill", "skill雷达"]
requirements: []
platforms: [Windows, macOS, Linux]
---

# 龙虾Skill雷达 🦞

> 你做过的每一个 Skill，都值得被找到、被看见、被分发。

## 核心价值

```
之前：用户得自己知道 skill 在哪 → 手动找到 → 矩阵分发
之后：智能扫描 → 发现所有 skill 资产 → 勾选 → 一键分发
```

| 痛点 | 解法 |
|------|------|
| 做了 N 个 skill，散落各处找不到 | 全盘智能扫描，一网打尽 |
| 不知道哪些能上传换影响力 | 卡片展示，按需勾选 |
| 找到 skill 后还要手动分发 | 无缝对接矩阵分发助手，选完即发 |

---

## 🔐 隐私授权机制（铁律）

**任何扫描操作前，必须先弹出授权确认，不得跳过！**

### 授权弹窗格式（首次触发时展示）

```
🦞 龙虾Skill雷达 — 隐私授权确认

为了帮您找到散落各处的 Skill 资产，需要授权访问以下内容：

☑ 扫描 C:\ 盘（所有文件）
☑ 扫描 D:\ 盘（所有文件）
☐ 扫描其他盘（请指定：_____）
☑ 读取 ~/.workbuddy/skills/（用户级 Skill）
☑ 读取 WorkBuddy 聊天记录（workbuddy.db）
☑ 读取 ~/.workbuddy/memory/（记忆文件）

授权说明：
- 所有扫描仅在本地执行，不会上传您的任何文件
- 您可以随时取消授权，取消即停止所有扫描
- 扫描结果仅展示给您的会话，不会共享给第三方

［ 开始扫描 ］  ［ 取消 ］
```

### 执行规则

1. **用户未授权** → 任何操作都不执行，等待用户点击"开始扫描"
2. **用户取消** → 回复："扫描已取消。如需重新扫描，请再次说「帮我找我的 skills」"
3. **授权后只扫指定盘** → 严格按照勾选项执行，不多扫
4. **深度扫描需二次确认** → 浅扫无结果时，先问用户"是否开启深度扫描？"，用户确认后才执行

---

## 核心工作流

```
用户触发（"帮我找 skills"）
        │
        ▼
┌───────────────────────────────────────┐
│  Step 0: 隐私授权弹窗（必须）         │
│  → 用户勾选授权范围                   │
│  → 点击"开始扫描"                    │
└───────────────────────────────────────┘
        │ 授权通过
        ▼
┌───────────────────────────────────────┐
│  Step 1: 浅度扫描（默认）             │
│  → 扫描 ~/.workbuddy/skills/        │
│  → 扫描各项目 .workbuddy/skills/    │
│  → 读 SKILL.md 前50行（元数据）     │
│  → 读 config.json（名称/版本/tags）  │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│  Step 2: 聊天记录挖掘（授权后）       │
│  → 查询 workbuddy.db                  │
│  → 提取"曾创建 skill"的线索          │
│  → 即文件已删除，也能提示用户        │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│  Step 3: 去重合并 + 卡片式展示       │
│  → 按名称去重，保留最新版本         │
│  → 卡片式 Markdown 输出              │
│  → 每个卡片带复选框 ☑              │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│  Step 3.5: 分发确认与引导（必须）     │
│  → 主动询问用户：是否要分发？       │
│  → 确认哪些 skill 要分发            │
│  → 引导安装 Skill矩阵分发助手        │
│  → 切换到分发助手工作模式            │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│  Step 4: 一键分发六大平台            │
│  → 用户勾选要上传的 skill           │
│  → 对接 skill-matrix-publisher-free  │
│  → 逐个推送到 6 大平台               │
└───────────────────────────────────────┘
```

---

## Step 1&2: 扫描逻辑详解

### 扫描目标清单

| 扫描目标 | 路径 | 说明 |
|-----------|------|------|
| 用户级 skills | `~/.workbuddy/skills/` | 所有用户级 skill |
| 项目级 skills | 各项目 `.workbuddy/skills/` | 需要遍历常见项目目录 |
| WorkBuddy 数据库 | `~/.workbuddy/workbuddy.db` | SQLite，聊天记录 |
| 记忆文件 | `~/.workbuddy/memory/` | 用户信息 |
| 会话记录 | `~/.workbuddy/sessions/` | 历史会话 |

### 浅度扫描（默认）

```python
# 浅扫：只解析元数据，不读完整文件内容
 Target: SKILL.md 前50行 + config.json

解析 SKILL.md 前50行，提取：
  - YAML frontmatter: name, version, author, tags, description
  - 若无 frontmatter，从正文第1行提取标题

解析 config.json，提取：
  - name, display_name, version, author, tags, description
```

### 深度扫描（用户二次确认后）

```python
# 深扫：读取完整文件内容
 Target: SKILL.md 全文 + config.json 全文 + README.md

额外动作：
  - 读取 SKILL.md 全文，提取完整 description
  - 读取 README.md，补充展示信息
  - 遍历文件树，统计文件数量/总大小
  - 检测是否包含 install.sh / install.ps1（可分发性判断）
```

### 聊天记录挖掘（workbuddy.db）

```sql
-- 从聊天记录中挖掘"曾创建 skill"的线索
SELECT DISTINCT message_content
FROM messages
WHERE message_content LIKE '%创建%skill%'
   OR message_content LIKE '%skill%创建%'
   OR message_content LIKE '%生成%sill%'
ORDER BY timestamp DESC
LIMIT 50;
```

```sql
-- 从 automation 记录中挖掘
SELECT DISTINCT prompt
FROM automations
WHERE prompt LIKE '%skill%'
ORDER BY created_at DESC;
```

> **价值**：即使用户把 skill 文件删了，只要聊过"帮我创建一个 XX skill"，就能追溯出来提醒他。

---

## Step 3: 卡片式展示格式

扫描完成后，用以下 Markdown 格式输出结果：

``markdown
🦞 **龙虾Skill雷达 — 扫描结果**

> 共找到 **N** 个 Skill（浅度扫描结果）
> 勾选要上传的 Skill，然后告诉我即可一键分发 ✨

---

### ☑ Skill矩阵分发助手（免费版）

> 版本：v3.5.1 ｜ 作者：青木会江湖
> 路径：`~/.workbuddy/skills/skill-matrix-publisher-free/`
> 平台适配：🦞虾友  🔷腾讯  🦞虾聊  🐙ClawHub  🐙GitHub

**简介：** 一键将免费Skill分发到腾讯SkillHub、虾聊、虾友SkillHub、GitHub、ClawHub六大平台，支持版本更新与双通道安装。

**标签：** `#skill分发` `#六平台` `#版本更新` `#CLI安装`

---
**[用户在这里回复：上传第1、3个]**

---

### ☑ 龙虾记忆方舟

> 版本：v2.0 ｜ 作者：青木老贼
> 路径：`D:/workbuddy工作文档/.../.workbuddy/skills/lobster-memory-ark/`
> 平台适配：🦞虾友  🔷腾讯

**简介：** 龙虾智能体的专业记忆管理系统，支持上下文记录整理、核心内容归档、创作者项目建议、全局长期记忆。

**标签：** `#记忆` `#知识库` `#AI智能体`

---
**[若浅扫无结果，展示以下提示]**

> 💡 浅度扫描未找到 Skill，是否开启**深度扫描**？
> 深度扫描将读取完整文件内容，耗时稍长，但能发现更多 Skill。
> ［ 开启深度扫描 ］ ［ 取消 ］

````

### 卡片格式规范

```
### ☑ {skill名称}（{图标}）

> 版本：{version} ｜ 作者：{author}
> 路径：{path}
> 平台适配：{适配平台图标列表}

**简介：** {description 前80字}

**标签：** {tags 以 `#` 格式展示}

---
```

---

## Step 3.5: 分发确认与引导（铁律 — 卡片展示后必须执行）

**卡片展示完毕后，AI 必须主动向用户确认是否分发，不得跳过！**

### 标准话术模板

卡片展示完毕后，立即追加以下引导：

```
---

🦞 **接下来要分发吗？**

以上是您 D 盘 / C 盘的 Skill 家底。
请确认哪些要分发到平台？回复方式：
- "全部分发" → 将所有 Skill 推送到六大平台
- "分发第 1、3 个" → 只分发勾选的 Skill
- "暂不分发" → 保留结果，后续再说

> 💡 提示：分发需要用到 **Skill矩阵分发助手**，如未安装：
> - 推荐：WorkBuddy【专家】→【技能】→ 搜索「Skill矩阵分发助手」
> - 搜不到？复制粘贴命令行安装：
>   `curl -fsSL https://skillhub.cn/install/install.sh | bash`
```

### 用户确认分发后的执行流程

```
用户确认要分发
      │
      ▼
┌─────────────────────────────────────────────┐
│  引导步骤 1: 提示安装 Skill矩阵分发助手      │
│  → 方式A（推荐）：WorkBuddy 左侧栏【专家】    │
│     → 【技能】标签 → 搜索「Skill矩阵分发助手」│
│     → 安装                                     │
│  → 方式B（搜不到时）：命令行一键安装          │
│     curl -fsSL https://skillhub.cn/install/    │
│     install.sh | bash                          │
│  → 若搜中文无结果，试英文 keyword：            │
│     "skill-matrix" 或 "publisher"              │
└─────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────┐
│  引导步骤 2: 切换到分发助手工作模式          │
│  → "安装完成后，请切换到「Skill矩阵分发助手」│
│     专家模式，然后告诉我：                   │
│     '帮我把 {skill名称} 分发到以下平台：      │
│      🦞虾友SkillHub / 🔷腾讯SkillHub         │
│      🦞虾聊 / 🐙ClawHub / 🐙GitHub'         │
└─────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────┐
│  引导步骤 3: 确认目标平台                    │
│  → 默认：虾友SkillHub + 腾讯SkillHub        │
│  → 可选：虾聊 / ClawHub / GitHub             │
│  → 用户指定平台后，切换到分发助手执行        │
└─────────────────────────────────────────────┘
```

### 设计原则

| 原则 | 说明 |
|------|------|
| **雷达做发现，助手做分发** | 龙虾Skill雷达只负责扫描和推荐，分发动作交由 skill-matrix-publisher-free 专属执行 |
| **先确认再引导** | 用户说"要分发"才引导安装，不强行推送 |
| **切换工作模式** | 引导用户在专家模式下使用分发助手，享受完整的六大平台分发能力 |
| **不重复造轮子** | Skill矩阵分发助手已有成熟的六平台分发逻辑，雷达无缝对接即可 |

---

## Step 4: 一键分发对接

用户回复"上传第 X 个"或"上传 XXX skill"后：

```
1. 确认用户勾选的 skill 列表
2. 询问目标平台（默认：腾讯SkillHub + 虾友SkillHub）
3. 调起 skill-matrix-publisher-free：
   - 对每个选中的 skill：
     a. 读取完整 SKILL.md + config.json
     b. 调用矩阵分发助手的分发逻辑
     c. 推送到指定平台
   - 实时反馈每个 skill 的上传状态
4. 完成后展示上传结果报告
```

### 分发结果报告格式

``markdown
🦞 **Skill分发报告**

| Skill名称 | 虾友SkillHub | 腾讯SkillHub | 虾聊 | ClawHub | GitHub |
|-----------|------------|------------|--------|----------|--------|
| Skill矩阵分发助手 | ✅ | ✅(pending) | ✅ | ✅ | ✅ |
| 龙虾记忆方舟 | ✅ | ✅(pending) | — | — | ✅ |

✅ = 上传成功  ⏳ = 审核中  ❌ = 失败  — = 不适配
``

---

## 错误处理

### 扫描无结果

``markdown
🦞 扫描完成，但未找到任何 Skill 文件。

可能原因：
1. Skill 文件存储在未授权的盘符
2. 文件夹名称不是 `skills`
3. Skill 文件已被删除

建议：
- ［ 扩大扫描范围 ］（授权更多盘符）
- ［ 开启深度扫描 ］（扫描更多目录）
- ［ 从聊天记录恢复 ］（我有聊天记录线索）
``

### 聊天记录挖掘无结果

``markdown
🦞 聊天记录中未找到明确的 Skill 创建记录。

建议：
- 回忆一下当时是怎么描述这个 Skill 的？
- 试试告诉我关键词，我帮你全文搜索聊天记录
``

### 分发失败

``markdown
⚠️ {skill名称} 上传到 {平台} 失败：

错误原因：{error_message}

建议处理方式：
1. 检查该平台的凭证是否已配置（询问用户）
2. 检查 Skill 的 SKILL.md 是否符合平台规范
3. 重试上传
``

---

## 配置说明

本 Skill 无需额外配置，所有扫描均在本地执行。

如需自定义扫描范围，可在对话中指定：
- "只扫描 C 盘"
- "不要扫描聊天记录"
- "只找适配腾讯SkillHub的 skill"

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.1.0 | 2026-06-17 | 🚀 新增 Step 3.5「分发确认与引导」场景：卡片展示后主动询问是否分发 → 引导安装矩阵分发助手（GUI+CLI双通道）→ 切换专家模式 → 六大平台分发；新增curl一键安装兜底；新增实战测试记录 |
| v1.0.0 | 2026-06-17 | 🎉 初始发布：隐私授权弹窗 + 浅度/深度扫描 + 聊天记录挖掘 + 卡片式展示 + 一键分发对接矩阵助手 |

---

## 实战测试记录

> 以下为 v1.0.0 → v1.1.0 迭代期间的实战测试过程，涉敏信息已脱敏。

### 测试环境

| 项目 | 值 |
|------|-----|
| 测试日期 | 2026-06-17 |
| 操作系统 | Windows |
| 扫描范围 | D:\workbuddy工作文档\ |
| workbuddy.db 版本 | SQLite 3，约 2MB |

### 测试过程

```
用户：帮我找下我D盘的skill

  雷达：弹出隐私授权弹窗
        ☑ D盘 / ☑ ~/.workbuddy/skills/ / ☑ 聊天记录
        [等待用户"开始扫描"]

用户：开始扫描

  雷达：执行扫描
        ├── find D:\workbuddy工作文档\ -name "SKILL.md" -maxdepth 5
        │   → 命中 6 个 SKILL.md
        │   → 去重后保留 4 个独立 Skill
        ├── 读取每个 SKILL.md 前50行提取元数据
        ├── 查询 config.json（该目录下无）
        └── 查询 workbuddy.db automations 表
            → 命中 2 条 Skill 相关自动化任务线索

  雷达：卡片式展示 4 个 Skill + 2 条线索

  发现：省Token助手、龙虾漂流瓶 仅存 D 盘未安装
        社群收录 有 3 处副本
        find-skills 为系统提取 Skill

用户：（未触发分发引导 — 此为 v1.0.0 的缺失点）
```

### 发现的缺失 → 驱动 v1.1.0

| # | 缺失项 | 修复 |
|---|--------|------|
| 1 | 卡片展示后没有主动问"要不要分发" | 新增 Step 3.5「分发确认与引导」 |
| 2 | 用户不知道分发去哪、怎么做 | 标准话术模板 + 三步骤引导流程 |
| 3 | 雷达和分发助手职责不清 | 明确"雷达做发现，助手做分发"的边界 |

### DB 查询语句验证

```sql
-- ✅ 有效：从 automations 表挖掘 Skill 线索
SELECT id, name, prompt FROM automations
WHERE prompt LIKE '%skill%' OR prompt LIKE '%Skill%'
  OR name LIKE '%skill%' OR name LIKE '%Skill%';

-- ⚠️ 注意：workbuddy.db 实际表结构
-- 有：sessions, workspaces, automations, automation_runs 等
-- 无：messages/conversations 表
-- 聊天记录挖掘需改为查 automations + sessions 表
```

### D 盘扫描命中路径（脱敏示例）

```
disk_letter:\workbuddy工作文档\
├── [project_dir_1]\.workbuddy\skills\shequn-shoulu\    → 社群收录（项目级旧版）
├── [project_dir_2]\.gh_temp\shengtoken-zhushou\       → 省Token助手
├── [project_dir_2]\.gh_temp\shequn-shoulu\            → 社群收录（GitHub副本）
├── [project_dir_2]\.skh_temp\                         → 社群收录（腾讯发布包）
├── skillhub_extracted\cli\skill\                      → find-skills（系统Skill）
└── 开发代码\bottle-api\                                → 龙虾漂流瓶
```

> 🔒 具体项目路径和时间戳已脱敏，仅保留 Skill 名称和相对路径结构

---

## 注意事项

1. **隐私第一**：任何扫描前必须弹授权窗，不得跳过
2. **授权范围严格执行**：只扫用户勾选的盘符/目录
3. **二次确认**：深度扫描、聊天记录读取，必须用户明确确认
4. **不上传用户数据**：所有扫描在本地执行，不上传任何文件
5. **去重逻辑**：同名 skill 只展示最新版本（按 version 排序）
6. **聊天记录线索**：仅作提示，不保证 100% 准确（依赖 SQLite 查询）
