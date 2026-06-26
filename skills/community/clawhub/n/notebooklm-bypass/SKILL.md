---
name: notebooklm
description: Programmatic NotebookLM control with auto-recovery for authentication errors.
---

# NotebookLM CLI

## Commands
```bash
notebooklm list                                    # List all notebooks + IDs
notebooklm create "Name"                           # Create notebook → returns ID
notebooklm source add "<url_or_file>" -n <ID>      # Add URL/PDF/YouTube to notebook
notebooklm source add "<url>" -n <ID> --wait       # Add + wait for processing
notebooklm source list -n <ID>                     # List sources in notebook
notebooklm ask "Question" -n <ID>                  # Query AI against sources
```

## Rules
1. **No playlists.** Extract individual YouTube URLs and add one by one.
2. **Max 50 sources** per notebook.
3. **Use `--wait`** when adding sources in scripts to ensure processing completes.
4. **Auth Recovery:** If `notebooklm` fails with "Authentication expired", you MUST ask the user for explicit permission before recovering. Propose running `python {WORKSPACE_DIR}/skills/notebooklm-bypass/scripts/auto_playwright.py`. If and only if they approve, run the script. This script steals fresh cookies and automatically injects them into your Windows Environment Variables. Once complete, retry your command.
