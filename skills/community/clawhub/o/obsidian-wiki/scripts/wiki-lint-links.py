#!/usr/bin/env python3
"""Lint and fix wikilink format for Obsidian resolution.

Obsidian resolves wikilinks by FILENAME only, not by frontmatter title or aliases.
Since filenames are kebab-case and links use Title Case, every [[Title]] link
must become [[filename|Title]] for Obsidian to resolve it.

Modes:
  --check     Report format issues without modifying files (default)
  --fix       Apply format fixes to files
  --lint      Full lint: broken links, orphans, format issues (structured output)
  --lint --fix  Full lint + apply format fixes
  --dry-run   Legacy alias for --check

Structured output (--lint mode):
  MAP:<n> entries, <n> known files
  AMBIG:<detail>
  DUPLICATE:<basename>\t<path1>\t<path2>
  BROKEN:<file>\t<link>
  ORPHAN:<file>
  FORMAT:<file>  |  FIXED:<file>
  ERROR:<file>\t<message>
  STATS:broken=<n> orphans=<n> format=<n> ambig=<n> dup=<n> errors=<n>
"""
import os, sys, re, glob, tempfile
from collections import defaultdict

# Ensure wiki_lib is importable from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wiki_lib import (
    WikiMap, read_md, parse_link_target,
    wikilink_re, fence_re, fence_unclosed_re, inline_code_re, comment_re,
)

# ── Argument parsing ──────────────────────────────────────

if "--help" in sys.argv or "-h" in sys.argv:
    print("Usage: python3 wiki-lint-links.py <vault-path> [--check|--fix|--lint]")
    print("Lint and fix wikilink format for Obsidian resolution.")
    print("  --check    Report format issues (default)")
    print("  --fix      Apply format fixes")
    print("  --lint     Full lint: broken links, orphans, format (structured)")
    print("  --dry-run  Legacy alias for --check")
    sys.exit(0)

vault = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else None
if not vault:
    print("Usage: python3 wiki-lint-links.py <vault-path> [--check|--fix|--lint]", file=sys.stderr)
    sys.exit(2)

_known_flags = {"--check", "--fix", "--lint", "--dry-run", "--help", "-h"}
for arg in sys.argv[1:]:
    if arg.startswith("-") and arg not in _known_flags:
        print(f"Error: unknown option '{arg}'", file=sys.stderr)
        sys.exit(2)

fix_mode = "--fix" in sys.argv
lint_mode = "--lint" in sys.argv
check_mode = not fix_mode and not lint_mode

wiki = os.path.join(vault, "wiki")
if not os.path.isdir(wiki):
    print(f"Error: {wiki} not found", file=sys.stderr)
    sys.exit(2)

# ── Phase 1: Build maps (via WikiMap) ─────────────────────

wm = WikiMap(vault)

# Expose maps used by rewrite_link / process_file below
title_to_file    = wm.title_to_file
file_to_title    = wm.file_to_title
known_files      = wm.known_files
_warnings        = wm.warnings
ambiguous_titles = wm._ambiguous_titles
_ambiguous_basenames = wm._ambiguous_basenames

def resolve_target(target):
    return wm.resolve_target(target)

def extract_links(filepath):
    return wm.extract_links(filepath)

# ── Phase 2: Link extraction and rewriting ────────────────

counters = {"rewrites": 0, "ambiguities": 0, "errors": 0}


def rewrite_link(match, in_table=False):
    """Rewrite a wikilink to canonical [[filename|Title]] format."""
    inner = match.group(1)
    if "\\|" in inner:
        parts = inner.split("\\|", 1)
        target_full, display = parts[0], (parts[1] if len(parts) > 1 else None)
        pipe_sep = "\\|"
    elif "|" in inner:
        target_full, display = inner.split("|", 1)
        pipe_sep = "\\|" if in_table else "|"
    else:
        target_full, display, pipe_sep = inner, None, ("\\|" if in_table else "|")

    if "#" in target_full:
        target, section = target_full.split("#", 1)[0], "#" + target_full.split("#", 1)[1]
    else:
        target, section = target_full, ""

    status, resolved = resolve_target(target)
    if status == "ambiguous":
        counters["ambiguities"] += 1
        return match.group(0)
    if status == "broken":
        return match.group(0)

    # Link resolves — determine if rewrite is needed
    if target != resolved:
        counters["rewrites"] += 1
        disp = display if display else file_to_title.get(resolved, target)
        return f"[[{resolved}{section}{pipe_sep}{disp}]]"
    # Table context: ensure escaped pipe even when target is already canonical
    if in_table and display is not None and "|" in match.group(0) and "\\|" not in match.group(0):
        counters["rewrites"] += 1
        return f"[[{resolved}{section}\\|{display}]]"
    if display is None and resolved in file_to_title:
        counters["rewrites"] += 1
        return f"[[{resolved}{section}{pipe_sep}{file_to_title[resolved]}]]"
    return match.group(0)


def process_file(md):
    """Process a single file for format issues. Returns True if content changed."""
    original = read_md(md)
    if original is None:
        raise OSError(f"cannot read {md}")

    protected = {}
    _prot_counter = [0]

    def protect(m):
        key = f"\x00P{_prot_counter[0]:06d}\x00"
        _prot_counter[0] += 1
        protected[key] = m.group(0)
        return key

    safe = fence_re.sub(protect, original)
    safe = fence_unclosed_re.sub(protect, safe)  # catch unclosed fences
    safe = inline_code_re.sub(protect, safe)
    safe = comment_re.sub(protect, safe)

    new_lines = []
    for line in safe.split("\n"):
        stripped = line.lstrip()
        in_table = stripped.startswith("|")

        def _rewrite(match, _t=in_table):
            return rewrite_link(match, _t)

        new_lines.append(wikilink_re.sub(_rewrite, line))
    new_content = "\n".join(new_lines)

    for key, val in protected.items():
        new_content = new_content.replace(key, val)

    if new_content != original:
        if fix_mode:
            fd, tmp = tempfile.mkstemp(dir=os.path.dirname(md), suffix=".tmp")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(new_content)
                os.replace(tmp, md)
            except Exception:
                os.unlink(tmp)
                raise
        return True
    return False


