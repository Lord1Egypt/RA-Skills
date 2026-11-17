# Interactive Menu

When invoked interactively (via `/` command), present a two-level menu using the `clarify` tool so the user can pick which function to run.

**Level 1 — Category selection** (max 4 choices):

```python
result = clarify(
    question="What would you like to do?",
    choices=[
        "Scan — scan Google Drive structure",
        "Organize — analyze, propose, and apply changes",
        "Manage — review, approve, or undo proposals",
        "Exit",
    ]
)
```

**Level 2 — Action selection** based on Level 1 choice:

- **Scan** → clarify with choices: "Deep scan", "Light scan"
- **Organize** → clarify with choices: "Analyze and propose", "Simulate changes"
- **Manage** → clarify with choices: "Review proposals", "Apply changes", "Undo last change", "Show status"
- **Exit** → break loop

After the user selects an action, execute it following the relevant procedure in this skill. Loop back to the Level 1 menu after each action completes, until the user chooses Exit or sends `/stop`.

### Response parsing

Match the user's response against the full choice string. If the response doesn't match any known choice (user typed free-form via "Other"), match key prefixes case-insensitively. Re-present the current menu level on no match.

### Platform adaptation

On CLI, choices are navigable with arrow keys. On messaging platforms, choices render as a numbered list. The two-level hierarchy ensures no more than 4 options appear at any level on any platform.


