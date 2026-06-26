# Candidate Review

## Goal

把 `learning_candidates` 从“能先记下来”推进成“能稳定 review、能决定去留”。

这一步仍然属于治理层，不是自动晋升系统。

## Lifecycle

每条 candidate 都建议带一个明确的生命周期阶段：

1. `collecting_evidence`
2. `ready_for_promotion`
3. `promoted`
4. `discarded`

人话就是：

- 先收证据
- 再进入“差不多可以升了”
- 升完后标记 promoted
- 不值得保留就标记 discarded

不要跳过中间判断，直接把“刚出现一次”写成可长期复用的真理。

## Default Review Decisions

每次 review，默认只做三种决定：

1. keep
2. promote
3. discard

不要在 review 阶段偷偷引入更多状态机。

## Keep

适合继续保留在 `learning_candidates` 的情况：

- 只有一次证据
- 还离不开当前案例语境
- 规则表述还不够抽象
- 对未来是否稳定有帮助仍不确定

## Promote

适合从 `learning_candidates` 升到 `reusable_lessons` 的情况：

- 已满足 `correction-pipeline.md` 里的至少两个 promotion signal
- 已能改写成脱离当前案例的通用规则
- 未来再次遇到时，直接复用这条经验比重新判断更便宜

如果要继续升到 `system_rules` / `tool_rules` / `AGENTS` / `TOOLS` / `SOUL`，仍应先经过 `reusable_lessons`，不要跳级。

## Discard

适合直接丢弃的情况：

- 只对一次任务成立
- 其实是项目局部事实，不是可迁移经验
- 信息已经过时
- 候选内容只是原始长日志或 breadcrumb

## Review Rhythm

推荐的 review 节奏：

- task closeout
- 同类纠错第二次出现时
- 准备写入长期规则前
- 候选层超过 7 天未刷新时

## Review Helper

可用这个 helper 做轻量 review：

```bash
python3 scripts/review-learning-candidates.py path/to/learning-candidates.md
```

它会做这些事：

- 先调用 frontmatter validator
- 统计 `## Candidates` 下的 candidate item 数量
- 区分结构化 candidate entry 和旧式简单 bullet
- 检查每个结构化 entry 是否写全 review 需要的字段
- 汇总每个 lifecycle stage 里有多少条 candidate
- 根据 `updated_at` 提醒是否 stale
- 给出 keep / promote / discard review 提示

它不会自动改文件，也不会自动晋升。

## Recommended Entry Shape

推荐每条 candidate 用一个小块来写，而不是只写一句 bullet：

```md
### Candidate: avoid hardening one-off corrections

- summary: single correction should enter the candidate layer first
- why_it_matters: reduces false hardening into durable rules
- promotion_signals: repeated across tasks; user says this should always apply
- lifecycle_stage: collecting_evidence
- evidence_count: 1
- next_review: after the next related correction or at task closeout
```

这样做的好处很直接：

- review 时不需要重新猜这条候选到底想表达什么
- 更容易判断 keep / promote / discard
- 更容易看出它现在到底还在收证据，还是已经准备升格
- stale 候选也更容易快速清理

旧的简单 bullet 仍可保留，但 helper 会提示它们还不够结构化。

## Anti-Patterns

- 用 reviewer 代替人工判断
- reviewer 一报 stale 就直接 promote
- candidate file 长期处于 `promoted` 或 `discarded` 但从不清理
- 把 candidate review helper 包装成隐式安装副作用
