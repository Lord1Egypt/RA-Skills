# Migration Guide

## Goal

把一个已经有散乱记忆习惯的宿主，逐步收敛到 `memory-governor`，而不是一次性重写整个系统。

这个 guide 假设宿主已经存在：

- 多个记忆文件
- 多个会写记忆的 skill
- 一些隐性规则和口头习惯

## Migration Principle

不要先迁数据。  
先统一 contract，再逐步统一入口和适配层。

顺序建议：

1. clarify
2. declare
3. validate
4. tighten
5. migrate only if needed

## Phase 1: Clarify

先回答这些问题：

- 当前有哪些地方在存“记忆”？
- 哪些属于事实 continuity？
- 哪些属于 reusable lessons？
- 哪些属于 current state？
- 哪些其实是噪声、日志或短期痕迹？

这一步的目标不是改文件，而是把现状映射到 `memory-governor` target classes。

## Phase 2: Declare

先声明宿主 contract，而不是先重构目录。

建议最小动作：

1. 安装 `memory-governor`
2. 在宿主入口承认它是上位治理规则
3. 添加 `memory-governor-host.toml`
4. 把现有路径先按 target class 声明进去

即使旧 adapter 仍然是 legacy 文件，也先声明：

```toml
[targets.reusable_lessons]
mode = "single"
paths = ["~/self-improving/memory.md"]
structured = false
```

先让宿主进入 `Integrated`，再追求更整齐的结构化形态。

## Phase 3: Validate

运行：

- `scripts/check-memory-host.py`
- `scripts/validate-memory-frontmatter.py`（仅针对结构化 fallback）

这一步的目标是确认：

- 宿主是否真的接上了
- 哪些 target 仍然只是 legacy adapter
- 哪些 fallback 已经能被工具稳定校验
- 宿主入口和 writer skill contract 是否已声明并存在

## Phase 4: Tighten

这一步开始减少规则分叉。

优先做这些：

- 清理宿主入口里和 `memory-governor` 重复的路由规则
- 给会写记忆的 skill 补 `Memory Contract`
- 把“路径即规则”的老说法，改成 “target class -> adapter”

这一步的目标是减少“文档打架”。

## Phase 5: Migrate Only If Needed

只有在这些情况，才值得迁移已有数据或 adapter：

- 当前路径已经让读取恢复很困难
- 多个 writer 持续互相覆盖
- 你需要 machine-checkable schema
- 你要把这套宿主对外分发

如果当前旧路径还能稳定工作，不必为了“形式统一”强行迁移。

## Recommended Migration Order

一般建议：

1. `system_rules`
2. `reusable_lessons`
3. `proactive_state`
4. `working_buffer`
5. 其他 target classes

原因：

- 先统一规则入口，能减少后续漂移
- 再统一最容易产生复利和混乱的两层
- 最后再处理更边缘的 target

## Common Mistakes

- 一上来就重写所有记忆文件
- 先迁数据，再补 contract
- 把 optional adapter 当成内核定义
- 为了结构漂亮，强行拆分原本工作正常的 legacy files
- 没跑 checker 就宣布迁移完成

## Success Criteria

宿主可以认为完成了有效迁移，当这些条件成立：

- 宿主入口明确服从 `memory-governor`
- `memory-governor-host.toml` 已声明 target classes
- checker 通过
- skill 不再各自发明记忆定义
- 旧规则不再和内核规则打架
