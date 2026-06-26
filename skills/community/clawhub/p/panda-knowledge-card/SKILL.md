---
name: panda-knowledge-card
description: >-
  将知识内容转化为精美的知识卡片图片系列。
  支持从文章自动提取知识点拆分为多张卡片，也支持直接输入知识点生成。
  卡片类型(Layout) × 视觉风格(Style) 二维组合，可选角色融合。
  触发词："知识卡片"、"knowledge card"、"生成卡片"、"知识图"、
  "做成卡片"、"卡片系列"。
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/hash-panda/panda-skills#panda-knowledge-card
---

# 知识卡片生成器

将知识内容转化为视觉化的知识卡片图片系列。支持从文章自动提取知识点拆分，也支持直接输入知识点。可选的卡通角色融合——有角色图片时自然融入卡片画面。

## 两个维度

| 维度 | 控制 | 示例 |
|------|------|------|
| **卡片类型（Layout）** | 信息结构与布局 | 要点清单、对比卡、问答卡、定义卡、步骤卡、矩阵卡 |
| **视觉风格（Style）** | 视觉美学 | 极简手绘、可爱、粉笔画、手写笔记、醒目 |

自由组合：`--layout tips --style notion`

或使用预设：`--preset study-guide` → 类型 + 风格一步到位。详见 [预设快捷方式](references/presets.md)。

## 卡片类型（Layout）

| 类型 | 描述 | 适用内容 |
|------|------|----------|
| `tips`（要点清单） | 编号列表 + 图标，3-7 个要点 | 干货清单、注意事项、必备技能 |
| `comparison`（对比卡） | 左右分栏或上下对比 | 优缺点、新旧对比、A vs B |
| `definition`（定义卡） | 大标题 + 核心解释 + 例子 | 概念科普、术语解释 |
| `steps`（步骤卡） | 编号步骤 + 简要说明 | 教程、操作指南、流程 |
| `qa`（问答卡） | 问题 + 答案结构 | FAQ、常见误区、面试题 |
| `matrix`（矩阵卡） | 2×2 或多格矩阵 | 分类、象限分析、SWOT |
| `quote`（金句卡） | 大字金句 + 出处/解读 | 名言、核心观点、启发 |
| `mindmap`（脑图卡） | 中心主题 + 分支 | 知识脉络、概念关系 |
| `cover`（封面卡） | 系列封面，标题 + 主视觉 | 系列首图 |
| `summary`（总结卡） | 系列收尾，核心回顾 + CTA | 系列末图 |

详见 [references/card-layouts.md](references/card-layouts.md)。

## 风格（Style）

| 风格 | 描述 | 适用场景 |
|------|------|----------|
| `notion`（极简手绘） | Notion 风格简笔画，知性简洁 | 知识分享、效率工具 |
| `study-notes`（手写笔记） | 仿真手写，蓝笔 + 红批注 + 黄荧光笔 | 学习笔记、考试重点 |
| `chalkboard`（粉笔画） | 黑板 + 彩色粉笔 | 课堂笔记、教学 |
| `cute`（可爱） | 甜美柔和、圆润线条 | 生活分享、轻松内容 |
| `bold`（醒目） | 高冲击力、大字体、强对比 | 避坑指南、重要提醒 |
| `warm`（温暖） | 友好亲切、柔和色调 | 个人成长、教育 |
| `vector-illustration`（矢量插画） | 扁平矢量、大胆几何 | 技术内容、教程 |
| `minimal`（极简） | 极致简洁、大量留白 | 哲学、核心概念 |
| `screen-print`（丝网印刷） | 海报艺术、半色调 | 观点、文化评论 |

详见 [references/styles.md](references/styles.md)。

## 使用方式

```bash
# 从文章提取知识点生成卡片系列
/panda-knowledge-card article.md

# 指定风格
/panda-knowledge-card article.md --style notion

# 直接输入知识点
/panda-knowledge-card
[粘贴内容或描述知识点]

# 指定卡片类型 + 风格
/panda-knowledge-card --layout tips --style bold

# 使用预设
/panda-knowledge-card article.md --preset study-guide

# 指定平台
/panda-knowledge-card article.md --platform xhs

# 指定角色模式
/panda-knowledge-card article.md --role narrator
```

## 选项

| 选项 | 描述 |
|------|------|
| `--layout <name>` | 卡片类型（见上表） |
| `--style <name>` | 视觉风格（见上表） |
| `--preset <name>` | 预设快捷方式（见 [presets.md](references/presets.md)） |
| `--platform <name>` | 目标平台：`xhs`(3:4), `wechat`(16:9), `weibo`(16:9), `general`(16:9) |
| `--role <mode>` | 角色融合模式：`auto`, `narrator`, `participant`, `decorator`, `none` |
| `--count <n>` | 卡片数量（默认自动） |
| `--lang <code>` | 卡片语言：`auto`, `zh`, `en` 等 |

## 工作流程

```
- [ ] 步骤 0: 预检查（EXTEND.md、角色配置）
- [ ] 步骤 1: 内容分析（文章提取 或 手动输入）
- [ ] 步骤 2: 确认设置（AskUserQuestion）
- [ ] 步骤 3: 生成大纲
- [ ] 步骤 4: 生成提示词 + 图片
- [ ] 步骤 5: 完成报告
```

