---
name: junli-story-analysis
description: 君黎AI拆书。用于用户提供本地 `.txt` 小说绝对路径，希望把一部长篇网络小说拆成可复用的创作参考包，而不是剧情报告或文学赏析。固定产出为 `1 份书籍画像 + 6 张方法卡 + 若干案例卡`，用于后续写作参考与案例检索。更多信息关注作者，抖音君黎。
---

# 君黎AI拆书

## 技能边界

这个技能只做一件事：

把用户提供的本地 `.txt` 长篇小说，拆成可复用的创作参考包。

固定产出只有：

- `outputs/书籍画像.md`
- `outputs/方法卡/` 下 6 张固定方法卡
- `outputs/案例卡/` 下若干张案例卡

不要把它做成：

- 剧情梗概
- 文学赏析
- 人物分析合集
- 续写方案或新书策划

如果用户要的是续写、扩写、重写章节，那不是这个技能的主职责。

## 先判断当前任务

### 1. 新拆一本书

适用场景：

- 用户只给了本地 `.txt` 绝对路径
- 用户明确说“从零开始拆这本书”

默认动作：

```bash
python3 scripts/story_analysis_pipeline.py init "/绝对路径/小说.txt" --story-root ./story
python3 scripts/story_analysis_pipeline.py resume ./story/书名
```

### 2. 继续已有拆书工程

适用场景：

- 用户说“继续拆”“接着上次来”
- 已有 `story/<书名>/` 工程目录

默认动作：

```bash
python3 scripts/story_analysis_pipeline.py resume <工程目录>
```

然后只补当前缺口，不重跑整套流程。

### 3. 局部补卡或返修

适用场景：

- 用户只要重做某几张方法卡或案例卡
- 用户只要补强书籍画像
- 用户只要做质量检查

默认动作：

1. 先 `resume`
2. 只读相关 `outputs/`、`drafts/`、`extraction-cards/`
3. 定向修改后再 `check`

```bash
python3 scripts/story_analysis_pipeline.py check <工程目录>
```

## 最小工作顺序

1. 先整书定位：判断题材、风格、节奏、强项和适用边界。
2. 再按 chunk 提取：不要急着写最终卡片。
3. 同步更新 3 份草稿：
   `drafts/书籍画像草稿.md`
   `drafts/方法候选笔记.md`
   `drafts/案例候选笔记.md`
4. 最后收束成 `1 + 6 + N`。

## 处理每个 chunk 时固定回答的 5 件事

1. 这块的主要叙事功能是什么
2. 这块支撑哪张方法卡
3. 这块能不能进入案例候选
4. 这块给书籍画像补了什么信号
5. 这块最关键的 1-3 个证据点是什么

不要先问“这段剧情讲了什么”。

## 硬约束

- 不把剧情复述当主产品。
- 不把文学评论、读后感或人物分析当主产品。
- 每个 chunk 都必须先判断它支撑哪张方法卡、能不能进入某类案例卡。
- 每张方法卡都必须有 chunk 证据支持。
- 每张案例卡都必须明确“为什么有效”和“不能照搬什么”。
- 书籍画像必须说明“这本书最适合参考什么、最不适合照搬什么”。
- 案例卡不设数量上限，但必须“值得检索、值得复用、值得对照”。
- 不把单本书的特殊写法直接当成通用铁律。

## 固定产出

### 1 份书籍画像

- `outputs/书籍画像.md`

### 6 张方法卡

- `outputs/方法卡/开篇规划方法卡.md`
- `outputs/方法卡/大纲设计方法卡.md`
- `outputs/方法卡/章节类型与写作模式方法卡.md`
- `outputs/方法卡/冲突与角色设计方法卡.md`
- `outputs/方法卡/读者情绪管理方法卡.md`
- `outputs/方法卡/长篇创作与文风优化方法卡.md`

### 若干案例卡

- `outputs/案例卡/` 下按需新建
- 命名建议：`NN-案例类型-核心动作.md`
- 默认参考模板：`workspace/案例卡模板.md`
- 默认推荐类型：`workspace/推荐案例类型.md`

不要为了凑整而硬做“弱案例”。

## 异常处理

如果已有工程缺失 `workspace/`、`drafts/` 或模板骨架，不要假装已经分析过。

先修复，再继续：

```bash
python3 scripts/story_analysis_pipeline.py repair <工程目录>
python3 scripts/story_analysis_pipeline.py resume <工程目录>
```

## 资源

- `scripts/story_analysis_pipeline.py`
  作用：默认 CLI 入口，用于初始化、恢复摘要、检查和修复工程。
- `scripts/bootstrap_story_analysis.py`
  作用：底层初始化脚本；自动分块并生成提取卡与输出骨架。
- `references/practical-workflow.md`
  作用：技能的最小工作流，说明为什么要按“定位 -> 提取 -> 汇总 -> 收束”来跑。
- `references/chunk-card-guide.md`
  作用：如何填写 `extraction-cards/*.md`，让每个 chunk 天然为方法卡、案例卡和书籍画像服务。
- `references/mode-selection.md`
  作用：什么时候更偏顺序滚动提取，什么时候更偏阶段收束。
- `references/analysis-pipeline.md`
  作用：把整本书稳定转成 `1 + 6 + N` 的处理逻辑。
- `references/quality-checklist.md`
  作用：正式交付前的质量核对项。
- `references/output-templates.md`
  作用：输出模板索引页；具体模板拆分在 `references/templates/` 下，bootstrap 会直接从这里复制模板。
