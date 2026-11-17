# Acceptance Criteria

| # | Criterion | How it is checked |
|---|-----------|-------------------|
| 1 | Skill directory follows the Huawei Cloud Skill layout (`SKILL.md` + `scripts/` + `tests/`) | `validate-skill.sh`; directory tree |
| 2 | Triggering the generator reliably outputs a study plan (7 days x 3 slots by default) | `test_default_plan_shape`; CLI run |
| 3 | Output format is clear (Markdown table: 日期 \| 时段 \| 学习主题 \| 实践内容 \| 时长) | `test_markdown_has_table_header_and_rows`; CLI run |
| 4 | Random generation produces different plans per run | `test_different_seed_differs` |
| 5 | The same `--seed` reproduces the exact same plan | `test_same_seed_is_reproducible`; CLI round-trip |
| 6 | Key parameters are configurable (days / slots per day / topics / session length) | `test_custom_days_and_slots`, `test_topics_as_names`, `test_topics_as_json_file`, CLI runs |
| 7 | Topics do not repeat until the pool is exhausted | `test_topic_no_repeat_until_pool_exhausted` |
| 8 | A day's time slots do not overlap; durations stay in a reasonable interval | `test_slots_do_not_overlap_within_a_day`, `test_durations_within_bounded_interval` |
| 9 | No Huawei Cloud API / resource / credential is required | No `hcloud`/SDK/curl in the skill; runs offline |

## Out of scope (not acceptance criteria)

- Calendar integration / reminders
- Progress tracking or persistence
- Nutrition-style scoring or difficulty estimation
- GUI / web interface