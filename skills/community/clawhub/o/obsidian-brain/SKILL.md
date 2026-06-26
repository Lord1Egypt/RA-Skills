---
name: obsidian-brain
description: Agent跨会话记忆——任务前搜agent memory L0→L1→L2分层加载，任务结束LLM提取事实→哈希去重→写入碎片。禁type/[[链接]]/related_fragments
version: 1.7.0
author: Hermes Agent
license: MIT
agent_trigger: 当需要读写跨会话记忆碎片、搜索Obsidian库中已有知识上下文、或任何涉及agent memory文件夹的操作时加载
metadata:
  hermes:
    tags: [obsidian, agent-memory, knowledge-graph, token-saving]
---

# Obsidian Brain — Agent 记忆系统

对话开始搜 agent memory，任务结束写回。读：L0→L1→L2。写：LLM提取→去重→碎片化。

## 碎片格式

文件名：`{项目} - {YYYY-MM-DD} - {描述}.md`

```yaml
---
tags: [agent-memory]
project: 项目名
date: 2026-05-05
summary: 一句话概述（L0扫描用）
importance: 0.8
confidence: 0.9          # 可选
source: conversation     # 可选
---
# 正文（agent压缩格式，见下方规则）
```

**禁写字段：** `type` `related_fragments` `[[链接]]`。碎片纯文本，不属KG图谱。用 `project` 字段分组代替关联。

## 碎片压缩规则

正文以**agent解析效率**为唯一目标，人类可读性忽略。

**格式要求：**
- **正文允许**：事实列表（`- key: value`）、短句（≤2行）、关键数据、显式关系（`→` `⇒` `∵` `∴`）
- **正文禁止**：段落叙事、`## 现象`/`## 根因`/`## 经验教训` 多级标题、过渡句、解释性装饰语
- **不再需要** `# 标题`（文件名已含标识）

**缩写约定**（不产生歧义时使用）：
| 词 | 缩写 |
|:--|:----|
| agent memory → am | kg → kg |
| search_files → sf | read_file → rf |
| write_file → wf | patch → p |
| session → sess | memory → mem |
| 工具混淆 → tool-conf | 缺失 → miss |

**示例**（同一碎片，压缩前后对比）：

❌ 旧格式（人类友好）：
```
# agent-memory 设计 - 2026-05-06 - 读+写双重失效

## 现象
本会话既没读agent memory，也没写agent memory。

## 根因
...

## 经验教训
1. 任何用户输入都是新任务开始
2. system memory 和 agent memory 是两套存储
```

✅ 新格式（agent压缩）：
```
**发现**：本sess既没读am也没写am
**根因-读**：用户发文件名→未触发AGENTS.md步0
**根因-写**：mem-tool满(2093/2200)→误判am也写不了（两者独立）
**教训**：①任意输入=任务开始→必须走步0 ②mem-tool≠am碎→容量不共享 ③📋模板从未加入回复格式
```

## L0/L1/L2 分层

| 层 | 加载内容 | 时机 |
|:--|:-----|:-----|
| L0 | frontmatter: `summary` `tags` `importance` | 搜到即加载 |
| L1 | 正文 | L0确认相关 |
| L2 | 同 project 其他碎片 | L1不够时 `search_files` |

## 写入

**判断（什么该记）：** 决策/结论/价格数据、踩坑教训、调研发现 ✔ | 临时计算、一次性信息 ✘

**流程：** LLM从结果提取关键事实 → 去重（有相似碎片且度>0.8→合并更新）→ 写 `.md`

## 读出

**顺序：** agent memory/ → 知识库skill(agent_trigger) → 概念/某物(abstract) → 网络

**排序：** `相关性×0.5 + importance×0.3 + e^(-0.01×days)×0.2`

## 维护

- `importance<0.3` 且 90天未访问 → `_archive/`
- 同 project 碎片 > 20 → 生成 L2 总结合并

## 执行流程

```
0. ⚠️ 读 agent memory（不可跳过，结果可视化）
   search_files → L0 → 相关则L1 → 注入上下文
   **在回复开头必须报告：** `📖 agent memory：读取 N 个碎片 → [标题+summary → 相关/不相关]`
1~N. 执行任务（中途转向时重搜）
N+1. ⚠️ 写 agent memory + 📋 留位检查（不可跳过）
   三问：决策/结论/发现？踩坑/教训？下次需要？
   任一"是" → 立即写入，同轮次完成。不等不拖。
   末尾加 `📋 agent memory：本次是否有需写入碎片？[有/无]`
N+2. ⚠️ 如果本技能（obsidian-brain）被编辑 → clawhub publish 新版本
```

## 触发约束

- **AGENTS.md**：对话开始强制搜 + 任务结束强制写
- **流程第0步**：任务前必搜，优先于网络/知识库
- **📋 留位**：每次回复末尾检查
- **失效保护**：连续3次漏读/漏写 → 下次加载时回溯

## 速查

```
读: 任务前→搜碎片L0→L1→L2  写: LLM提取→去重→碎片化
禁: type/[[链接]]/related_fragments
排: 0.5×相关+0.3×importance+0.2×时间
维: <0.3且90天→archive   >20碎片→总结
```

## 陷阱

- **忘读** → AGENTS.md 系统约束，不靠自觉
- **忘写** → 三问+同轮次+📋留位
- **碎片写type/[[链接]]/related_fragments** → 禁止。纯文本
- **混淆 system memory 与 agent memory 碎片** → 两者是独立存储。system memory 用 `memory` 工具操作（2200字符上限），agent memory 碎片用 `write_file` 写 Obsidian vault（无上限）。一个满了不影响另一个，不要用一个判断另一个。
- **用户发文件名/单字不算"任务开始"** → 任何用户消息（即使只是一个文件名）都是对话开始信号，必须先执行第0步搜碎片。文件名≠跳过符。
- **混淆 system memory 与 agent memory** → 见 `references/storage-distinction.md`。两者独立存储，容量不共享。看到 memory 满≠agent memory 不能写。
