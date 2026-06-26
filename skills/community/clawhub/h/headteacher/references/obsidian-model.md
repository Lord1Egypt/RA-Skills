# Obsidian Model

Obsidian is a v1 local-first placeholder backend.

## What v1 supports

- folder scaffolding
- markdown templates
- schema documentation
- local artifact indexing guidance

## External prerequisite

This repository does not ship Obsidian connectivity itself.

Before using the Obsidian path, the user should:

- install the Obsidian CLI locally
- keep Obsidian available if the CLI requires a running app
- install or enable the official Obsidian-related skill in the agent environment when needed

If these prerequisites are missing, the skill should stop at installation or verification guidance.

## What v1 does not promise

- full structured database behavior
- full parity with Feishu Base relations and views
- automated dashboards

## Suggested vault structure

```text
班主任工作台/
├── 00-配置/
├── 01-学生主档/
├── 02-考试批次/
├── 03-成绩明细/
├── 04-成长事件/
├── 05-家校沟通/
├── 06-班级安排/
└── 07-产物索引/
```

## Adapter stance

If the user chooses Obsidian in v1:

- generate folders and markdown templates
- emit a schema mapping
- treat Obsidian CLI and the official Obsidian skill as external prerequisites
- explain that this is a local knowledge-workbench mode, not a full structured runtime backend
