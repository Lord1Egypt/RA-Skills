---
name: just-note
description: |
  像发消息一样记录一切（灵感/想法/知识/收支/日记/任务/引用），AI 自动分类、标签、关联，让知识自然生长。
  支持微信/飞书消息输入，零摩擦记录。统一存储，多视图呈现（闪记视图/日记视图/周报视图）。
  触发：用户发送任何想记录的内容时自动调用。
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
---

# 记一下 (just-note) - 零摩擦知识记录

## 一句话定位

> 像发消息一样记录一切，AI 自动分类整理，让知识自然生长。

## 核心能力

| 能力 | 说明 |
|------|------|
| **零摩擦输入** | 微信/飞书发消息即可记录，无需打开任何界面 |
| **AI 自动分类** | 自动识别 9 类内容（inspiration/idea/knowledge/expense/income/diary/task/quote/other） |
| **AI 标签生成** | 自动生成 3-5 个标签，便于检索 |
| **AI 标题生成** | 自动生成简洁标题 |
| **统一存储** | 所有记录存储在统一位置，支持多视图呈现 |
| **智能检索** | 关键词搜索 + 类型筛选 + 语义检索 |
| **日记视图** | 按天聚合记录，支持每日汇总 |
| **周报/月报** | AI 自动生成的周期性总结 |

## 内容类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **inspiration** | 灵感、创意、想法 | 「这个产品功能可以这样做...」 |
| **idea** | 想法、读书心得 | 「今天读到的一句话很有启发...」 |
| **knowledge** | 知识点、解释 | 「Python 的装饰器原理是...」 |
| **expense** | 支出记录 | 「花了¥200 买书」 |
| **income** | 收入记录 | 「收到稿费¥5000」 |
| **diary** | 日记、感受 | 「今天遇到了一个有趣的人...」 |
| **task** | 待办事项 | 「记得下周约医生」 |
| **quote** | 引用、名人名言 | 「XXX 说：...」 |
| **other** | 其他无法分类的内容 | - |

## 快速开始

### 方式 1：微信/飞书消息（推荐）

**发送消息即可，AI 自动分类**：

```
这个产品功能可以这样做：用户发消息后，AI 自动分类并存入知识库，比手动标签简单多了
```

AI 自动处理：
- 类型：inspiration
- 标签：[product, ai, automation]
- 标题：产品自动化分类功能灵感
- 存储：`memory/just-note/2026-03/2026-03-26-120000.md`

**再试一笔支出**：

```
花了 200 块买书
```

AI 自动处理：
- 类型：expense
- 金额：200
- 标签：[book, learning]
- 标题：买书支出¥200

### 方式 2：CLI 命令（调试用）

**明确指定参数，CLI 直接执行**：

```bash
just-note write --type expense --amount 200 --tags "book,learning" --content "买书"
```

**查看今日记录**：

```bash
just-note today
```

输出：
```
## 2026-03-26 今日记录

共 5 条记录：
- inspiration: 2 条
- expense: 1 条 (¥200)
- task: 1 条
- diary: 1 条

[详细列表...]
```

### 检索历史记录

按关键词：
```bash
just-note search "产品"
```

按类型：
```bash
just-note list --type expense
```

按日期范围：
```bash
just-note list --from 2026-03-01 --to 2026-03-31
```

## 笔记格式标准

采用 memory-notes 格式，支持知识图谱：

```markdown
---
title: "AI 生成的标题"
type: inspiration  # 9 类之一
created: 2026-03-26T12:00:00+08:00
day-id: 2026-03-26  # 用于按天聚合
tags: [tag1, tag2, tag3]
amount: 200  # 可选，收支类型时有
currency: CNY  # 可选
source: wechat  # wechat/feishu/voice/image
---

# AI 生成的标题

## 原始内容
用户发送的原始消息内容...

## AI 整理
- [insight] AI 提取的核心观点 1
- [insight] AI 提取的核心观点 2
- [meta] 金额：¥200（如果是收支类型）

## 关联笔记
- relates_to [[相关笔记标题]]
```

## 目录结构

```
memory/just-note/
├── 2026-03/
│   ├── 2026-03-26-120000.md
│   ├── 2026-03-26-140000.md
│   └── ...
├── 2026-04/
│   └── ...
└── index.json  # 可选，加速检索
```

## 命令参考

### 记录类

| 命令 | 说明 |
|------|------|
| `just-note record "内容"` | 手动记录一条 |
| `just-note quick "内容"` | 快速记录（最小化处理） |

