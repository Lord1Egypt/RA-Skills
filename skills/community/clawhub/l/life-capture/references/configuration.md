# Parser configuration

The parser behavior is controlled by `references/parser_config.json`.

## What you can change without editing Python

- expense category matching
- expense subcategory matching
- default tags
- task project mapping
- idea type mapping
- schedule tag mapping
- high-level hint regexes used during type inference

## Important notes

- Rules are evaluated top to bottom. Put more specific rules before broader ones.
- Each rule uses a Python regular expression string in `pattern`.
- Keep tags short. The parser trims tags to 8 characters and keeps at most 4 tags.
- When changing a pattern, test with `python scripts/parse_entries.py --text "..."` before packaging.

## File overview

### `expense_category_rules`
Maps text to an expense category and optional extra tags.

### `expense_subcategory_rules`
Adds a subcategory and optional extra tags.

### `idea_type_rules`
Maps an idea to a configured idea type.

### `task_project_rules`
Maps task text to a project bucket like `家务` or `健康`.

### `schedule_tag_rules`
Adds one extra tag for schedule entries.

### `default_tags`
Defines default tags for each record type.

### `hints`
Regexes used for initial type inference.
