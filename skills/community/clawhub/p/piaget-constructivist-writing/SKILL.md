---
name: piaget-constructivist-writing
description: 皮亚杰建构主义（constructivism）写作与教学表达工作流。用于把知识点写成“读者可建构理解”的文章/讲义/课程脚本：从旧知出发，制造可控认知冲突，同化/顺应逐步搭建概念结构，输出概念地图、学习路径、分层讲解、练习题、误解纠偏与目标达成评估。
---

# 皮亚杰建构写作：让读者自己“搭起来”

## 触发方式

- 用户说“用建构主义/皮亚杰方式写/面向新手写讲义/想写成循序渐进的科普/老师备课/要从旧知引出新概念”时使用本 Skill。
- 适用：教学讲义、科普文章、知识体系笔记、课程脚本、训练营作业讲解。

## 输入模板（复制填空）

缺信息时先做合理假设，并把假设写入“待确认项”。如果用户只给了 Topic，没有给读者画像，优先问 1-2 个问题补齐。

```text
主题（Topic）：
读者（Audience）：年级/背景/是否完全新手
写作目标（Goal）：理解/能复述/能应用/能迁移
读者旧知锚点（Prior Knowledge）：他们已经会什么/相信什么
常见误解（Misconceptions）：3-5 条（没有就写“未知”）
必须包含/避免（Must include/avoid）：
限制（Constraints）：字数/时长/讲义 or 文章/是否允许公式
```

## Quick Start（开箱即用）

当用户输入不完整时，按顺序补齐并开始产出：

1. 选择场景预设：科普文章 / 课程讲义 / 学习笔记（见 `references/presets.md`）
2. 用 `references/rubric.md` 生成 3-7 条 Success Criteria（成功标准）
3. 若用户想直接测试，提供 `references/sample-requests.md` 的示例输入
4. 读取 `assets/output-template.md` 选择模板：短讲解用 `assets/compact-template.md`；讲义/课程用 `assets/lesson-template.md`
5. 按模板输出，并在最后做“目标达成评估”

## 工作流（建构主义写作）

按顺序执行；除非用户指定输出形式，否则使用“默认输出格式”。

### 1) 建立概念地图（Concept Map）

- 列出 5-10 个核心概念与关系（包含：上位/下位、因果、对比、前置依赖）。
- 选出 1 条“主线因果链/理解链”，后续段落围绕它展开，避免百科式罗列。

### 2) 旧知锚点与认知冲突（Prior Knowledge -> Cognitive Conflict）

- 用读者已有经验作为锚点（他们已懂的类比/直觉/场景）。
- 设计一个“可控冲突”：让旧知解释不了某个现象/题目/反例，从而引出新概念的必要性。
- 冲突必须可验证：用一个小例子或问题触发，而不是纯口号。

### 3) 同化与顺应支架（Scaffolding）

- 同化（Assimilation）：先在旧框架下解释新信息能解释的部分，建立连续性。
- 顺应（Accommodation）：明确指出旧框架的边界，再引入新框架，补齐解释力缺口。
- 每次引入新术语时，给一句话定义 + 一个最小例子（不要一次堆很多术语）。

### 4) 迁移练习（Transfer）

- 提供 3 组练习：`概念辨析`、`应用题`、`迁移题`（从熟悉场景迁移到新场景）。
- 每题都给“为什么这么想”的解题思路，而不是只给答案。

### 5) 误解纠偏（Misconceptions）

- 列出 3-7 条常见误解：误解是什么 -> 为什么容易误解 -> 正确模型是什么 -> 如何自检。
- 需要证据边界时要写清：哪些是普遍结论，哪些取决于条件。

### 6) 目标达成评估（Evaluate Against Goal）

- 对照 Success Criteria 打分并给理由。
- 给出结论：`已达成/部分达成/未达成（需澄清）`。
- 若输出仍显得“像灌输/跳步/术语先行”，读取 `references/anti-patterns.md` 做二次修订后再给最终版。

## 默认输出格式（建议）

- `概念地图`：概念与关系
- `学习路径`：旧知锚点 -> 冲突 -> 新概念 -> 迁移
- `分层讲解`：短讲解 or 讲义结构（按模板）
- `练习题（含思路与答案）`
- `误解纠偏`
- `待确认项`
- `目标达成评估`

## 资源文件（references/ 与 assets/）

- 预设：`references/presets.md`（场景选择与默认结构）
- 评分量表：`references/rubric.md`（Success Criteria 与评估口径）
- 示例输入：`references/sample-requests.md`（复制即用）
- 完成品样张：`references/example-outputs.md`（对齐颗粒度与风格）
- 反模式库：`references/anti-patterns.md`（输出不清楚时用于纠偏）
- 模板索引：`assets/output-template.md`（选择短讲解/讲义模板）
