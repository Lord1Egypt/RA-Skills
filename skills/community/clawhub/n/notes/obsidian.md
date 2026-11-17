# Obsidian

A vault is a folder of plain markdown, which makes Obsidian the only app-backed platform where the files are also a first-class interface. Driven through `obsidian-cli`, or edited directly.

**Contents:** [Requirements](#requirements) · [Choosing the Vault](#choosing-the-vault) · [Operations](#operations) · [Renames and Wikilinks](#renames-and-wikilinks) · [Direct File Editing](#direct-file-editing) · [Vault Layout](#vault-layout) · [Plugins and Portability](#plugins-and-portability) · [Fallback](#fallback) · [Obsidian Traps](#obsidian-traps)

**Before writing**, read `vault_path` in `~/Clawic/data/notes/config.yaml` and `## Platform Facts` in `memory.md`. Most Obsidian mistakes are one mistake: writing into the wrong vault, where the note is not lost but is unfindable because nobody opens that vault.

## Requirements

Obsidian installed, plus the user's own installation of `obsidian-cli` (`brew install yakitrak/yakitrak/obsidian-cli`). Nothing is installed on the user's behalf. Direct file editing needs neither — a vault is a folder, and the app picks up external changes automatically.

## Choosing the Vault

```bash
obsidian-cli print-default                 # which vault is default
obsidian-cli print-default --path-only     # its path on disk
obsidian-cli set-default "VaultName"
```

- **Multiple vaults are the norm** (work, personal, an archive). Resolve the target once per session and record it in `## Platform Facts`; never rely on "the default" staying the same.
- **`vault_path` in config is the declaration**; `print-default` is the observation. When they disagree, the declaration wins and the discrepancy is said out loud once (SKILL.md, precedence).
- macOS keeps the vault registry at `~/Library/Application Support/obsidian/obsidian.json`; it is read-only intelligence about which vaults exist, not a file to edit.

## Operations

```bash
obsidian-cli search "pricing"                    # by note name
obsidian-cli search-content "three tiers"        # by content, returns snippets and line numbers
obsidian-cli create "Meetings/2026-07-26 Pricing" --content "$CONTENT"
obsidian-cli create "Meetings/2026-07-26 Pricing" --content "$CONTENT" --open
obsidian-cli move "Inbox/old note" "Meetings/2026-07-26 Pricing"
obsidian-cli delete "Inbox/old note"
```

Content with frontmatter is passed as a here-doc into a variable, so the YAML survives intact:

```bash
CONTENT=$(cat << 'EOF'
---
date: 2026-07-26
type: meeting
title: "Pricing: staying at three tiers"
tags: [product, pricing]
attendees: [alice, bob]
---

## Decisions
- Three tiers stay; revisit at 500 customers — @alice
EOF
)
obsidian-cli create "Meetings/2026-07-26 Pricing" --content "$CONTENT"
```

## Renames and Wikilinks

**This is the one rule that matters here.** `[[wikilinks]]` resolve by note name, so renaming a file outside Obsidian breaks every inbound link, silently and with no error.

- **Always rename with `obsidian-cli move`** (or the app's own rename), which rewrites links across the vault.
- **A rename done in Finder is repaired by grepping the old name** across the vault and fixing each hit in the same turn (`local.md`).
- **Backlinks are the reason to link at all here.** A vault whose links are broken has lost the only feature that justified the app.
- **For notes expected to leave Obsidian**, prefer relative markdown links: wikilinks resolve nowhere else (`migration.md`).

## Direct File Editing

A vault is a folder, so anything in `local.md` applies: grep, git, batch edits, frontmatter queries.

```bash
VAULT=$(obsidian-cli print-default --path-only)
grep -rl '^tags:.*pricing' "$VAULT"
```

- **Obsidian picks up external writes automatically**, but a file open in the app can be overwritten by the app's own save. Close the note before a batch edit.
- **Do not write into dotted folders** (`.obsidian/`, `.trash/`): they are app state, and a note created there is invisible in the UI.
- Bulk operations state how many files they will touch before running, and are not run while sync is mid-write (`sync.md`).

## Vault Layout

Mirror the type folders so a note keeps its identity across routing changes: `Meetings/`, `Decisions/`, `Projects/`, `Journal/`, `Research/`, `Inbox/`.

- **Obsidian's own daily-note plugin will fight a `Journal/YYYY-MM-DD.md` convention** if it is configured for a different folder or format. Check its setting once, align it, and record which won in `## Platform Facts`.
- **Attachments**: set the vault to store attachments next to the note or in one attachments folder — either works, but the setting must be known, because it decides whether a moved note keeps its images.
- Tags live in frontmatter (`tags: [a, b]`) rather than inline `#tags`: the frontmatter form is what survives export and what a grep finds.

## Plugins and Portability

- **Plugin syntax is not markdown.** Dataview queries, callout variants, and templater expressions render as noise anywhere else, including in a future export. Keep them out of decisions, research, and anything with a long life.
- **Community plugins can read and write the whole vault.** That is a supply-chain surface on a folder that may hold client material — a fact to state once, not to police.
- **`.obsidian/workspace.json` churns on every window change** and conflicts on every synced device; exclude it from git and from selective sync (`sync.md`).
- The vault is already plain markdown, so migration out is the cheapest of any app-backed platform: copy the folder (`migration.md`).

## Fallback

If `obsidian-cli` is missing, write the file directly into the vault path — the app will pick it up. If the vault path itself is unknown, write locally, stamp `platform: local (fallback from obsidian)`, and say it in one line (SKILL.md Rule 1).

## Obsidian Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Writing into whichever vault is default | The note lands in a vault nobody opens | Resolve the vault once per session, record it |
| Renaming in Finder | Every inbound wikilink breaks with no error | `obsidian-cli move`, or grep and repair |
| Wikilinks in notes that will be exported | They resolve nowhere outside Obsidian | Relative links for durable notes |
| Inline `#tags` only | Missed by frontmatter greps and lost in some exports | `tags:` in frontmatter |
| Editing a file open in the app | The app's save overwrites the external write | Close the note first |
| Creating notes in `.obsidian/` or `.trash/` | Invisible in the UI, deleted without warning | Real folders only |
| Dataview or templater syntax in a decision note | Unreadable in five years and in every other tool | Plain markdown for durable notes |
| Committing `.obsidian/workspace.json` | A conflict on every device, every session | Exclude it |

**Write triggers for this file** — in the same turn: the resolved vault path, the daily-note plugin setting and the attachment setting to `## Platform Facts` in `~/Clawic/data/notes/memory.md`; `vault_path` and the routing choice to `config.yaml` and `## Note Map`; every action item found in a vault note to `actions.md` with `Source: obsidian:[[Note]]`; a bulk rename or link repair to `artifacts/<kebab-name>.md` with how many files were touched. Formats and thresholds: `memory-template.md`.