### 步骤 0: 预检查

**0.1 加载偏好设置（EXTEND.md）⛔ 阻塞**

```bash
test -f .panda-skills/panda-knowledge-card/EXTEND.md && echo "project"
test -f "${XDG_CONFIG_HOME:-$HOME/.config}/panda-skills/panda-knowledge-card/EXTEND.md" && echo "xdg"
test -f "$HOME/.panda-skills/panda-knowledge-card/EXTEND.md" && echo "user"
```

| 结果 | 操作 |
|------|------|
| 找到 | 读取、解析、显示摘要 |
| 未找到 | ⛔ 运行 [首次配置](references/config/first-time-setup.md) |

**0.2 加载角色配置**

从 EXTEND.md 的"角色"区块读取角色信息。角色融合的详细规则引用 panda-article-illustrator 的 [character-roles.md](../panda-article-illustrator/references/character-roles.md)。

完整流程详见 [references/workflow.md](references/workflow.md#步骤-0-预检查)

### 步骤 1: 内容分析

**文章提取模式**：分析文章，提取核心知识点，自动拆分为卡片序列。详见 [references/extraction-rules.md](references/extraction-rules.md)。

**手动输入模式**：结构化用户提供的知识点，确定适合的卡片类型。

完整流程详见 [references/workflow.md](references/workflow.md#步骤-1-内容分析)

### 步骤 2: 确认设置 ⚠️

**使用 AskUserQuestion，最多 4 个问题。**

| 问题 | 选项 |
|------|------|
| **Q1: 预设或类型** | [推荐预设], [备选预设], 或手动选择卡片类型 |
| **Q2: 风格** | [推荐], notion, cute, bold, chalkboard, study-notes, 其他 |
| **Q3: 张数** | 自动(推荐), 3张, 5张, 7张, 自定义 |
| **Q4: 角色模式** | 自动推荐, 讲解者, 点缀, 无角色 — **仅在有角色配置时显示** |

完整流程详见 [references/workflow.md](references/workflow.md#步骤-2-确认设置-)

### 步骤 3: 生成大纲

保存 `outline.md` 到输出目录，包含每张卡片的标题、要点、布局类型、角色动作。

完整模板详见 [references/workflow.md](references/workflow.md#步骤-3-生成大纲)

### 步骤 4: 生成提示词 + 图片

⛔ **提示词文件必须在图片生成之前保存。**

1. 为每张卡片创建提示词文件，遵循 [references/prompt-construction.md](references/prompt-construction.md)
2. 保存到 `prompts/NN-{layout}-{slug}.md`
3. 有角色时注入角色区块，使用 `--ref` 传递角色参考图
4. 调用图片生成技能生成图片

完整流程详见 [references/workflow.md](references/workflow.md#步骤-4-生成提示词--图片)

### 步骤 5: 完成报告

```
知识卡片生成完成！

主题：[topic]
风格：[style] | 平台：[platform] | 比例：[ratio]
角色：[名称] / [融合模式] 或 "无角色"
卡片：X 张已生成

文件列表：
✓ outline.md
✓ 01-cover-[slug].png
✓ 02-tips-[slug].png
✓ ...
✓ NN-summary-[slug].png
```

## 输出目录

| `默认输出目录` | 输出路径 |
|----------------|----------|
| `knowledge-cards`（默认） | `knowledge-cards/{topic-slug}/` |
| `same-dir` | 当前目录 |
| `imgs-subdir` | `{article-dir}/imgs/` |

```
{output-dir}/
├── source-{slug}.md          # 源内容（如有）
├── outline.md                # 大纲
├── prompts/
│   └── NN-{layout}-{slug}.md
├── 01-cover-{slug}.png
├── 02-{layout}-{slug}.png
└── NN-summary-{slug}.png
```

**Slug 规则**：2-4 个词，kebab-case。**冲突**：追加 `-YYYYMMDD-HHMMSS`。

## 修改已有卡片

| 操作 | 步骤 |
|------|------|
| 编辑 | 更新提示词 → 重新生成 → 更新引用 |
| 添加 | 确定位置 → 创建提示词 → 生成 → 更新大纲 |
| 删除 | 删除文件 → 更新大纲 |

## 参考文档

| 文件 | 内容 |
|------|------|
| [references/workflow.md](references/workflow.md) | 完整工作流程 |
| [references/card-layouts.md](references/card-layouts.md) | 10 种卡片类型详解 |
| [references/extraction-rules.md](references/extraction-rules.md) | 文章知识点提取规则 |
| [references/prompt-construction.md](references/prompt-construction.md) | 提示词构建指南 |
| [references/styles.md](references/styles.md) | 风格体系 |
| [references/presets.md](references/presets.md) | 预设快捷方式 |
| [references/config/first-time-setup.md](references/config/first-time-setup.md) | 首次配置流程 |
| [references/config/preferences-schema.md](references/config/preferences-schema.md) | EXTEND.md schema |
| [角色融合模式](../panda-article-illustrator/references/character-roles.md) | 引用 article-illustrator |
| [角色风格兼容性](../panda-article-illustrator/references/character-style-compat.md) | 引用 article-illustrator |
| [社交平台预设](../panda-article-illustrator/references/platform-presets.md) | 引用 article-illustrator |
