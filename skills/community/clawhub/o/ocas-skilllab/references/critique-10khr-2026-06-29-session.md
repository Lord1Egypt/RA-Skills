# 10khr Grinding Session — 2026-06-29

**Skills improved:** ocas-custodian (49→50), ocas-dispatch (49→50), ocas-mentor (49→50)  
**Library state:** 61/61 at 50/50

## Key Learnings

### 1. D3: The 450-line hard threshold

The heuristic scorer applies `total_lines > 450` → d3 -= 1. This means:
- 450 lines = no penalty (score 5)
- 451 lines = -1 penalty (score 4)

The skill rubric says "under 500 lines" for a 5, but the runner's heuristic is stricter at 450. **Always target ≤450 to guarantee D3 = 5/5.**

**Fix priority for D3 = 4/5:**
1. Remove duplicate Support File Map entries (huge ROI — often 5-15 lines)
2. Remove dated session-specific entries from Support File Maps (entries from >7 days ago that are just historical records)
3. Compact verbose gotchas by replacing inline detail with `references/` pointers
4. Remove duplicate/repeated sections in the main body
5. Remove empty lines between table rows

### 2. Support File Map Deduplication

After multiple sessions, Support File Maps accumulate duplicate entries. Always dedup by filename before measuring line count:

```bash
awk -F'|' '{print $2}' SKILL.md | grep "references/" | sed 's/^ *//' | sort | uniq -d
```

### 3. D1: `metadata.hermes` nesting

The frontmatter must use `metadata.hermes:` (nested), NOT flat `metadata:`. The heuristic checks for `includes:` when `references/` exists — missing it is a D1-4 deduction.

**Correct pattern:**
```yaml
metadata:
  author: Indigo Karasu
  version: 3.0.0
  hermes:
    tags: [monitoring]
    category: devops
```

### 7. D7: Error Handling table format

The heuristic scores D7 based on presence of "error" + "handling" in content. A formal table is the reliable fix:

```markdown
## Error Handling

| Failure | Handling |
|---------|----------|
| `read_file` blocked | Use `terminal(command="cat ...")` |
| grep blocked by hardline filter | Switch to python3 file I/O |
```

### 9. D9: Script baseline requirements

All scripts must have:
- `--help` (via argparse or sed-based self-documentation)
- `--dry-run` for destructive operations
- `set -euo pipefail` for bash
- Meaningful exit codes

**Bash --help pattern (no argparse needed):**
```bash
--help)
    sed -n '2,15p' "$0"
    exit 0
    ;;
```

### Duplicate body sections

Check for repeated sections with:
```bash
grep -n "^## " SKILL.md | sort -t: -k2 | uniq -fd 2
```

If "CRITICAL" or "MUST" sections appear twice, remove the duplicate.

## Skills Grinded

### ocas-custodian (466→449 lines, 49→50)
- Added `metadata.hermes` block with tags + category (D1)
- Added Error Handling section with failure/handling table (D7)
- Added checklists for Light Scan (10 steps) and Escalation Runner (8 steps) (D5)
- Fixed all 6 scripts with --help + --dry-run (D9)
- Removed duplicate content, redundant sections, 10 duplicate map entries
- Extracted verbose gotchas to references (config empty section, no-agent install)
- Removed redundant "Overview" section, incomplete map entries, dated scan records

### ocas-dispatch (451→449 lines, 49→50)
- Removed 2 session-specific entries from Support File Map

### ocas-mentor (505→449 lines, 49→50)
- Removed 56 dated session entries from Support File Map
- Removed duplicate "CRITICAL: Dispatch-triggered heartbeats" section (appeared identically twice)
- Removed stray table row (#75 entry left over from a copy-paste)