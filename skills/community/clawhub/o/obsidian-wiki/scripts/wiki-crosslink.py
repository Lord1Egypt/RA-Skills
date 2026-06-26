#!/usr/bin/env python3
"""wiki-crosslink.py — Find unlinked mentions of wiki page titles/aliases.

Scans wiki pages for text mentions of known page titles and aliases that are
not already wrapped in [[wikilinks]]. Useful for enriching cross-references.

Usage:
  python3 wiki-crosslink.py <vault-path>          # report unlinked mentions
  python3 wiki-crosslink.py <vault-path> --fix     # auto-add [[wikilinks]]
  python3 wiki-crosslink.py <vault-path> --help

Structured output:
  UNLINKED:<file>\t<mention>\t<target-filename>
  STATS:scanned=N unlinked=N fixed=N

Skips:
  - Code blocks and inline code
  - Obsidian comments (%% ... %%)
  - YAML frontmatter
  - Existing [[wikilinks]]
  - Titles <= 3 characters (unless explicitly defined as aliases in frontmatter)
"""
import os, sys, re, tempfile

# Ensure wiki_lib is importable from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wiki_lib import (
    WikiMap, read_md, parse_link_target, frontmatter_re,
    wikilink_re, fence_re, fence_unclosed_re, inline_code_re, comment_re,
)

# Markdown link/image regex: [text](url) or ![alt](url) or [text][ref] or [ref]: url ...
_md_link_re = re.compile(r"!?\[[^\]]*\]\([^)]*\)|!?\[[^\]]*\]\[[^\]]*\]|^\[[^\]]*\]:.*$", re.MULTILINE)

# ── Argument parsing ──────────────────────────────────────

if "--help" in sys.argv or "-h" in sys.argv:
    print("Usage: python3 wiki-crosslink.py <vault-path> [--fix]")
    print("Find page titles/aliases mentioned in text without [[wikilinks]].")
    print("  --fix   Auto-add [[wikilinks]] for unlinked mentions")
    sys.exit(0)

vault = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else None
if not vault:
    print("Usage: python3 wiki-crosslink.py <vault-path> [--fix]", file=sys.stderr)
    sys.exit(2)

_known_flags = {"--fix", "--help", "-h"}
for arg in sys.argv[1:]:
    if arg.startswith("-") and arg not in _known_flags:
        print(f"Error: unknown option '{arg}'", file=sys.stderr)
        sys.exit(2)

fix_mode = "--fix" in sys.argv

wiki_dir = os.path.join(vault, "wiki")
if not os.path.isdir(wiki_dir):
    print(f"Error: {wiki_dir} not found", file=sys.stderr)
    sys.exit(2)

# ── Build maps ────────────────────────────────────────────

wm = WikiMap(vault)

# Collect explicit aliases from frontmatter (exempt from 3-char filter)
_aliases_re = re.compile(r"^aliases:\s*\[(.+?)\]\s*$", re.MULTILINE)
_explicit_aliases = set()
for md in wm.content_pages():
    content = read_md(md)
    if not content:
        continue
    fm_match = frontmatter_re.match(content)
    if not fm_match:
        continue
    fm = fm_match.group(1)
    m = _aliases_re.search(fm)
    if m:
        for alias in m.group(1).split(","):
            alias = alias.strip().strip("'\"")
            if alias:
                _explicit_aliases.add(alias)

# Build sorted list of (mention_text, target_basename) pairs to search for.
# Longer mentions first to avoid partial matches shadowing full matches.
# Exclude ambiguous titles/aliases — auto-fixing those could link to the wrong page.
_candidates = []
for mention, target in wm.title_to_file.items():
    # Skip short titles unless they are explicit frontmatter aliases
    if len(mention) <= 3 and mention not in _explicit_aliases:
        continue
    # Skip ambiguous titles or targets (could resolve to multiple pages)
    if wm.is_ambiguous(mention) or wm.is_ambiguous(target):
        continue
    _candidates.append((mention, target))
# Sort longest first so "Tree of Thoughts" matches before "Tree"
_candidates.sort(key=lambda x: len(x[0]), reverse=True)


def _strip_protected(text, protected):
    """Restore protected blocks into a copy (for display only; not used in scanning)."""
    for key, val in protected.items():
        text = text.replace(key, val)
    return text


