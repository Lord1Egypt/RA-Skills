---
name: gkeep-notes
description: Google Keep notes via gkeepapi. List, search, create, manage notes. Add items to notes. Supports authorization via OAuth 2.0 Token.
slash: gkeep-notes
version: 1.0.14
author: PromptingPufferfish
homepage: https://github.com/PromptingPufferfish/gkeep-notes
metadata:
  openclaw:
    emoji: "📝"
    requires:
      bins: ["python3"]
    setup: |
      cd ~/.openclaw/workspace/skills/gkeep-notes
      python3 -m venv venv
      source venv/bin/activate
      pip install -r requirements.txt
---

# Google Keep Notes Skill 📝

## WHEN TO USE
Use this skill when users ask to:
- List Google Keep notes
- Search notes by keyword  
- Create new notes
- Add items to notes
- Get specific note details
- Archive/pin/delete notes

**"List" = Google Keep note (not a bullet list)**

## SETUP (First Run Only)
1. Creates venv + installs requirements automatically
2. Manual call of generate_token.py from the shell, then copy & paste token to file `$HOME/.config/gkeep/token.json`. 

```
gkeep.py list [--limit 10]                    # List notes
gkeep.py search "note_name"                   # Search notes  
gkeep.py get <note_id>                        # Get note details
gkeep.py create "note_name" "note_body"       # Create note
gkeep.py add <note_id> "new item"             # Add item to note
gkeep.py archive <note_id>                    # Archive note
gkeep.py delete <note_id>                     # Trash note
gkeep.py pin <note_id>                        # Pin note
gkeep.py unpin <note_id>                      # Unpin note
```

## USAGE FLOW
```
1. User: "Show my <note_name>"
2. → gkeep.py list | grep <note_name> → note_id
3. → gkeep.py get <note_id> → show content
4. User: "Add milk to <note_name>"
5. → gkeep.py list | grep <note_name> → note_id 
6. → gkeep.py add <note_id> "milk"
```

## EXECUTION TEMPLATE
```bash
cd ~/.openclaw/workspace/skills/gkeep-notes
source venv/bin/activate
python gkeep.py [command] [args]
```

## TROUBLESHOOTING
```
❌ "No token" → manually generate token with generate_token.py and copy token into token.json
❌ "Module not found" → setup properly
❌ "API changed" → Check GitHub issues
```

## NOTES
- Unofficial API (may break if Google changes)
- venv auto-created during setup
- Note IDs from `gkeep list` output
- Active project (updated March 2026)
```
