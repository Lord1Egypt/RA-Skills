# Memory Template - IMAP

Create `~/imap/memory.md` with this structure:

```markdown
# IMAP Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined
mutation_default: read_only | ask_first | allowed_for_named_playbooks
report_style: concise | detailed

## Activation
<!-- When this skill should activate -->
<!-- Example: Use automatically for mailbox search, IMAP triage, and sync debugging -->

## Accounts
<!-- High-level account list only -->
<!-- Example: fastmail-work, proton-bridge-personal -->

## Preferences
<!-- Stable user preferences about mailbox workflows -->
<!-- Example: Never mark mail seen during reviews -->

## Notes
<!-- Durable operational notes worth remembering -->

---
Updated: YYYY-MM-DD
```

Create `~/imap/accounts.md` with this structure:

```markdown
# IMAP Accounts

## {account-label}
- provider:
- endpoint:
- auth style:
- default folders:
- capabilities:
- notes:
```

Create `~/imap/folder-map.md` with this structure:

```markdown
# Folder Map

## {account-label}
- delimiter:
- inbox:
- archive:
- sent:
- drafts:
- trash:
- junk:
- notes:
```

Create `~/imap/sync-state.md` with this structure:

```markdown
# Sync State

## {account-label} / {folder}
- uidvalidity:
- uidnext:
- highestmodseq:
- last_processed_uid:
- last_sync:
- notes:
```

Create `~/imap/playbooks.md` with this structure:

```markdown
# Playbooks

## {playbook-name}
- goal:
- safe by default: yes | no
- typical search:
- fetch depth:
- allowed mutations:
- reporting format:
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning mailbox habits | Keep refining defaults over time |
| `complete` | Stable enough for normal work | Use saved policy unless the user changes it |
| `paused` | User does not want setup questions now | Work with current context only |
| `never_ask` | User does not want mailbox-profile questions | Stop asking and only react to explicit instructions |

## Key Principles

- Save non-secret context only.
- Keep mutation policy explicit so mailbox actions stay predictable.
- Use account labels and folder names exactly as discovered.
- Reset sync assumptions if `UIDVALIDITY` changes.
- Prefer short operational notes over verbose message history.
