# Interactive Menu

When invoked interactively (via `/` command), present a two-level menu using the `clarify` tool so the user can pick which function to run.

**Level 1 — Category selection** (max 4 choices):

```python
result = clarify(
    question="What would you like to do?",
    choices=[
        "Scan & Ingest — scan for signals, ingest manually, enrich items",
        "Query & Discover — get recommendations, serendipity",
        "Model & Reports — taste model status, weekly reports, Spotify sync",
        "Journal — write journal for current run",
    ]
)
```

**Level 2 — Action selection** based on Level 1 choice:

- **Scan & Ingest** → clarify with choices: "scan — Scan for taste signals", "scan.report — Generate taste scan report", "ingest.signal — Ingest a taste signal manually", "enrich.item — Enrich item with metadata"
- **Query & Discover** → clarify with choices: "query.recommend — Get recommendations", "query.serendipity — Get serendipitous discoveries"
- **Model & Reports** → clarify with choices: "model.status — Show taste model status", "report.weekly — Generate weekly report", "sync.spotify — Sync Spotify history"
- **Journal** → run "journal — Write journal for current run" directly (single action — no sub-menu needed)

After the user selects an action, execute it following the relevant procedure in this skill. Loop back to the menu after each action completes, until the user chooses to exit or sends `/stop`.

### Response parsing

Match the user's response against the full choice string. Extract the action key by splitting on `" — "` and taking the first segment. If the response doesn't match any known choice (user typed free-form via "Other"), match key prefixes case-insensitively. Re-present the current menu level on no match.

### Platform adaptation

On CLI, choices are navigable with arrow keys. On messaging platforms, choices render as a numbered list. The two-level hierarchy ensures no more than 4 options appear at any level on any platform.