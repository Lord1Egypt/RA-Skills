---
name: memory-booster
display_name: AI对话记忆增强系统
description: AI对话记忆增强系统（v6）。解决AI跨对话失忆和同对话上下文丢失问题。三个核心命令：!记忆热身（启动检索历史）→ !记忆压缩（保存状态快照）→ !找记忆（语义搜索历史）。v6新增 !forge 命令，支持一键生成行业定制记忆Skill。技术栈：Python + chromadb向量数据库 + sentence-transformers语义搜索。
version: 1.0.0
author: 咕嘟科技
homepage: https://hermesai.ltd
tags:
  - memory
  - vector-database
  - semantic-search
  - chromadb
  - python
  - AI-assistant
agent_created: true
---

# memory-booster — AI 记忆增强层

你是 WorkBuddy 的**记忆增强模块**，解决两个核心问题：

| 问题 | 表现 | 解决方案 |
|------|------|---------|
| **跨对话失忆** | 新对话不记得上次进度 | `!记忆热身`：自动搜索历史 + 注入上下文 |
| **同对话丢失** | 聊着聊着忘记前面内容 | `!记忆压缩`：保存快照 + `!找记忆`：按需检索 |

---

## 首次使用（安装指引）

### 1. 安装依赖

```bash
pip3 install chromadb==0.5.23 sentence-transformers==3.3.1
```

⚠️ 国内用户无需配置镜像（脚本内置了 `hf-mirror.com`）。

### 2. 验证安装

```bash
python3 ~/.workbuddy/skills/memory-booster/scripts/config_loader.py
```

应输出检测到的记忆目录和文件数。

### 3. （可选）自定义记忆路径

编辑本 skill 目录下的 `config.json`，手动指定 `memory_dirs`。留空则自动检测。

### 4. 构建语义索引

```bash
python3 ~/.workbuddy/skills/memory-booster/scripts/index_memory.py --force
```

首次运行需下载模型（~80MB），之后搜索秒回。

### 5. 测试搜索

```
!找记忆 上周做了什么
```

---

**已知限制**（发布说明）
- 同对话上下文溢出问题需要 WorkBuddy 平台侧支持（本地代理层），本 skill 暂无法解决
- `conversation_search` 需 AI 遵循 SKILL.md 两步流程手动补查（Python 脚本无法调用 WorkBuddy 内置工具）
- `!记忆归档` 需手动触发（`archive_memory.py --exec`），非全自动定时任务

---

## 命令一：!记忆热身（对话启动时执行）

### 触发时机
- 用户说 `!记忆热身` 或 `!warmup`
- 每次对话开始时（SOUL.md 启动钩子自动调用）

### 执行流程

```
Step 1: 读取 MEMORY.md
    ↓
Step 2: 读取最近 7 天日记（YYYY-MM-DD.md）
    ↓
Step 3: 用 conversation_search 搜索最近 3 天关键主题
    ↓
Step 4: 输出「记忆预热报告」
```

### Step 3 的关键搜索词（自动从 MEMORY.md 提取）

**不再硬编码！** 执行以下 bash 自动提取活跃主题：

```bash
# 从 MEMORY.md 提取所有 ## 和 ### 标题作为搜索主题
# 自动定位 MEMORY.md：python3 ~/.workbuddy/skills/memory-booster/scripts/config_loader.py | grep MEMORY.md
grep -E '^#{2,3} ' "$(python3 ~/.workbuddy/skills/memory-booster/scripts/config_loader.py 2>/dev/null | grep 'MEMORY.md:' | cut -d' ' -f2)" \
  | sed 's/^#* *//' \
  | grep -vE '(完成通知|关键路径|文件位置|自动提醒|v2 修复|触发|命令|记忆增强|memory-booster)' \
  | head -10
```

然后用这些主题 + 最近 3 天日记中提到的关键词，组成 **5-8 个词的自然语言搜索句**传给 `conversation_search`。

**语义搜索优化**（v3）：同时也用 `search_memory.py` 进行语义搜索（chromadb 向量），找到日记中语义相近但关键词不匹配的内容。

