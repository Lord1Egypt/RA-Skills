# Publish Checklist (clawhub)

## Skill Identity

- Folder name and `name` in `SKILL.md` are identical: `pdf-booklet-print-merge`
- Description includes searchable keywords:
  - pdf merge
  - booklet
  - duplex
  - saddle stitch
  - 小册子打印
  - 中缝翻页

## Required Files

- `SKILL.md` exists and has valid YAML frontmatter.
- Script entry file exists: `./scripts/booklet_merge.py`.
- Relative links in `SKILL.md` resolve correctly.

## Runtime Dependency

- Python 3.9+
- `pypdf>=5.4.0,<6`

Install:

```bash
/usr/bin/python3 -m pip install pypdf
```

## Smoke Test

```bash
/usr/bin/python3 ./.claude/skills/pdf-booklet-print-merge/scripts/booklet_merge.py --input-dir data/input
```

Expected:

- booklet file generated at `data/output/booklet_print.pdf`
- optional merged source at `data/output/merged_source.pdf`

## Suggested Search Name

- Display Name: `PDF小册子合并排版（2-up双面中缝打印）`
- Slug Name: `pdf-booklet-print-merge`
