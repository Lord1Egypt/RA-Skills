---
name: writing-proofreading
description: Use when user wants to review, polish, or proofread articles. Triggers include「帮我改文章」「检查一下」「润色」「帮我改改」「校对一下」「看看文章」.
metadata: {"openclaw":{"emoji":"✏️","requires":{"anyBins":["markdownlint-cli2"]}}}
---

# Writing Proofreading

文章审校助手，提供 6 步审校流程，帮助打磨中文文章。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| markdownlint-cli2 | cli | No | `npx markdownlint-cli2` (no install needed, used in step 6) |
| markdown-lint | skill | No | Included in `npx skills add niracler/skill` (for repo setup) |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

## 核心原则

| 原则 | 说明 |
|------|------|
| **先讨论再修改** | 提出方案让用户选择，不直接动手 |
| **分段审校** | 按 Markdown 标题为节点，每次 1-2 个标题 |
| **启发式提问** | 对草稿内容用提问引导，不替用户决定 |

## 6 步审校流程

```text
1. 结构诊断 → 2. 读者 Context → 3. 语言规范 → 4. 信源查证 → 5. 风格检查 → 6. Markdown 格式
```

### 步骤 1: 结构诊断

**目标**：确保文章结构清晰、主题明确

- 拆解段落，识别主题
- 提出 2-3 个重组方案，**先讨论再修改**
- 删除内容移到「素材.md」保留

详见 [structure-review.md](references/structure-review.md)

### 步骤 2: 读者 Context 检查

**核心问题**：「读者看这里会不会不明所以？」

| 检查项 | 问题表现 | 改进方式 |
|--------|----------|----------|
| 背景假设 | 直接使用专有名词、缩写 | 补充解释或脚注 |
| 自说自话 | 「就是那种...」但没说清楚 | 具体化描述 |
| 跳跃逻辑 | 从 A 直接到 C | 补充过渡说明 |
| 隐含情绪 | 「实在是太...」但没铺垫 | 先铺垫原因 |
| 信息差 | 假设读者知道来龙去脉 | 简要交代背景 |

详见 [structure-review.md](references/structure-review.md)

### 步骤 3: 语言规范

基于余光中《怎样改进英式中文》：

| 问题 | 示例 |
|------|------|
| 抽象名词做主语 | ❌ 收入减少改变生活 → ✅ 他因收入减少而改变生活 |
| 冗赘句式 | ❌ 基于这个原因 → ✅ 因此 |
| 动词弱化 | ❌ 作出贡献 → ✅ 贡献 |
| 介词/连接词堆砌 | 减少「有关」「和」「以及」 |
| 被动语态滥用 | ❌ 问题被解决了 → ✅ 问题解决了 |

详见 [chinese-style.md](references/chinese-style.md)

### 步骤 4: 信源查证

**信源优先级**：政府官方 > 权威媒体 > 行业媒体 > 避免个人博客

数据使用原则：

- 不能只扔数据，要融入体验
- 体感判断需要脚注支撑推算逻辑
- 科普精简，详细放脚注

**工作节奏**：查一个 → 讨论 → 写一个 → 确认 → 下一个

详见 [source-verification.md](references/source-verification.md)

### 步骤 5: 风格一致性

检查是否符合个人写作风格：

| 检查项 | 说明 |
|--------|------|
| 标志性表达 | 「怎么说呢」「其实」「有点...」 |
| 语气特征 | 自嘲式开场、括号补充吐槽 |
| 量化习惯 | 用具体数字增强说服力 |
| 加粗克制 | 每标题下 ≤ 3 处 |

**避免**：

- 「不是……而是……」句型（AI 味）
- 加引号的「幽默」比喻
- emoji 或序号开头
- 频繁使用破折号

详见 [personal-style.md](references/personal-style.md)

### 步骤 6: Markdown 格式化

自动化格式检查（需仓库已配置 markdown-lint skill）：

```bash
npx markdownlint-cli2 article.md          # 检查
npx markdownlint-cli2 --fix article.md    # 自动修复
```

> 仓库未配置？使用 markdown-lint skill 完成初始化。

自动化工具无法覆盖的内容审查：

- 标题层级是否合理（H2→H3，不跳级）
- 列表格式是否一致（全用 `-` 或全用 `*`）
- 代码块是否正确标记语言

## Review 节奏

```text
┌─────────────────────────────────────────────────┐
│  每个标题下的审校流程                             │
│                                                 │
│  1. 读取当前段落                                 │
│  2. 按 6 步流程检查                              │
│  3. 提出修改建议（不直接改）                      │
│  4. 等待用户确认                                 │
│  5. 确认后再处理下一个标题                        │
└─────────────────────────────────────────────────┘
```

**关键**：每段 review 后等待确认，不连续处理多个段落。

## 写作风格速查

| 要素 | 要求 |
|------|------|
| 语言 | 口语化，像和朋友聊天 |
| 段落 | 一个段落一个主题 |
| 加粗 | 只在重要转折/感悟处使用，每标题下 ≤ 3 处 |
| 数据 | 融入体验，脚注放详细来源 |
| 坦诚 | 承认不足、标注未完成，保留思考痕迹 |

## 详细参考

- [chinese-style.md](references/chinese-style.md) - 中文语言规范
- [structure-review.md](references/structure-review.md) - 结构诊断与读者 Context
- [source-verification.md](references/source-verification.md) - 信源查证与脚注
- [personal-style.md](references/personal-style.md) - 个人风格指南