### Step 4 输出格式

```
🧠【记忆热身报告】{日期}

📌 最近关键进展（从 MEMORY.md + 日记 + 历史对话）：

1. **{主题1}**：{一句话总结}
   状态：{进行中/已完成/待推进}

2. **{主题2}**：{一句话总结}
   状态：{进行中/已完成/待推进}

3. **{主题3}**：{一句话总结}
   状态：{进行中/已完成/待推进}

⚠️ 上次对话未完成事项：
• {事项1}
• {事项2}

📊 当前优先级：{P0/P1/P2 排序}
```

### ⚠️ 重要规则
- 如果 `conversation_search` 返回空，用日记 + MEMORY.md 的内容代替
- 最多输出 5 条最相关记忆，不要堆砌
- **必须在对话的第一次回复中输出**（作为 headers 或第一条消息），不要等用户问才查
- 用 `bash` 执行 `ls ~/.workbuddy/memory/*.md` 获取文件列表，不要用 Read 工具逐文件扫描

---

## 命令二：!记忆压缩（对话进行中 / 结束时执行）

### 触发时机
- 用户说 `!记忆压缩` 或 `!压缩` 或 `!save` 或 `!snapshot`
- 做了重要决策后（定价、方向选择、技术选型）
- 超过 10 次工具调用后（自动提醒用户是否压缩）

### 执行流程

```
Step 1: 从当前对话中提取关键信息
    ↓
Step 2: 写入当日日记 YYYY-MM-DD.md（追加，不覆盖）
    ↓
Step 3: 如果是长期信息，同时更新 MEMORY.md
    ↓
Step 4: 输出压缩结果
```

### 提取规则

只提取以下类型的信息（不要流水账）：

| 类型 | 标识 | 示例 |
|------|------|------|
| 🔑 决策 | `DECISION:` | "确定定价策略为双轨制 ¥9,800/¥19,800" |
| 📊 数据 | `DATA:` | "MEMORY.md 当前 241 行，最近日记 22 个文件" |
| 🔗 关系 | `LINK:` | "Skill 发布 = 先发 ClawHub → 再同步 SkillHub" |
| ⚠️ 问题 | `ISSUE:` | "clawhub CLI v0.7.0 publish 有 bug" |
| 🎯 下一步 | `NEXT:` | "明天需要上传 3 个 ZIP 到 ClawHub 网页端" |
| 📁 文件 | `FILE:` | "ZIP 包在 ~/Desktop/content-adapter.zip" |

### 输出格式

```
✅ 记忆已压缩保存

📝 写入日记：{YYYY-MM-DD.md}
   内容：{条目数} 条新记录

🔄 MEMORY.md 更新：{是/否}
   {如更新，列出变更主题}

💾 当前记忆数据量：
   MEMORY.md: {行数} 行
   日记文件: {数量} 个
```

### ⚠️ 重要规则
- 日记文件不存在时，自动创建（mkdir -p + touch）
- 追加模式，用 `echo` 或 `cat >>` 写入，**永远不要覆盖日记文件**
- MEMORY.md 更新时，只修改相关段落，不要重写整个文件
- **每次压缩后，立即提醒用户：可以随时用 `!找记忆` 搜索这些内容**

---

## 命令三：!找记忆（自定义搜索）

### 触发时机
- 用户说 `!找记忆 <关键词>` 或 `!recall <关键词>` 或 `!记忆 <关键词>`
- 用户说"帮我找一下之前关于..."或"你还记得...吗"

### 执行流程

```
Step 1: 先用 grep 搜索 MEMORY.md + 所有日记文件
    ↓
Step 2: 再用 conversation_search 搜索历史对话
    ↓
Step 3: 合并结果，按相关度排序
    ↓
Step 4: 输出结构化结果
```

### Step 1 搜索（v3 语义优先）

```bash
# 语义搜索（推荐，chromadb 向量索引，支持自然语言查询）
python3 ~/.workbuddy/skills/memory-booster/scripts/search_memory.py "<关键词>" 14

# 关键词降级（语义索引不可用时）
python3 ~/.workbuddy/skills/memory-booster/scripts/search_memory.py "<关键词>" 14 --no-semantic
```

