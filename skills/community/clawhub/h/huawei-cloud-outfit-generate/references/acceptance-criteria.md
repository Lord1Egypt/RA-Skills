# Acceptance Criteria

| # | Criterion | How it is checked |
|---|-----------|-------------------|
| 1 | Skill directory follows the Huawei Cloud Skill layout (`SKILL.md` + `scripts/` + `tests/` + `references/`) | `validate-skill.sh`; directory tree |
| 2 | A single run reliably outputs one outfit covering 上装 / 下装 / 鞋履 / 配饰 | `python3 scripts/generate_outfit.py`; `test_default_shape` |
| 3 | Output is readable Markdown / plain text | `render_markdown()` / `render_text()`; `test_markdown_contains_sections` |
| 4 | Results are random: different seeds give different outfits | `test_different_seeds_differ` |
| 5 | Random logic is reproducible with the same `--seed` | `test_same_seed_is_reproducible`; CLI round-trip |
| 6 | `--style` / `--season` filtering actually constrains the picks | `test_style_filter_is_applied`; `test_season_filter_is_applied` |
| 7 | `--format json` emits parseable JSON | `test_json_render_round_trips`; CLI `json.loads` |
| 8 | No Huawei Cloud API / resource / credential is required | No `hcloud`/SDK/curl in the skill; runs offline |

## Out of scope (not acceptance criteria)

- Real merchandising catalogue / brand SKUs / pricing or sizing data
- Weather API integration or calendar/schedule awareness
- Drawing / image rendering of the outfit
- Persistent storage or a personal wardrobe history
- GUI