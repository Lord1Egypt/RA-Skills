# Interactive Menu

When invoked interactively (via `/` command), present a two-level menu using the `clarify` tool so the user can pick which function to run.

**Level 1 — Category selection** (max 4 choices):

```python
result = clarify(
    question="What would you like to do?",
    choices=[
        "Analyze — ingest image, propose actions, execute action",
        "Config & Rollback — set configuration, rollback action",
        "Status — show system status",
        "Exit",
    ]
)
```

**Level 2 — Action selection** based on Level 1 choice:

- **Analyze** → clarify with choices: "ingest.image — Ingest an image for analysis", "propose.actions — Propose actions from image", "execute.action — Execute a proposed action"
- **Config & Rollback** → clarify with choices: "rollback.action — Rollback an action", "config.set — Set configuration value"
- **Status** → run "status — Show system status" directly (single action — no sub-menu needed)
- **Exit** → break the loop

After the user selects an action, execute it following the relevant procedure in this skill. Loop back to the menu after each action completes, until the user chooses to exit or sends `/stop`.

### Response parsing

Match the user's response against the full choice string. Extract the action key by splitting on `" — "` and taking the first segment. If the response doesn't match any known choice (user typed free-form via "Other"), match key prefixes case-insensitively. Re-present the current menu level on no match.

### Platform adaptation

On CLI, choices are navigable with arrow keys. On messaging platforms, choices render as a numbered list. The two-level hierarchy ensures no more than 4 options appear at any level on any platform.




Look bridges the physical world and the digital agent — it takes a user-provided image, infers what the user probably wants done with it, and produces a validated, decision-ready action draft across domains including calendar events, meal macros, places, product comparisons, receipts, documents, and civic reports. It resolves ambiguity through research and option reduction before asking any clarifying questions, and nothing executes without explicit per-draft confirmation.