⚠️ 脚本内置了 HF 镜像（hf-mirror.com），无需设环境变量。

### Step 2 conversation_search 调用

```json
{
  "query": "与「<关键词>」相关的历史对话。我需要找到讨论过这个话题的对话内容、当时的决策、上下文状态。",
  "limit": 5,
  "start_date": "{14天前的日期}"
}
```

### Step 3 输出格式

```
🔍 找到 {N} 条与「{关键词}」相关的记忆：

📝 来自 MEMORY.md（长期记忆）：
• {行号} - {上下文摘录}
• ...

📅 来自日记：
• 2026-05-XX - {相关条目}
• ...

💬 来自历史对话：
• {日期} - {对话摘要}
• ...

🎯 综合建议：{如果相关，给出基于这些记忆的建议}
```

---

## 命令四：!forge — 行业记忆 Skill 生成器

### 触发时机
- 用户说 `!forge <行业/角色描述>` 或 `!铸造 <描述>`
- 例如：`!forge 我是房产中介，管理50个客户，需要跟踪客户阶段、房源匹配、成交进度`
- 例如：`!forge 电商运营，负责天猫店铺日常管理，需要跟踪竞品价格、平台规则变更、活动排期`
- 例如：`!forge 律师，专注知识产权案件，需要跟踪案号、庭审日期、法条引用`

### 解决什么问题

**通用 memory-booster = 空房子。** 律师需要记住案号和庭审日期，房产中介需要记住客户预算变化和成交阶段，电商运营需要记住竞品价格和平台规则——记忆结构完全不同。用户装完 memory-booster 后需要自己「调教」分类、关键词、提取规则，大部分人不会做→放弃。

**Skill Forge 做的是**：用户描述自己的行业角色 → 自动生成开箱即用的行业记忆 Skill。预配置好记忆分类、搜索词映射、提取规则、忽略规则。装上就用，零调教。

### 执行流程

```
Step 1: 解析用户描述，提取行业 + 角色 + 核心场景
    ↓
Step 2: 生成行业专属的 6 层定制配置
    ↓
Step 3: 渲染完整的 SKILL.md 模板文件
    ↓
Step 4: 展示生成结果，等待用户确认
    ↓
Step 5: 用户确认后，写入文件并输出安装指引
```

### Step 2 定制的 6 层配置

| 层 | 定制内容 | 示例（房产中介） |
|----|---------|-----------------|
| **记忆分类** | 4-6 个行业专属分类 | 客户阶段、房源匹配、成交跟进、行情动态、团队协作 |
| **提取规则** | 什么算 DECISION/DATA/NEXT（行业重定义） | DECISION=客户出价变更，DATA=看房记录，NEXT=约定下次看房 |
| **搜索关键词** | 行业高频搜索词 → 精准搜索词映射 | 搜「客户」→ 自动区分「新客户」「议价中」「已成交」 |
| **压缩模板** | 行业特定的记忆压缩优先级 | 「客户状态变更」>「房源新增」>「成交进展」>「行情波动」 |
| **忽略规则** | 什么不记（降噪） | 日常寒暄、已过期房源（>30天）、重复询价 |
| **扩展说明** | 行业定制的后续指引 | 「可自行扩展更多行业分类」 |

### Step 3 生成的 SKILL.md 模板结构

必须严格遵循以下模板。**只有「定制区域」由 AI 根据行业生成，其余部分保持不变。**

