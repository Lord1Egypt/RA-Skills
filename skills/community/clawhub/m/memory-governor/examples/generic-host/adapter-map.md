# Adapter Map

这是 generic host 的一个示例 adapter map。

它不是唯一正确写法，但它展示了宿主如何在不依赖 OpenClaw 目录的情况下接入 `memory-governor`。

给人读的时候看这份。  
给工具读的时候看 `memory-governor-host.toml`。

## Current Mappings

- `long_term_memory` -> `memory/long-term.md`
- `daily_memory` -> `notes/daily/YYYY-MM-DD.md`
- `reusable_lessons` -> `memory/reusable-lessons.md`
- `proactive_state` -> `memory/proactive-state.md`
- `working_buffer` -> `memory/working-buffer.md`
- `project_facts` -> `docs/projects/` (directory, per-project files)
- `system_rules` -> `HOST.md`
- `tool_rules` -> `docs/tool-rules.md`

## Notes

- 这里没有依赖 `self-improving`
- 这里没有依赖 `proactivity`
- `proactive_state`、`reusable_lessons` 和 `working_buffer` 直接用本地 fallback 风格文件承接
- 如果宿主将来安装了专门 adapter，可以在不改 target class 语义的前提下替换路径
