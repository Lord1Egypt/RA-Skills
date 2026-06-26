---
name: file-organizer
description: Scan, deduplicate, and organize files in a directory (Downloads, Desktop, etc.). Use when asked to: clean up downloads, organize files, find duplicates, declutter desktop, sort files by type, move files into folders, remove duplicate files, create a file inventory, or tidy up a folder. Conservative by default — always shows a plan before moving anything. NEVER deletes files.
---

# File Organizer

Scans a target directory, categorizes files by type, finds duplicates, and generates (or executes) a cleanup plan. Dry-run by default — always shows what will happen before doing it.

## Scripts

All scripts live in `scripts/`. Run with `python3`. No third-party dependencies.

| Script | Purpose |
|--------|---------|
| `scan.py` | Walk a directory, output JSON inventory |
| `find_duplicates.py` | Find duplicate files by content hash |
| `organize.py` | Generate and optionally execute a move plan |
| `manifest.py` | Produce a markdown before/after manifest |

Category mappings (extension → folder) are in `references/categories.md`. Read it if asked about supported file types or to customize mappings.

## Typical Workflow

### 1. Scan the directory

```bash
python3 scripts/scan.py ~/Downloads --output /tmp/scan.json
```

Add `--hash` to pre-compute hashes (needed for duplicate detection without a separate pass).

### 2. Find duplicates (optional)

```bash
python3 scripts/find_duplicates.py /tmp/scan.json --output /tmp/dupes.json
```

Or scan and deduplicate in one step:
```bash
python3 scripts/find_duplicates.py --directory ~/Downloads
```

### 3. Generate organization plan (dry run)

```bash
python3 scripts/organize.py /tmp/scan.json --output /tmp/plan.json
```

Or scan + plan in one step:
```bash
python3 scripts/organize.py --directory ~/Downloads
```

Key flags:
- `--dest ~/Downloads/Organized` — custom destination (default: `<dir>/Organized/`)
- `--flat` — don't preserve subdirectory structure
- `--dry-run` — default, shows plan without moving anything
- `--execute` — actually move files (prompts for confirmation)
- `--execute --yes` — skip confirmation prompt

### 4. Execute the plan

```bash
python3 scripts/organize.py /tmp/scan.json --execute
# or skip the prompt:
python3 scripts/organize.py /tmp/scan.json --execute --yes
```

### 5. Generate manifest

```bash
# From plan JSON
python3 scripts/manifest.py --plan /tmp/plan.json --output /tmp/manifest.md

# Before/after comparison (run scan.py twice)
python3 scripts/manifest.py --before /tmp/before.json --after /tmp/after.json --output /tmp/diff.md

# Simple inventory
python3 scripts/manifest.py --scan /tmp/scan.json --output /tmp/inventory.md
```

## Safety Rules

- `organize.py` **never deletes files** — only moves them
- Dry-run is the default; `--execute` must be explicit
- Symlinks are skipped (never moved)
- Destination conflicts are flagged in the plan and skipped during execution (unless `--yes`)
- Hidden files/dirs (`.dotfiles`) are skipped by default; use `--include-hidden` to include them

## Common Scenarios

**"Clean up my Downloads folder"**
→ Run scan + organize dry-run, show the plan summary, ask user to confirm before executing.

**"Find duplicate files in my Desktop"**
→ Run `find_duplicates.py --directory ~/Desktop`, report groups sorted by wasted space.

**"Organize my files and save a report"**
→ Run scan → organize (dry-run) → confirm → organize (execute) → manifest to markdown.

**"What file types are supported?"**
→ Read `references/categories.md` and summarize the category mappings.

## Output Locations

Default destination for organized files: `<target_dir>/Organized/`
Subfolders are created per category: `Images/`, `Documents/`, `Videos/`, etc.
Files with unrecognized extensions go to `Other/`.
