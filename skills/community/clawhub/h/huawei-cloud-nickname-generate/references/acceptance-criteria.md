# Acceptance Criteria

| # | Criterion | How it is checked |
|---|-----------|-------------------|
| 1 | Skill directory follows the Huawei Cloud Skill layout (`SKILL.md` + `scripts/` + `tests/` + `references/`) | `validate-skill.sh`; directory tree |
| 2 | A single run reliably outputs one nickname (exit 0, no error) | `python3 scripts/generate_nickname.py`; `test_default_shape` |
| 3 | Results are random: different seeds give different nicknames | `test_different_seeds_differ` |
| 4 | Random logic is reproducible with the same `--seed` | `test_same_seed_is_reproducible`; CLI round-trip |
| 5 | `--count N` returns N de-duplicated nicknames; default (`1`) and maximum (`20`) are explicit | `test_count_returns_distinct_names`; `--count` bound tests; Parameter Confirmation table |
| 6 | `--style` / `--length` filtering actually constrains the picks | `test_style_filter_is_applied`; `test_length_filter_is_applied`; `test_style_and_length_combined` |
| 7 | Output is readable Markdown / plain text by default | `render_markdown()` / `render_text()`; render tests |
| 8 | `--format json` emits parseable JSON | `test_json_render_round_trips`; CLI `json.loads` |
| 9 | `--output` writes the result to a file | `test_cli_output_writes_file` |
| 10 | Bundled stdlib unit tests pass | `python3 -m unittest discover -s tests -v` |
| 11 | No Huawei Cloud API / resource / credential is required | No `hcloud`/SDK/requests in the source; runs offline |

## Out of scope (not acceptance criteria)

- Nickname uniqueness / real availability / handle-registration checks
- Trademark or sensitive-word compliance filtering
- Persistent storage or a personal nickname history
- Translation, romanisation, or pinyin output
- GUI