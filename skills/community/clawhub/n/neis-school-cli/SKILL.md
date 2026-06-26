---
name: neis-school-cli
description: Query Korean school information, meals, and timetables from the official NEIS OpenAPI. Use when the user asks for school lunch menus, school timetables, or school code lookup in Korea. Prefer --json output when another agent or tool will consume the result.
---

# NEIS School CLI

Use this skill when the user wants:
- 학교명으로 학교 코드 찾기
- 학교 급식 조회
- 학교 시간표 조회
- NEIS OpenAPI 기반 CLI 사용

## Requirements

- `python3`
- Optional: `NEIS_API_KEY`

## Commands

학교 검색:

```bash
python3 scripts/neis_cli.py school search "세종과학예술영재학교"
```

급식 조회:

```bash
python3 scripts/neis_cli.py meal --school "늘봄초등학교" --date 2026-03-16
```

시간표 조회:

```bash
python3 scripts/neis_cli.py timetable --school "세종과학예술영재학교" --date 2026-03-16 --grade 1 --classroom 1
```

## Notes

- Use `--json` when another agent, script, or UI will consume the result.
- JSON output includes `ok`, `command`, `endpoint`, `query`, `count`, and `data`.
- Read `references/neis-api.md` only when you need endpoint details or response-shape reminders.