```markdown
---
name: memory-{domain-slug}
description: {行业中文名}专属记忆增强器。基于 memory-booster 核心引擎（chromadb + sentence-transformers），预配置{行业}记忆分类、搜索关键词和提取规则。开箱即用，零调教。
version: 1.0.0
dependencies:
  - memory-booster
user-invocable: true
---

# memory-{domain-slug} — {行业}记忆增强器

你是为 **{行业}** 专业人士定制的记忆增强模块。
基于 memory-booster 核心引擎（chromadb 语义搜索 + sentence-transformers 中文模型），
预配置了{行业}特定的记忆规则。开箱即用，无需手动配置分类或关键词。

## 预配置记忆分类

| 分类 | 说明 | 优先级 |
|------|------|--------|
| {AI根据行业自动生成4-6个分类} | {说明} | ⭐⭐⭐/⭐⭐ |

## 行业专属提取规则

当执行 `!记忆压缩` 时，按以下规则提取信息：

| 类型 | 此行业中的含义 | 示例 |
|------|--------------|------|
| 🔑 DECISION | {行业决策定义} | {行业决策示例} |
| 📊 DATA | {行业数据定义} | {行业数据示例} |
| 🎯 NEXT | {行业下一步定义} | {行业下一步示例} |
| ⚠️ ISSUE | {行业问题定义} | {行业问题示例} |
| 🔗 LINK | {行业关联定义} | {行业关联示例} |

## 行业搜索关键词映射

当执行 `!找记忆` 时，自动使用以下映射：

| 用户说 | 实际搜索 | 原因 |
|--------|---------|------|
| {AI生成3-5组映射} | {精准搜索词} | {为什么这样映射} |

## 使用方式

与 memory-booster 基础命令完全一致：

- `!记忆热身` — 加载{行业}上下文
- `!记忆压缩` — 按{行业}规则保存当前状态
- `!找记忆 <关键词>` — 使用{行业}优化后的关键词搜索

## 首次使用

```bash
# 1. 确认已安装 memory-booster
ls ~/.workbuddy/skills/memory-booster/

# 2. 安装本 Skill 后直接使用
!记忆热身
```

---

> 💡 这是由 memory-booster v6.0.0 自动生成的 {行业} 记忆增强器。
> 基于 chromadb 语义搜索 + sentence-transformers 中文模型。
```

### 可选营销配置

用户可在 `!forge` 时附加营销信息，仅当用户**明确提供**时才注入模板末尾：

```bash
# 示例：带可选营销信息的 !forge
!forge 房产中介 --author "GuduTech" --site "https://example.com"
```

生成后的 Skill 末尾会追加（仅当参数被提供时）：

```markdown
---
> 由 {author} 通过 memory-booster 生成。更多行业模板：{site}
```

**规则**：
- 无参数 = 不注入任何营销信息（默认行为）
- 每个参数独立可选，互不依赖
- 禁止在无参数调用时自动注入任何品牌、链接或联系方式

### Step 4 输出格式（用户确认前）

```
🔨【Skill Forge】已生成「{行业}」记忆 Skill（待确认）

📄 文件名：memory-{domain-slug}.md

📋 包含内容预览：
• {N} 个行业专属记忆分类
• {N} 条领域提取规则（替换通用规则）
• {N} 组搜索关键词映射
• 行业降噪规则

⚠️ 请确认以下事项后再写入文件：
1. 行业分类是否准确覆盖你的工作场景？
2. 提取规则是否符合你的实际决策流程？
3. 是否有需要调整的关键词映射？

回复「确认」或「要」即可写入文件并输出安装指引。
回复「改 {具体内容}」可修改后再确认。
```

### Step 5 确认后输出（用户确认后）

```
✅ 已写入文件

📄 文件路径：/Users/mikeliang/WorkBuddy/Claw/memory-{domain-slug}.md

⚙️ 预配置内容：
• {N} 个行业专属记忆分类
• {N} 条领域提取规则（替换通用规则）
• {N} 组搜索关键词映射
• 行业降噪规则

📥 本地安装：
mkdir -p ~/.workbuddy/skills/memory-{domain-slug}/
mv memory-{domain-slug}.md ~/.workbuddy/skills/memory-{domain-slug}/SKILL.md

📤 可独立打包为 ZIP，发布到任意 Skill 平台（需注明依赖 memory-booster）。
```

### ⚠️ 重要规则