### 查询类

| 命令 | 说明 |
|------|------|
| `just-note today` | 查看今日记录 |
| `just-note yesterday` | 查看昨日记录 |
| `just-note list` | 列出所有记录 |
| `just-note list --type <type>` | 按类型筛选 |
| `just-note list --from <date> --to <date>` | 按日期范围 |
| `just-note search "<keyword>"` | 关键词搜索 |
| `just-note diary --date <date>` | 日记视图（按天聚合） |

### 统计类

| 命令 | 说明 |
|------|------|
| `just-note stats` | 总体统计 |
| `just-note stats --type expense` | 按类型统计 |
| `just-note weekly` | 本周统计 |
| `just-note monthly` | 本月统计 |

### 导出类

| 命令 | 说明 |
|------|------|
| `just-note export --format flomo` | 导出为 flomo 格式 |
| `just-note export --format obsidian` | 导出为 Obsidian 格式 |
| `just-note export --format excel` | 导出为 Excel（收支专用） |

## AI 分类实现

### 核心理念：AI 做大脑，CLI 做手脚

| 角色 | 职责 | 特点 |
|------|------|------|
| **AI（我）** | 理解、分类、推理、生成标签 | 有"大脑"，会思考 |
| **CLI** | 执行明确指令、写入文件 | 无"大脑"，纯工具 |

### 工作流程

#### 消息模式（主要）

```
用户微信消息
    ↓
OpenClaw Gateway 接收
    ↓
AI（我）理解内容 → 自动分类、生成标签、提取金额
    ↓
AI 调用 CLI：just-note write --type xxx --tags xxx ...
    ↓
CLI 执行写入 → 文件保存
```

**关键**：AI 负责理解，CLI 负责执行。

#### CLI 模式（备用）

```
用户明确参数：just-note write --type expense --amount 200 ...
    ↓
CLI 直接执行 → 文件保存
    ↓
不做任何分类/理解
```

**关键**：CLI 不做思考，只执行明确指令。

### 为什么这样设计？

1. **效率最高** - AI 做擅长的事（理解），CLI 做擅长的事（执行）
2. **职责清晰** - AI 有"大脑"，CLI 是"手脚"
3. **符合直觉** - 用户发消息 = 让 AI 处理；用 CLI = 自己明确指定

**Prompt 模板**:
```
你是一个知识记录分类助手。请分析用户输入的内容，完成以下任务：

1. 识别内容类型（9 选 1）：
   - inspiration: 灵感、创意、想法
   - idea: 想法、读书心得
   - knowledge: 知识点、解释
   - expense: 支出记录
   - income: 收入记录
   - diary: 日记、感受
   - task: 待办事项
   - quote: 引用、名人名言
   - other: 其他无法分类的内容

2. 生成 3-5 个标签（简洁、有意义）

3. 生成一个简洁的标题（10-20 字）

4. 如果是收支类型，提取金额和货币单位

5. 提取 1-3 个核心观点/事实（用于 Observations）

输出 JSON 格式：
{
  "type": "inspiration",
  "title": "标题",
  "tags": ["tag1", "tag2", "tag3"],
  "amount": null,
  "currency": null,
  "observations": ["观点 1", "观点 2"]
}
```

## 实现细节

### 1. 消息接收

通过 OpenClaw Gateway 接收微信/飞书消息：

```javascript
// 伪代码
onMessage(async (message) => {
  if (message.source === 'wechat' || message.source === 'feishu') {
    await processRecord(message.content, message.source);
  }
});
```

### 2. AI 分类

调用 LLM 进行自动分类：

```bash
# 伪代码
ai_classify() {
  content="$1"
  prompt=$(cat <<EOF
[分类 Prompt 见上方]
用户输入：$content
EOF
)
  response=$(call_llm "$prompt")
  echo "$response"
}
```

### 3. 文件写入

生成 Markdown 文件：

```bash
write_note() {
  type="$1"
  title="$2"
  content="$3"
  tags="$4"
  observations="$5"
  
  timestamp=$(date +%Y-%m-%d-%H%M%S)
  month=$(date +%Y-%m)
  file="memory/just-note/$month/$timestamp.md"
  
  cat > "$file" <<EOF
---
title: "$title"
type: $type
created: $(date -Iseconds)
day-id: $(date +%Y-%m-%d)
tags: [$tags]
source: $SOURCE
---

# $title

## 原始内容
$content

## AI 整理
$(format_observations "$observations")

## 关联笔记
$(format_relations "$relations")
EOF
}
```