# ── Execution ─────────────────────────────────────────────

if __name__ == "__main__":
    all_mds = sorted(glob.glob(os.path.join(wiki, "**", "*.md"), recursive=True))
    all_mds = [md for md in all_mds if os.path.isfile(md)]
    special_root = {os.path.join(wiki, "index.md"), os.path.join(wiki, "log.md")}
    all_mds = [md for md in all_mds if md not in special_root]

    if lint_mode:
        # --- Structured output for wiki-lint.sh ---

        print(f"MAP:{len(title_to_file)} entries, {len(known_files)} known files")

        dup_count = 0
        map_ambig_count = 0
        build_errors = 0
        for w in _warnings:
            if w[0] == "DUPLICATE":
                print(f"DUPLICATE:{w[1]}\t{w[2]}\t{w[3]}")
                dup_count += 1
            elif w[0].startswith("AMBIG"):
                print(f"AMBIG:{w[1]} maps to both {w[2]} and {w[3]}")
                map_ambig_count += 1
            elif w[0] == "SKIP":
                print(f"ERROR:{w[1]}\t{w[2]}")
                build_errors += 1

        # Pass 1: broken links + orphan detection
        # Design: links FROM index.md and log.md are excluded from inbound tracking
        # because these are auto-generated pages. A page linked only from the
        # auto-generated index is still considered orphan.
        inbound = defaultdict(set)
        broken = []
        for md in all_mds:
            bn = os.path.splitext(os.path.basename(md))[0]
            relpath = os.path.relpath(md, vault)
            for target in extract_links(md):
                status, resolved = resolve_target(target)
                if status == "broken":
                    broken.append((relpath, target))
                elif resolved:
                    # Track inbound even for ambiguous (lenient orphan detection)
                    if resolved != bn:
                        inbound[resolved].add(bn)

        orphans = sorted(
            wm._basename_paths[bn]
            for bn in known_files
            if bn not in ("index", "log")
            and not inbound.get(bn)
            and bn in wm._basename_paths
        )

        # Pass 2: format issues
        format_files = []
        for md in all_mds:
            try:
                if process_file(md):
                    format_files.append(os.path.relpath(md, vault))
            except Exception as e:
                counters["errors"] += 1
                print(f"ERROR:{os.path.relpath(md, vault)}\t{e}")

        # Output structured results
        for relpath, link in broken:
            print(f"BROKEN:{relpath}\t{link}")
        for orphan in orphans:
            print(f"ORPHAN:{orphan}")
        tag = "FIXED" if fix_mode else "FORMAT"
        for relpath in format_files:
            print(f"{tag}:{relpath}")

        total_ambig = counters['ambiguities'] + map_ambig_count
        total_errors = counters['errors'] + build_errors
        print(
            f"STATS:broken={len(broken)} orphans={len(orphans)} "
            f"format={len(format_files)} ambig={total_ambig} "
            f"dup={dup_count} errors={total_errors}"
        )

        if total_errors > 0:
            sys.exit(2)
        if broken or orphans or format_files or total_ambig or dup_count:
            sys.exit(1)

    else:
        # --- Human-readable output (backward-compatible --check / --fix) ---

        for w in _warnings:
            if w[0] == "DUPLICATE":
                print(f"  \u26a0\ufe0f  DUPLICATE BASENAME: '{w[1]}' exists at {w[2]} and {w[3]}")
            elif w[0] == "AMBIG_TITLE":
                print(f"  \u26a0\ufe0f  AMBIGUOUS: '{w[1]}' maps to both {w[2]} and {w[3]} (keeping {w[3]})")
            elif w[0] == "AMBIG_ALIAS":
                print(f"  \u26a0\ufe0f  AMBIGUOUS: alias '{w[1]}' maps to both {w[2]} and {w[3]} (keeping {w[3]})")
            elif w[0] == "AMBIG_CI":
                print(f"  \u26a0\ufe0f  AMBIGUOUS: title '{w[1]}' maps to both {w[2]} and {w[3]} (case-insensitive)")
            elif w[0] == "AMBIG_FILE":
                print(f"  \u26a0\ufe0f  AMBIGUOUS: filename '{w[1]}' maps to both {w[2]} and {w[3]}")
            elif w[0] == "SKIP":
                print(f"  \u26a0\ufe0f  SKIP (read error): {w[1]}: {w[2]}")

        print(f"Link map: {len(title_to_file)} entries, {len(known_files)} known files")

        for md in all_mds:
            try:
                if process_file(md):
                    relpath = os.path.relpath(md, vault)
                    if check_mode:
                        print(f"  WOULD REWRITE: {relpath}")
                    else:
                        print(f"  REWRITTEN: {relpath}")
            except Exception as e:
                counters["errors"] += 1
                print(f"  \u274c ERROR processing {os.path.relpath(md, vault)}: {e}", file=sys.stderr)

        print(f"\nTotal rewrites: {counters['rewrites']}")
        if counters["ambiguities"] > 0:
            print(f"Ambiguous links skipped: {counters['ambiguities']}")
        if counters["errors"] > 0:
            print(f"Processing errors: {counters['errors']}")
        if check_mode:
            print("(check mode \u2014 no files changed)")
        if counters["errors"] > 0:
            sys.exit(2)
        if counters["rewrites"] > 0 or counters["ambiguities"] > 0:
            sys.exit(1)
