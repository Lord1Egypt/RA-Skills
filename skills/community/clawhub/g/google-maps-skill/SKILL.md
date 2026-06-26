---
name: gmaps
description: 通过脚本直连 Google Maps Platform API 完成地理编码、逆地理编码、路线规划、地点搜索、地点详情、海拔查询和时区查询。用户要求"Google Maps 查询""国际路线规划""地点搜索"或需要用命令行脚本调用 Google Maps API 时使用。
---

# Google Maps Skill

## Quick Start
1. Ensure `GOOGLE_MAPS_API_KEY` is set.
2. Run `bun scripts/gmaps.ts --help` in this skill directory.
3. Pick the matching command from `references/command-map.md`.

## Workflow
1. Validate user intent and select one command.
2. Coordinates use **lat,lng** order (Google convention).
3. Keep output as raw Google Maps JSON without wrapping fields.
4. Treat any API business error as failure.

## Commands
- Full command mapping: `references/command-map.md`
- Ready-to-run examples: `references/examples.md`

## Notes
- This skill is script-first and does not run an MCP server.
- Only `GOOGLE_MAPS_API_KEY` is supported.