### 4. 检索实现

关键词搜索：

```bash
search_notes() {
  keyword="$1"
  grep -r "$keyword" memory/just-note/ --include="*.md"
}
```

按类型筛选：

```bash
list_by_type() {
  type="$1"
  grep -l "^type: $type$" memory/just-note/*/*.md
}
```

### 5. 日记视图

按天聚合：

```bash
diary_view() {
  date="$1"
  echo "# $date 日记"
  echo ""
  echo "## 今日概览"
  
  count=$(grep -l "^day-id: $date$" memory/just-note/*/*.md | wc -l)
  echo "共 $count 条记录"
  
  # 按类型统计
  for type in inspiration idea knowledge expense income diary task quote other; do
    type_count=$(grep -l "^type: $type$" memory/just-note/*/*.md | grep "$date" | wc -l)
    if [ $type_count -gt 0 ]; then
      echo "- $type: $type_count 条"
    fi
  done
  
  echo ""
  echo "## 详细记录"
  grep -l "^day-id: $date$" memory/just-note/*/*.md | while read file; do
    cat "$file"
    echo ""
    echo "---"
    echo ""
  done
}
```

## 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `JUST_NOTE_STORAGE` | 存储路径 | `memory/just-note` |
| `JUST_NOTE_LLM_MODEL` | LLM 模型 | `qwen3.5-plus` |
| `JUST_NOTE_AUTO_TAG` | 是否自动标签 | `true` |
| `JUST_NOTE_AUTO_RELATE` | 是否自动关联 | `true` |

### 配置文件

`~/.just-note/config.yaml`:

```yaml
storage: memory/just-note
llm:
  model: qwen3.5-plus
  temperature: 0.3
features:
  auto_tag: true
  auto_relate: true
  daily_summary: true
  weekly_report: true
notifications:
  daily_summary_time: "21:00"
  weekly_report_time: "Sunday 20:00"
```

## 最佳实践

### 1. 记录技巧

- **简短为好** - 一条记录 1-3 句话最佳
- **及时记录** - 灵感来了立刻记
- **不用整理** - AI 会自动分类标签
- **定期回顾** - 每周/每月查看汇总

### 2. 检索技巧

- **用标签搜** - `just-note search "#product"`
- **按类型筛** - `just-note list --type expense`
- **按日期找** - `just-note diary --date 2026-03-26`

### 3. 复盘技巧

- **每日回顾** - 睡前查看今日记录
- **每周汇总** - 周末查看周报
- **每月总结** - 月末查看月报

## 与 flomo 对比

| 维度 | flomo | just-note |
|------|-------|-----------|
| 输入方式 | 微信/APP | 微信/飞书 |
| 整理方式 | 手动标签 | AI 自动分类 |
| 内容类型 | 通用笔记 | 9 类（含收支） |
| 数据位置 | 云端 | 本地 + 云端可选 |
| 检索方式 | 标签 + 关键词 | 关键词 + 类型 + 语义 |
| 复盘功能 | 每日回顾 | 每日/每周/每月 AI 总结 |
| 收支统计 | ❌ | ✅ |
| 价格 | ¥12/月 | 免费 |

## 未来规划

### 阶段 1（MVP）- 1-2 周

- [x] 核心记录功能
- [x] AI 自动分类
- [x] 基础检索
- [ ] 每日汇总

### 阶段 2（增强）- 2-4 周

- [ ] 语义检索
- [ ] 智能关联
- [ ] 收支统计图表
- [ ] 导出功能

### 阶段 3（产品化）- 1-2 月

- [ ] Web 界面
- [ ] 多端同步
- [ ] API 开放
- [ ] 插件系统

## 常见问题

### Q: 和 flomo 比有什么优势？

A: 
1. AI 自动分类，不用手动标签
2. 支持收支记录和统计
3. 数据存储在本地，完全自主
4. 免费开源

### Q: 数据会丢失吗？

A: 
- 数据存储在本地 `memory/just-note/` 目录
- 建议定期 Git 备份或同步到云端
- 可以导出为 flomo/Obsidian 格式

### Q: 分类不准确怎么办？

A: 
- 可以手动修改笔记的 `type` 字段
- 分类准确率会随着使用提升
- 欢迎反馈改进建议

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 PR！

GitHub: https://github.com/your-org/just-note
