# insentek-api-skills

This is a GSD-managed project. Use `/gsd-progress` to check status and next steps.

## Project Overview

基于 insentek OpenAPI 工程仓库和接口文档，产出一份通用 `skill.md` 技能文件及配套文档与示例。终端用户可在 OpenClaw、Hermes-Agent、Claude Code、ChatGPT 等 Agent 平台上直接对话使用，通过自然语言调用 insentek API 完成设备数据查询、报告生成与实时分析。

## Quick Links

- Project context: `.planning/PROJECT.md`
- Requirements: `.planning/REQUIREMENTS.md`
- Roadmap: `.planning/ROADMAP.md`
- Current state: `.planning/STATE.md`

## Working with This Project

1. Always read `.planning/STATE.md` first to understand current phase and focus
2. Check `.planning/PROJECT.md` for core value and constraints
3. Follow the roadmap phase order
4. Update STATE.md when phase status changes

## Key Decisions

- Single universal `skill.md` (not per-industry splits)
- Content production project (not a tool/generator)
- Horizontal Layers phase structure
- 1-2 week delivery timeline

## Reference Materials

- API codebase: `ref/api-repo/` (Spring Boot 3.5.4, Java 21)
- API documentation: `ref/api-document-latest.pdf`
