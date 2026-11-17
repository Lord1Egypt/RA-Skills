# Interactive Menu

When invoked interactively (via `/` command), present a menu using the `clarify` tool so the user can pick which function to run.

```python
result = clarify(
    question="What would you like to do?",
    choices=[
        "run — Run task through multi-pass pipeline",
        "search — Search for capability gaps",
        "sessions — List active sessions",
        "More — replay session, show status",
    ]
)
```

If the user selects **More**, present a second clarify with choices: "replay — Replay a session", "status — Show system status".

After the user selects an action, execute it following the relevant procedure in this skill. Loop back to the menu after each action completes, until the user chooses to exit or sends `/stop`.

## Response parsing

Match the user's response against the full choice string. If the response doesn't match any known choice (user typed free-form via "Other"), match key prefixes case-insensitively. Re-present the menu on no match.

## Platform adaptation

On CLI, choices are navigable with arrow keys. On messaging platforms, choices render as a numbered list. The max-4-choices rule applies at every menu level.
