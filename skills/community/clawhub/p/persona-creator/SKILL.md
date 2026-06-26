---
name: persona-creator
description: >
  数字人风格生成器。当用户说"生成我的数字人"、"分析我的说话风格"、"创建我的风格档案"，
  或输入 /superme 进入角色扮演，或使用 [扮演xxx] 前缀时触发本 Skill。
  基于 memory/*.md 中的历史对话（≥10条）提取说话风格，生成 persona/$user.json 档案。
  支持：首次创建、增量刷新、遗忘重置、角色扮演模式（/superme 命令或 [扮演xxx] 前缀）。
metadata:
  openclaw:
    category: persona
    emoji: 🧬
---

# Persona Creator — 数字人风格生成器

## 触发条件

以下任意情况下激活本 Skill：

**风格分析类：**
- 用户说"生成我的数字人"、"分析我的风格"、"创建我的风格档案"、"persona"
- 用户说"更新我的风格"、"刷新风格"、"refresh persona"
- 用户说"遗忘我的风格"、"删除档案"、"forget persona"、"重置档案"

**角色扮演类：**
- 消息以 `/superme <用户名>` 开头（进入角色扮演）
- 消息以 `/superme clear` 开头（退出角色扮演）
- 消息以 `[扮演<用户名>]` 或 `[as:<用户名>]` 开头（进入角色扮演）

---

## 路径约定

所有路径相对于当前 workspace（通常为 `/root/.openclaw/workspace` 或 `$GF_IDE_DEFAULT_PROJECT_ROOT` 的父目录）：

- `memory/` — 短期记忆文件目录（`memory/YYYY-MM-DD.md`）
- `persona/` — 风格档案输出目录
- `persona/yourself.json` — 通用模板，不可删除
- `persona/$user.json` — 用户个人风格档案

Skill 脚本目录（相对本 SKILL.md）：`./scripts/`

---

## 功能一：首次生成风格档案

### 触发词
"生成我的数字人"、"分析我的风格"、"创建风格档案"

### 执行流程

**Step 1：询问用户名**
```
你好！我需要你的名字/昵称来创建风格档案（例如：张三、alice、tom）
请输入你的名字：
```

**Step 2：确认 memory 目录**
- 默认从 `{workspace}/memory/` 读取
- 若不存在，提示用户提供路径

**Step 3：运行分析脚本（dry-run 先检查）**

```bash
python3 {skillDir}/scripts/analyze.py \
  --user "{用户输入的名字}" \
  --memory-dir "{workspace}/memory" \
  --persona-dir "{workspace}/persona" \
  --dry-run
```

- 若发言数 < 10，告知用户并停止，给出提示：
  > "当前仅找到 N 条发言记录，至少需要 10 条才能生成可靠的风格分析。请继续使用后再试。"

**Step 4：运行完整分析，获取 prompt**

```bash
python3 {skillDir}/scripts/analyze.py \
  --user "{名字}" \
  --memory-dir "{workspace}/memory" \
  --persona-dir "{workspace}/persona"
```

从输出中提取 `ANALYSIS_PROMPT_START` 到 `ANALYSIS_PROMPT_END` 之间的内容。

**Step 5：调用 LLM 进行风格分析**

将提取出的 prompt 直接作为用户消息发给自身（或用 exec 写入文件后读取），要求 LLM 严格按 JSON 格式输出。

**Step 6：保存结果**

将 LLM 输出的 JSON 字符串保存到 `/tmp/persona_analysis_result.json`，然后运行：

```bash
python3 {skillDir}/scripts/save_persona.py \
  --analysis-file /tmp/persona_analysis_result.json \
  --meta-file /tmp/persona_meta.json
```

**Step 7：展示摘要报告**

读取生成的 `persona/{名字}.json`，以用户友好的方式呈现：

```
✅ 数字人风格档案生成完成！

👤 用户：{名字}
📊 分析了 {N} 条发言记录（{起始日期} ~ {结束日期}）

🎭 风格画像：
  • 整体语气：{tone.overall}
  • 句式偏好：{sentence_structure.preference}
  • Emoji 使用：{emoji_usage.frequency}，常用 {emoji_usage.favorites}
  • 专业程度：{professionalism.jargon_level}
  • 幽默指数：{humor.level * 10:.0f}/10 — {humor.style}

💬 口头禅：{catchphrases 列表}
🔑 常用词：{common_phrases 列表}
🗂️ 话题偏好：{topic_preferences 列表}

💡 AI 模仿提示词已生成，可通过 /superme {名字} 进入角色扮演模式。
📁 档案保存位置：persona/{名字}.json
```

---

## 功能二：增量刷新

### 触发词
"更新我的风格"、"刷新档案"、"refresh"

### 执行流程

**Step 1：询问用户名**（若上下文中没有）

**Step 2：检查是否需要刷新**

```bash
python3 {skillDir}/scripts/refresh.py \
  --user "{名字}" \
  --memory-dir "{workspace}/memory" \
  --persona-dir "{workspace}/persona"
```

- 若输出 `SKIP:true`，告知用户"无需刷新"
- 若输出 `REFRESH_NEEDED:true`，继续执行新文件的分析

**Step 3：仅对新文件运行分析，合并结果**
- 按与功能一 Step 4-6 相同的流程处理
- save_persona.py 会自动保留 `created_at` 并递增 `version`

**Step 4：展示刷新结果**（与功能一 Step 7 格式相同）

---

## 功能三：遗忘/删除档案

### 触发词
"遗忘我的风格"、"删除档案"、"forget"、"重置"

### 执行流程

**Step 1：询问用户名 + 确认操作**
```
⚠️ 确认要删除 {名字} 的风格档案吗？
  [1] 完全删除（可恢复备份会保留）
  [2] 重置为空白模板（保留文件）
  [3] 取消
```

**Step 2：执行对应操作**

完全删除：
```bash
python3 {skillDir}/scripts/forget.py --user "{名字}" --persona-dir "{workspace}/persona"
```

重置模板：
```bash
python3 {skillDir}/scripts/forget.py --user "{名字}" --persona-dir "{workspace}/persona" --reset
```

**Step 3：确认反馈**
- 删除：`🗑️ {名字} 的风格档案已删除，备份保存为 persona/{名字}.bak.XXXXXX.json`
- 重置：`🔄 {名字} 的风格档案已重置为空白模板`

---

## 功能四：角色扮演模式

### 触发方式 A：斜杠命令

**进入：** 消息以 `/superme <用户名>` 开头
**退出：** 消息以 `/superme clear` 开头

### 触发方式 B：前缀模式

**进入：** 消息以 `[扮演<名字>]` 或 `[as:<名字>]` 开头
**退出：** 消息以 `[/扮演]` 或 `[/as]` 开头

### 进入角色扮演流程

**Step 1：加载 persona 档案**

```python
persona_path = f"{workspace}/persona/{用户名}.json"
```

若档案不存在：
> `❌ 未找到 {用户名} 的风格档案，请先运行"生成我的数字人"创建档案。`

**Step 2：构建角色扮演系统提示**

从 `persona.system_prompt_fragment` 提取基础描述，拼接完整 system prompt：

```
你现在要完全模仿用户「{display_name}」的说话风格来回答问题。

【风格要求】
{persona.persona.system_prompt_fragment}

【具体要求】
- 语气：{persona.persona.tone.overall}，正式程度 {persona.persona.tone.formality_level*10:.0f}/10
- 句式：{persona.persona.sentence_structure.preference}
- Emoji：使用频率「{persona.persona.emoji_usage.frequency}」，偏爱 {persona.persona.emoji_usage.favorites}
- 口头禅：适当穿插 {persona.persona.catchphrases}
- 常用词：{persona.persona.common_phrases}
- 结构化：表格使用={persona.persona.formatting.loves_tables}，列表={persona.persona.formatting.uses_lists}
- 幽默风格：{persona.persona.humor.style}

【重要】只模仿说话风格，不要模仿具体事项。回答时保持自然，不要提及"我在模仿xxx"。
```

**Step 3：进入角色扮演状态**

向用户确认：
```
🎭 已进入角色扮演模式 — 正在模仿「{display_name}」的风格
（输入 /superme clear 或 [/扮演] 退出）
```

**Step 4：以角色风格回答用户问题**

从用户消息中去掉前缀（如 `/superme 名字 ` 或 `[扮演名字]`），将剩余内容作为实际问题，用角色风格回答。

**Step 5：退出角色扮演**

收到退出指令后：
```
👋 已退出角色扮演模式，恢复正常模式。
```

---

## 错误处理

| 错误情况 | 处理方式 |
|---------|---------|
| memory 目录不存在 | 提示用户指定正确路径 |
| 发言数 < 10 | 提示需要更多对话记录 |
| LLM 返回格式错误 | 提示用户重试，或手动修正 JSON |
| persona 文件不存在 | 提示先创建档案 |
| yourself.json 模板缺失 | 从 skillDir 重建默认模板 |

---

## 文件结构

```
{skillDir}/
├── SKILL.md              ← 本文件
├── persona/
│   └── yourself.json     ← 通用模板（勿删）
└── scripts/
    ├── analyze.py        ← 提取发言 + 生成分析 prompt
    ├── save_persona.py   ← 保存 LLM 分析结果
    ├── refresh.py        ← 增量刷新检测
    └── forget.py         ← 删除/重置档案
```

用户档案生成在：`{workspace}/persona/{用户名}.json`
