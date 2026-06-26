# Generic Host Example

这个目录演示：

> 一个不具备 OpenClaw 目录结构的普通宿主，如何接入 `memory-governor`

它不是 OpenClaw 镜像。

它故意假设宿主只有最基本的能力：

- 一个宿主级说明文件
- 一个 `skills/` 目录
- 一个本地 `memory/` 目录
- 没有 `self-improving`
- 没有 `proactivity`
- 没有 `AGENTS.md`

## What This Example Contains

- `HOST.md`
  宿主级“记忆治理声明”
- `memory-governor-host.toml`
  给 checker 读取的 machine-readable adapter manifest
  现在也声明了 host entry 和 writer contract 路径
- `adapter-map.md`
  这个宿主当前采用的 target class 到路径映射
- `memory/long-term.md`
  `long_term_memory` 的一个宿主级落点示例
- `skills/example-writer/SKILL.md`
  一个接入了 `memory-governor` 的普通 skill 示例
- `memory/learning-candidates.md`
  本地 `learning_candidates` fallback 示例
- `python3 ../scripts/review-learning-candidates.py memory/learning-candidates.md`
  对候选层做轻量 review 检查
- `memory/proactive-state.md`
  本地 `proactive_state` fallback 示例
- `memory/reusable-lessons.md`
  本地 fallback 示例
- `memory/working-buffer.md`
  本地 fallback 示例
- `docs/projects/`
  `project_facts` 落点示例（directory 模式，每个项目一份）
- `docs/tool-rules.md`
  `tool_rules` 落点示例

## What This Example Proves

它证明三件事：

1. 宿主不必长得像 OpenClaw
2. target class 可以映射到宿主自己的目录结构
3. optional skill 缺失时，仍然可以靠 fallback 正常成立

## Suggested Reading Order

1. `HOST.md`
2. `memory-governor-host.toml`
3. `adapter-map.md`
4. `memory/proactive-state.md`
5. `skills/example-writer/SKILL.md`
6. `memory/learning-candidates.md`
7. `memory/reusable-lessons.md`
8. `memory/working-buffer.md`
