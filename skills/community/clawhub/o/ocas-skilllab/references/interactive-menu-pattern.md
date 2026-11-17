# Interactive Menu Pattern

When invoked interactively (via `/` command), present a menu using the `clarify` tool so the user can pick which function to run.

## Single-Level Menu

```python
result = clarify(
    question="What would you like to do?",
    choices=[
        "action1 — Description of action 1",
        "action2 — Description of action 2",
        "action3 — Description of action 3",
        "More — additional options",
    ]
)
```

## Two-Level Menu

**Level 1 — Category selection** (max 4 choices):

```python
result = clarify(
    question="What would you like to do?",
    choices=[
        "Category1 — description",
        "Category2 — description",
        "Category3 — description",
        "Status — show system status",
    ]
)
```

**Level 2 — Action selection** based on Level 1 choice. Present another clarify with the specific actions for that category.

## Response Parsing

Match the user's response against the full choice string. Extract the action key by splitting on `" — "` and taking the first segment. If the response doesn't match any known choice (user typed free-form via "Other"), match key prefixes case-insensitively. Re-present the current menu level on no match.

## Platform Adaptation

On CLI, choices are navigable with arrow keys. On messaging platforms, choices render as a numbered list. The max-4-choices rule applies at every menu level. For skills with more than 4 actions, use a two-level hierarchy.