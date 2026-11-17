---
name: normalize-whitespace
description: Normalize indentation of a large reference text document (e.g. README.md) to a consistent TAB style while keeping content byte-identical. Use when asked to fix inconsistent leading spaces, align command blocks, or clean indentation spread across hundreds of lines in a prose-heavy, single-fence document. Built from the 2026-09 instguid README.md normalization session.
---

# Normalize whitespace in a text document

Removes inconsistent leading-space indentation (2/4/8-space outliers) by converting command lines and code blocks to a leading-tab style, while preserving content exactly and leaving verbatim/preformatted regions untouched. The guiding invariant: **no character of content may change** — only leading/trailing whitespace.

## Rules (immutable)

1. **Whitespace changes only.** The final content-integrity check is `git diff --ignore-all-space --ignore-blank-lines` against the pre-change state: it must show *only* real, user-approved content edits (line merges etc.). If it shows anything else, a bug ate a character — stop and fix before continuing.
2. **Classify every line before editing.** Buckets: (a) command/code line → normalize to tab; (b) verbatim/prose/preformatted → leave byte-identical; (c) ambiguous → ask the user, never guess.
3. **Never touch what is content, not noise:** verbatim terminal captures (`[root@... ~]#`, `mbp:~ jeff$`), ASCII-art/flowcharts, GUI-navigation prose (`panel > ...`), and verbatim copies of config files (raidtab, XF86Config, `/etc/config/network`, XML). Prefer state your leave-as-is classes up front so the user can correct the list.
4. **`grep`-ability is preserved.** Word-repeat separators may truncate the last repeat (e.g. `cachyos...cach`) — intended; `grep '^cachyos'` still matches.

## Procedure

### 1. Establish the file's conventions
- Read the repo's `AGENTS.md` for its whitespace/wall rules (instguid's README: single ```bash fence, TAB indentation, 60-char walls).
- State the leave-as-is classes aloud, then confirm the target style (tab vs space) before running anything that writes.

### 2. Scan & classify with a marker-level view
Use `cat -A` (`^I` = tab, `$` = EOL) over suspicious regions, and drive bulk analysis from Python, e.g. list every line with leading spaces:

```python
from pathlib import Path
lines = Path('README.md').read_text().split('\n')
for i, l in enumerate(lines, 1):
    if l.startswith(' ') and l.strip():
        print(i, repr(l[:80]))
```

### 3. Apply whitespace edits with Python read/replace/write
The built-in `edit` tool treats whitespace-only `oldString`s as no-ops — it will not change `"    x"` to `"\tx"`. Do the writes in Python:

```python
from pathlib import Path
p = Path('README.md')
lines = p.read_text().split('\n')
for i, l in enumerate(lines):
    if l.startswith('    '):          # exact old/new required
        lines[i] = '\t' + l[4:]
p.write_text('\n'.join(lines))
```

**Longest-prefix-first.** When stripping multiple indent depths, branch on the longest first:
```
if l.startswith('    '):  -> \t + l[4:]
elif l.startswith('  '):  -> \t + l[2:]
```
Matching the 2-space branch first silently leaves 2 spaces behind.

**Prefer explicit exact-string maps** over arithmetic slicing for anything except mechanical `startswith(n)` strips. A slicing-start bug (`old[2:]` vs `old[1:]`) can silently drop the first character (`no` → `o`) — dump `repr()` of the surrounding lines before and after any non-trivial transform, and re-run `git diff` after each batch.

### 4. Binary/UTF-8 lines break string matching
Lines containing non-ASCII bytes (e.g. openssl `Salted__...` demo output, OCR-corrupted art) fail literal `str.replace`/`find`. Switch to line-index transforms (`enumerate`) keyed on a neighbouring ASCII anchor (`if 'SSH Tunnel not running' in l:`) instead of matching the whole line.

### 5. Verify each band, then the whole file
- After each section: re-scan with `awk 'NR>=... && /^ +[^ ]/' README.md | cat -A` until no unexpected leading-space lines remain.
- When a line's destination depends on your earlier loop state (a variable reused across strides), re-verify the exact output lines — this is where content-loss bugs (e.g. `wifi-menu -o` overwritten) sneak in.
- End of file: confirm the single code fence is intact (`grep -n '^```'` → exactly the opening line and the closing line) and the separator walls' reported width matches the spec.

## Example: instguid README.md (2026-09)

Normalized ~600 lines across AIX/linux/security/ssh/mac/arch/pacman/nodejs/python sections:
- 4-space command lines → `\t`; nested script bodies → `\t    ` (tab + 4-space steps, matching the existing `__complete_ssh_host()` / `createTunnel()` style).
- Script shebangs got tabbed with their bodies; heredocs (`docker-completion`), command lists, and `==> Formulae`/`==> Casks` output headers tabbed.
- Left byte-identical: `[root@storage-2 ~]#` / `mbp:~ jeff$` / `jeff@debian:~$` captures, ifconfig/glxinfo/brew output alignment, the OpenVPN MTU prose, GUI-nav prose, config copies (raidtab, XF86Config, OpenWrt network, fontconfig XML), the ASCII rubric.
- Content-integrity diff stayed clean the whole way; two line-merges were the only real edits. One loop bug temporarily replaced `wifi-menu -o` with a stale value — caught by immediate re-scan and restored.