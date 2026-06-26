# Notion Model

Notion is a v1 placeholder backend.

## What v1 supports

- explaining the unified schema in Notion terms
- generating a database plan
- generating minimal setup instructions
- optionally creating a lightweight workspace skeleton if the agent has Notion access

## External prerequisite

This repository does not ship Notion connectivity itself.

Before using the Notion path, the user should:

- connect Notion MCP in their agent environment
- verify that Notion tools are actually available in the session

If Notion MCP is not connected, the skill should stop at installation or verification guidance rather than pretending Notion is ready.

## What v1 does not promise

- full runtime parity with Feishu Base
- automatic dashboards
- full artifact registration and sync automation

## Suggested Notion layout

- `班级配置` database
- `学生主档` database
- `考试批次` database
- `成绩明细` database
- `成长事件` database
- `家校沟通` database
- `产物索引` database
- one overview page linking the databases

## Adapter stance

If the user chooses Notion in v1:

- state that it is a planning-first adapter
- generate the mapping cleanly
- treat Notion MCP as a prerequisite that must already exist outside this repo
- do not claim a fully automated runtime