def _find_unlinked(content, self_bn):
    """Return list of (mention_text, target_basename) for unlinked mentions.

    Scans the body text (after stripping frontmatter, code, comments, and
    existing wikilinks) for occurrences of known titles/aliases.
    """
    # Strip frontmatter
    body = re.sub(r"^---\n.*?\n---\n?", "", content, count=1, flags=re.DOTALL)

    # Replace code blocks and inline code with spaces (preserve offsets)
    protected = {}
    counter = [0]

    def protect(m):
        key = f"\x00P{counter[0]:06d}\x00"
        counter[0] += 1
        protected[key] = " " * len(m.group(0))
        return key

    safe = fence_re.sub(protect, body)
    safe = fence_unclosed_re.sub(protect, safe)  # catch unclosed fences
    safe = inline_code_re.sub(protect, safe)
    safe = comment_re.sub(protect, safe)

    # Replace existing wikilinks with spaces so we don't double-match
    safe = wikilink_re.sub(lambda m: " " * len(m.group(0)), safe)

    # Replace Markdown links/images [text](url) to avoid matching inside them
    safe = _md_link_re.sub(lambda m: " " * len(m.group(0)), safe)

    results = []
    seen_mentions = set()  # avoid reporting same mention twice

    for mention, target in _candidates:
        if target == self_bn:
            continue
        if mention in seen_mentions:
            continue

        # Word-boundary aware search (handles Unicode; also rejects hyphens to avoid
        # false positives on compounds like "pre-processing" matching "processing")
        pattern = re.compile(
            r"(?<![a-zA-Z0-9\-])" + re.escape(mention) + r"(?![a-zA-Z0-9\-])",
            re.UNICODE,
        )
        if pattern.search(safe):
            results.append((mention, target))
            seen_mentions.add(mention)
            # Mask this mention so shorter overlapping candidates don't fire
            safe = pattern.sub(" " * len(mention), safe)

    return results


def _apply_fixes(content, unlinked):
    """Replace bare mention text with [[target|mention]] wikilinks."""
    # Strip frontmatter for body-only processing
    fm_end = 0
    if content.startswith("---\n"):
        m = re.search(r"^---\n.*?\n---\n?", content, re.DOTALL)
        if m:
            fm_end = m.end()
    frontmatter = content[:fm_end]
    body = content[fm_end:]

    # Protect code/comment regions from rewrites
    protected = {}
    counter = [0]

    def protect(m):
        key = f"\x00P{counter[0]:06d}\x00"
        counter[0] += 1
        protected[key] = m.group(0)
        return key

    safe = fence_re.sub(protect, body)
    safe = fence_unclosed_re.sub(protect, safe)  # catch unclosed fences
    safe = inline_code_re.sub(protect, safe)
    safe = comment_re.sub(protect, safe)
    # Also protect existing wikilinks and markdown links
    safe = wikilink_re.sub(protect, safe)
    safe = _md_link_re.sub(protect, safe)

    # Apply replacements (longest mentions first — already sorted)
    # Use escaped pipe in table rows to avoid breaking table layout
    for mention, target in unlinked:
        pattern = re.compile(
            r"(?<![a-zA-Z0-9\-])" + re.escape(mention) + r"(?![a-zA-Z0-9\-])",
            re.UNICODE,
        )
        new_lines = []
        for line in safe.split("\n"):
            in_table = line.lstrip().startswith("|")
            pipe = "\\|" if in_table else "|"
            repl = f"[[{target}{pipe}{mention}]]"
            new_lines.append(pattern.sub(repl, line))
        safe = "\n".join(new_lines)
        # Re-protect newly added wikilinks so they aren't processed again
        safe = wikilink_re.sub(protect, safe)

    # Restore protected regions
    for key, val in protected.items():
        safe = safe.replace(key, val)

    return frontmatter + safe


# ── Main scan ─────────────────────────────────────────────

pages = wm.content_pages()
total_scanned = 0
total_unlinked = 0
total_fixed = 0
total_errors = 0

for md in pages:
    content = read_md(md)
    if content is None:
        relpath = os.path.relpath(md, vault)
        print(f"ERROR:{relpath}\tread error", file=sys.stderr)
        total_errors += 1
        continue
    total_scanned += 1
    self_bn = os.path.splitext(os.path.basename(md))[0]
    relpath = os.path.relpath(md, vault)

    unlinked = _find_unlinked(content, self_bn)
    if not unlinked:
        continue

    total_unlinked += len(unlinked)
    for mention, target in unlinked:
        print(f"UNLINKED:{relpath}\t{mention}\t{target}")

    if fix_mode:
        new_content = _apply_fixes(content, unlinked)
        if new_content != content:
            fd, tmp = tempfile.mkstemp(dir=os.path.dirname(md), suffix=".tmp")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(new_content)
                os.replace(tmp, md)
                total_fixed += len(unlinked)
            except Exception as e:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
                print(f"ERROR:{relpath}\t{e}", file=sys.stderr)
                total_errors += 1

print(f"STATS:scanned={total_scanned} unlinked={total_unlinked} fixed={total_fixed} errors={total_errors}")
if total_errors > 0:
    sys.exit(2)
if total_unlinked > 0 and not fix_mode:
    sys.exit(1)  # issues found but not fixed
# In fix mode, exit 0 if fixes succeeded (errors already caught above)
