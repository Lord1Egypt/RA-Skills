---
name: mind-map-skill
description: Generate a PNG mind map from Markdown using free (auto), center, or horizontal layout. Use when user asks to produce a brain map/思维导图 from notes.
argument-hint: "[free|center|horizontal] [markdown_file_or_inline_markdown]"
disable-model-invocation: true
allowed-tools: Bash(python mind_map/scripts/run_mind_map.py *), Read, Write
---

# Mind Map Skill

Generate mind map images locally from Markdown content.

## Invocation

Use this skill directly:

- `/mind-map-skill free docs/plan.md`
- `/mind-map-skill center "# 项目\n## 模块\n- A\n- B"`
- `/mind-map-skill horizontal notes.md`

Arguments are mapped as:

- `$0`: layout type (`free`, `center`, `horizontal`)
- `$1`: markdown file path or inline markdown text

If layout argument is missing, use `free`.

## Execution steps

1. Parse `$ARGUMENTS`.
2. Resolve markdown input:
   - If `$1` is a file path, read file content.
   - Otherwise treat `$1` as inline markdown.
3. Run from repository root (`D:\Work\skills\mind_map`):

```bash
python mind-map-skill/scripts/run_mind_map.py --layout <layout> --input "<file-or-markdown>" --output-dir mind_map_output
```

By default, output files are grouped by date under `mind_map_output/YYYY-MM-DD/`.
Use `--flat-output` to write directly into `mind_map_output/`.

4. Report:
    - selected layout
    - output PNG path
    - input markdown saved path (same dated folder)
    - node count and depth

## Layout behavior

- `center`: radial structure (equivalent to mind_map_center capability)
- `horizontal`: left-to-right structure (equivalent to mind_map_horizontal capability)
- `free`: auto select based on complexity (equivalent to mind_map_free capability)

Auto rule in free mode:

- choose `center` when `depth <= 4` and `total_nodes <= 100`
- otherwise choose `horizontal`

## Supporting files

- Runtime engine: `mind-map-skill/scripts/mind_map_generator.py`
- Runner script: `mind-map-skill/scripts/run_mind_map.py`
- Example markdown: `mind-map-skill/examples/sample.md`
- Parameter schema (optional compatibility): `mind-map-skill/skill.yaml`
- Detailed reference: `mind-map-skill/reference.md`
- Usage examples: `mind-map-skill/examples.md`

## Font behavior

- On first run, the skill attempts to download a CJK font to local cache: `~/.cache/mind-map-skill/chinese_font.ttc`.
- Download source in repository: `resources/chinese_font.ttc` (not part of skill upload package).
- If download is unavailable, it falls back to prioritized system CJK fonts (Linux/macOS/Windows specific order).

## Project metadata

- **Author**: [@sawyer-shi](https://github.com/sawyer-shi)
- **Email**: sawyer36@foxmail.com
