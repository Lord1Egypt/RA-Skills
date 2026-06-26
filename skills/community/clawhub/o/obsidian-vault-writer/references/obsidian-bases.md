# Obsidian Bases Reference

Bases files (`.base`) create database-like views of vault notes using YAML.

Full docs: https://help.obsidian.md/bases/syntax

---

## Workflow

1. Create a `.base` file in the vault with valid YAML content.
2. Add `filters` to select which notes appear.
3. Add `formulas` (optional) for computed properties.
4. Configure `views` (table, cards, list, or map).
5. Validate: no YAML syntax errors; all referenced properties and formulas defined.

---

## Schema

```yaml
# Global filters applied to ALL views
filters:
  and: []
  or: []
  not: []

# Computed properties
formulas:
  formula_name: 'expression'

# Display name overrides
properties:
  property_name:
    displayName: "Display Name"
  formula.formula_name:
    displayName: "Formula Display Name"

# Custom summary formulas
summaries:
  custom_summary_name: 'values.mean().round(3)'

# Views
views:
  - type: table | cards | list | map
    name: "View Name"
    limit: 10
    groupBy:
      property: property_name
      direction: ASC | DESC
    filters:
      and: []
    order:
      - file.name
      - property_name
      - formula.formula_name
    summaries:
      property_name: Average
```

---

## Filter Syntax

```yaml
# Single filter
filters: 'status == "done"'

# AND
filters:
  and:
    - 'status == "done"'
    - 'priority > 3'

# OR
filters:
  or:
    - file.hasTag("book")
    - file.hasTag("article")

# NOT
filters:
  not:
    - file.hasTag("archived")
```

Filter operators: `==`, `!=`, `>`, `<`, `>=`, `<=`, `&&`, `||`, `!`

---

## Property Types

1. **Note properties** — frontmatter: `status`, `author`
2. **File properties** — metadata: `file.name`, `file.mtime`, `file.size`, `file.tags`, `file.path`, `file.folder`
3. **Formula properties** — computed: `formula.my_formula`

---

## Formula Syntax

```yaml
formulas:
  total: "price * quantity"
  status_icon: 'if(done, "✅", "⏳")'
  created: 'file.ctime.format("YYYY-MM-DD")'
  days_old: '(now() - file.ctime).days'
  days_until_due: 'if(due_date, (date(due_date) - today()).days, "")'
```

Key functions: `date()`, `now()`, `today()`, `if()`, `duration()`, `file()`, `link()`

**Duration pitfall:** Subtracting two dates returns a `Duration`, not a number. Access `.days`, `.hours`, etc. before calling number functions:

```yaml
# CORRECT
"(now() - file.ctime).days.round(0)"

# WRONG — Duration doesn't support .round() directly
"(now() - file.ctime).round(0)"
```

---

## Default Summary Formulas

`Average`, `Min`, `Max`, `Sum`, `Range`, `Median`, `Stddev`, `Earliest`, `Latest`, `Checked`, `Unchecked`, `Empty`, `Filled`, `Unique`

---

## Example: Daily Notes Index

```yaml
filters:
  and:
    - file.inFolder("Daily Notes")
    - '/^\d{4}-\d{2}-\d{2}$/.matches(file.basename)'

formulas:
  day_of_week: 'date(file.basename).format("dddd")'

views:
  - type: table
    name: "Recent Notes"
    limit: 30
    order:
      - file.name
      - formula.day_of_week
      - file.mtime
```

---

## Embedding in Markdown

```markdown
![[MyBase.base]]
![[MyBase.base#View Name]]
```

---

## YAML Quoting Rules

- Use single quotes for formulas containing double quotes: `'if(done, "Yes", "No")'`
- Quote strings containing `:`, `{`, `}`, `[`, `]`, `#`, and similar YAML special characters.
