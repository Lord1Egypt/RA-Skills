# Integration Checklist

## 目标

让新接入的 skill 能稳定服从 `memory-governor`，并在 optional skill 缺失时优雅降级。

## 接入检查表

- 这个 skill 会不会写入某种“记忆”？
- 如果会，它产出的信息属于哪些 memory types？
- 这些 memory types 对应哪些 target classes？
- 当前环境优先使用哪个 adapter？
- 如果 adapter 不存在，fallback 去哪里？
- 宿主是否已经用 `memory-governor-host.toml` 显式声明 adapter map？
- 如果 `reusable_lessons` 不是单文件，它是 `directory` 还是 `pattern`，这个 mode 是否已显式声明？
- 如果是 stateful target，它应该 append、replace 还是 merge？
- 如果多个 skill 会写同一 target，谁是 canonical writer？
- 如果宿主想做自动化校验，是否采用结构化 frontmatter？
- 哪些内容只能短存，不能直接进长期层？
- 哪些内容命中排除规则？
- 这个 skill 是否错误地把下游沉淀规则当成全局记忆规则？

## 最小接入要求

每个接入的 skill 至少要补清楚：

1. `This skill follows memory-governor`
2. 典型输出映射
3. 明确约束
4. optional adapter 缺失时的 fallback 行为
5. stateful target 的写入语义
6. 如果宿主支持 manifest，当前 skill 的 target class 是否和宿主 manifest 一致

## Optional Skill 检查

如果某个 skill 依赖这些可选能力：

- `self-improving`
- `proactivity`
- 其他未来插件

需要明确：

- 是否为 hard dependency
- 如果缺失，是否有 fallback
- 如果没有 fallback，是否只降级某个能力，而不是破坏整个内核
- 如果宿主有 manifest，这些 adapter 是否被显式声明，而不是只靠文档约定

## 常见错误

- 直接把 `~/self-improving/...` 当成内核定义
- 直接把 `~/proactivity/...` 当成唯一状态记忆路径
- 直接把 Notion / Obsidian 目录当成全局记忆层
- 只写“落到哪里”，不写“它属于什么 target class”
- 宿主已经换了 adapter，但 `memory-governor-host.toml` 还停在旧映射
- 没装 optional skill 时，整个 memory contract 失效
