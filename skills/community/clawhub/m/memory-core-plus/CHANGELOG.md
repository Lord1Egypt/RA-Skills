# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-03-14

### Changed

- **Breaking:** `autoRecall` now defaults to `true`. Auto-recall is enabled out of the box when the plugin is activated. To disable, set `autoRecall: false` or run `openclaw config set plugins.entries.memory-core-plus.config.autoRecall false`.
- **Breaking:** `autoCapture` now defaults to `true`. Auto-capture is enabled out of the box when the plugin is activated. To disable, set `autoCapture: false` or run `openclaw config set plugins.entries.memory-core-plus.config.autoCapture false`.

### Removed

- Removed `autoRecallMinScore` configuration option. Score filtering is now handled entirely by the search manager.

## [0.1.1] - 2026-03-13

### Changed

- Improved npm discoverability: added keywords `llm`, `ai-agent`, `rag`, `ai-gateway`, `typescript`.
- Added GitHub repository topics for better search visibility.

### Docs

- Enhanced README with Mermaid flowcharts, processing steps explanation, slots config, and CLI commands.
- Changed `autoRecallMinScore` default from `0.3` to `0.7` in docs examples.

## [0.1.0] - 2026-03-13

### Added

- **Auto-Recall**: Semantically searches workspace memory before each LLM turn and injects relevant memories into the prompt context via the `before_prompt_build` hook.
- **Auto-Capture**: Automatically extracts durable facts, preferences, and decisions from conversations after each agent run via the `agent_end` hook.
- Configurable similarity threshold and maximum recalled memories per turn.
- Safety guardrails: prompt injection detection, recursion guard, and HTML escaping.
- Full configuration via `openclaw.json` under the `memory-core-plus` key.
- English and Chinese (Simplified) documentation.
