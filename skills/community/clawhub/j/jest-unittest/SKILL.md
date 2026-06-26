---
name: jest-unittest
description: >
  单元测试 Skills 集合。当用户提到单测、单元测试、覆盖率、单测覆盖、单测失败、单测报错、修复单测、补充测试、覆盖率不足、覆盖率100%、运行单测、组件测试等关键词时触发。
  包含三个子技能：unittest-checker（覆盖率检测）、unittest-completer（自动补全测试至100%）、unittest-doctor（诊断并修复单测报错）。
---

# Unit Test System

根据用户意图路由到对应子技能。

## 配置

配置文件按项目隔离，存放在 `.temp/projects/<hash>/` 下（hash 由项目根路径计算）：
- `source.json` — 用户配置的 jest 配置文件路径
- `config.json` — 由 `reload.cjs` 自动生成的完整配置

各子技能的脚本启动时会自动校验配置和环境。如果返回 `error` 字段，根据 `type` 处理：
- `config_error` → 按 `hint` 帮用户配置 `source.json`（路径见错误信息中的 `sourceJsonPath`），执行 `node scripts/reload.cjs` 生成配置，然后重试
- `env_error` → 根据 `error` 信息排查环境问题，解决后重试

用户主动要求 reload 时，直接执行 `node scripts/reload.cjs`。

### 多项目支持

本 skill 支持在多个项目间使用而不产生配置冲突。每个项目的 `source.json` 和 `config.json` 独立存放在 `.temp/projects/<hash>/` 下，切换项目时自动识别。

## 路由规则

| 用户意图 | 路由到 |
|---------|--------|
| 查看覆盖率、检查哪些单测覆盖率未达标、覆盖率报告 | **unittest-checker** |
| 补充测试、让单测覆盖率达到100%、写单测 | **unittest-completer** |
| 单测报错、单测失败、修复单测、诊断单测问题 | **unittest-doctor** |

## 严禁事项

- **严禁手动编辑 `config.json`**，必须通过 `reload.cjs` 生成。
- **严禁修改项目的 jest 配置文件**来适配本 skill。
- **严禁手动运行 jest 命令**来替代脚本，脚本参数由 `config.json` 提供。

## Sub-skills

| Sub-skill | 功能 |
|-----------|------|
| unittest-checker | 运行测试并分析覆盖率，输出未达标组件列表 |
| unittest-completer | 指定组件名，自动补充测试直到四项覆盖率全部100% |
| unittest-doctor | 运行测试，诊断失败和console警告，支持自动修复 |
