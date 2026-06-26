# OmniSkill 统一聚合技能 - 规格说明书 (Spec)

## 1. 项目目标
通过微内核（Microkernel）与插件化架构，将现有的十几个零散 Skill（如 ai-trace-evader, novel-director 等）整合为单一入口的 `omni-skill`。
所有 Hook 与自然语言请求均指向 `omni-skill`，通过其内部路由分配到对应插件。这极大降低了维护成本，提升了 QPS（>20%）和内存效率（减少 >15%）。

## 2. 核心架构
- **MicroKernel (`src/core/kernel.py`)**: 负责系统启动、生命周期钩子（on_init, on_start, on_pause, on_destroy）、热加载注册。
- **PluginManager**: 自动扫描并加载 `OmniPlugin` 子类。
- **EventBus**: 基于 `EventType` 的发布订阅模型，用于插件间解耦通信。
- **ConfigManager (`src/core/config.py`)**: 支持 YAML/JSON 及环境变量（`OMNI_`）覆盖。
- **Metrics (`src/core/metrics.py`)**: 提供 Circuit Breaker（熔断）和 Rate Limiter（限流）保障稳定性。

## 3. 旧 SKILL.md 兼容方案
- 旧的各技能文件夹下的 `SKILL.md`（如 `ai-trace-evader/SKILL.md`）已统一提取。
- 提取后的 Prompt/Instruction 存放在 `.trae/skills/omni-skill/prompts/` 目录下，并以 `<plugin_name>.md` 命名。
- 插件在 `on_init` 阶段可读取这些 Markdown，作为执行具体大语言模型任务时的 Prompt Context。