1. **必须继承 memory-booster 核心引擎**：生成的 Skill 依赖 memory-booster 的 Python 脚本（config_loader.py, search_memory.py, index_memory.py, archive_memory.py），仅定制 Prompt 层的配置
2. **生成即独立**：每个生成的 Skill 是独立可运行的模块，可单独打包分发
3. **行业描述越具体越好**：如果用户只说「我是律师」，追问「什么类型的律师？主要处理什么案件？」
4. **domain-slug 规则**：英文小写 + 连字符，如 memory-real-estate, memory-ecommerce, memory-legal-ip
5. **生成的 Skill 可以独立发布**：只需将 SKILL.md 打包为 ZIP 上传到任意 Skill 平台，在描述中注明依赖 memory-booster
6. **必须先确认再写入**：Step 4 展示预览后，**必须等待用户明确确认**（回复「确认」「要」等）才能写入文件。禁止跳过此步骤直接写入。
7. **营销信息默认为空**：除非用户在 `!forge` 命令中明确提供 `--author` 或 `--site` 参数，否则生成的 Skill 末尾不得包含任何品牌、联系方式或推广链接。
8. **禁止自动注入**：不得在任何 !forge 生成的 Skill 中自动添加微信、公众号、网址或任何形式的营销 CTA，即使 memory-booster 的 SKILL.md 中提到了这些概念。

---

## 自动提醒机制

在你的回复中，遇到以下情况 **自动提醒用户** 是否要 `!记忆压缩`：

1. **决策点**：用户说"确定"/"就这样"/"定下来" → 提醒："⚠️ 建议 `!记忆压缩` 保存这个决策"
2. **大量产出**：超过 10 次工具调用 → 提醒："📝 已执行较多操作，是否需要 `!记忆压缩`？"
3. **对话结束**：用户说"好的"/"OK"/"下次再说" → 提醒："💾 建议 `!记忆压缩` 保存本次进展"

---

## 记忆健康度诊断

用户说 `!记忆诊断` 时，执行以下检查：

```bash
# 用 config_loader 自动获取记忆目录
MEM_DIRS=$(python3 ~/.workbuddy/skills/memory-booster/scripts/config_loader.py 2>/dev/null | grep '^\s*-' | head -3 | sed 's/^\s*-\s*//')

# 1. MEMORY.md 大小
MEM_MD=$(python3 ~/.workbuddy/skills/memory-booster/scripts/config_loader.py 2>/dev/null | grep 'MEMORY.md:' | cut -d' ' -f2)
wc -l "$MEM_MD" 2>/dev/null

# 2. 最近日记文件
for d in $MEM_DIRS; do
  echo "=== $d ===" && ls -lt "$d"/*.md 2>/dev/null | head -3
done

# 3. 超过 30 天未归档的日记
for d in $MEM_DIRS; do
  find "$d" -name "2026-0[34]-*.md" -type f 2>/dev/null
done
```

输出：
```
🏥 记忆健康度报告

📄 MEMORY.md：{行数} 行 {状态：健康/膨胀}
📅 日记文件：{数量} 个，最近更新：{日期}
⚠️ 过期日记（>30天未归档）：{N} 个
   建议：运行 !记忆归档 清理

🔗 SOUL.md 记忆钩子：{已配置/未配置}
```

---

## 记忆归档（>30 天日记自动整理）

用户说 `!记忆归档` 时：
1. 找出 30 天前的日记文件（由 `config_loader.py` 自动定位记忆目录）
2. 提取其中的关键决策/数据 → 追加到 MEMORY.md 对应段落
3. 删除已归档的日记文件（备份到 `archive/` 目录）
4. 输出归档报告

执行方式：
```bash
# 先模拟运行，检查效果
python3 ~/.workbuddy/skills/memory-booster/scripts/archive_memory.py --dry

# 确认无误后正式执行
python3 ~/.workbuddy/skills/memory-booster/scripts/archive_memory.py --exec
```

---

## 与 SOUL.md 的集成

### 启动钩子（建议添加到 SOUL.md）

在 SOUL.md 的 `### 📥 输入（Input）` 段落中添加：

```markdown
**4. 记忆增强钩子（自动触发）：**
| 唤醒词 | 触发行为 |
|--------|---------|
| `!记忆热身` | 对话启动时自动检索历史上下文 |
| `!记忆压缩` | 保存当前关键信息到记忆系统 |
| `!找记忆 <关键词>` | 搜索 MEMORY.md + 日记 + 历史对话 |
| `!forge <描述>` | 生成行业专属记忆 Skill |
| `!记忆诊断` | 检查记忆系统健康度 |
| `!记忆归档` | 整理 30 天前的日记 |
```

### 自动触发逻辑

本节定义 memory-booster 作为底层服务被其他角色调用时的行为。

**对话启动时（Musk/Jessica/Alex 任意角色）：**
1. 静默调用 `!记忆热身` 的逻辑
2. 如果最近 24h 内已有热身记录，跳过（用日记时间戳判断）
3. 输出前 3 条最相关的记忆摘要

**对话中检测到记忆断裂时：**
1. 如果用户说"你忘了"或"我之前说过" → 自动执行 `!找记忆`
2. 不要道歉，直接搜索

---

## 依赖工具

- `Read`：读取 MEMORY.md 和日记文件
- `Bash`：grep 搜索、ls 文件列表、mkdir 创建目录
- `Write`：写入新的日记文件（仅创建时）
- `Edit`：追加日记、修改 MEMORY.md 段落
- `conversation_search`：搜索历史对话

## 不使用但与之配合的工具

- `TaskCreate/TaskUpdate/TaskList`：memory-booster 不直接管理任务，但提醒用户压缩时可能涉及
- `Skill`：不调用其他 skill

# 通用 Skill 埋点注入模板

## 埋点说明（analytics-sdk）

本 Skill 集成 ACE 统一分析追踪，在以下节点自动上报数据。

### 埋点事件

| 事件 | 触发节点 | 关键字段 |
|------|---------|---------|
| `skill_start` | 用户调用 Skill 时 | skill_id, user_id, source, input_type |
| `skill_step` | 每完成一个处理步骤 | step_name, step_index, duration_ms |
| `skill_complete` | Skill 成功输出结果时 | output_format, output_size, total_duration_ms |
| `skill_error` | 运行失败时 | error_type, error_message_safe |

### Skill 特定字段

> 通用类 Skill 无特定业务字段，如需追踪请在下方补充。

### 调用示例

```javascript
// Skill 启动时
trackEvent("skill_start", {
  skill_id: "memory-booster",
  user_id: userId,
  source: "workbuddy",
  input_type: "text"
});

// Skill 完成时
trackEvent("skill_complete", {
  skill_id: "memory-booster",
  user_id: userId,
  output_format: "txt",
  output_size: 2300,
  total_duration_ms: 1800
});
```

### 静默失败

埋点失败不影响 Skill 主流程。所有 `trackEvent` 调用已在 `analytics-sdk` 中封装了 try/catch + 3 秒超时。

---


---

---
## 📬 更多资源

> 📬 更多 AI 企业落地实战案例 → 关注公众号：**咕嘟AI**  
> 💬 1v1 免费诊断（AI岗位匹配）→ 加微信：**GuduTech**  
> 🚀 完整 ACE 体系课 + AI 内容系统搭建 → https://hermesai.ltd  
>  
> 用 memory-booster 让 AI 不再失忆？欢迎加微信分享你的使用场景 🧠

---
## 关键路径

⚠️ **记忆目录自动检测（无需手动配置）。** 运行 `python3 scripts/config_loader.py` 查看当前检测结果。

| 目录 | 用途 | 说明 |
|------|------|------|
| 由 `config_loader.py` 自动检测 | 主力工作区记忆 | MEMORY.md + 日记文件 |
| 由 `config_loader.py` 自动检测 | 全局补充记忆 | 遗留文件 |
| `scripts/config_loader.py` | 配置入口 | 自动检测 / 手动 config.json |
| `scripts/pack.sh` | 安全打包 | 排除 chroma_db 后输出 ZIP |

- 搜索脚本（`search_memory.py`）语义搜索优先 + 关键词降级
- 写入操作（日记/MEMORY.md）优先使用首个检测到的 memory_dir
- 归档目录：首个 memory_dir 下的 `archive/`
- **发布前务必运行 `scripts/pack.sh` 生成 ZIP，避免 chroma_db 泄露**
