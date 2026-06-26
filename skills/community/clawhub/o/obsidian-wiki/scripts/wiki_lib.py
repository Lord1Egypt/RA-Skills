#!/usr/bin/env python3
"""wiki_lib.py — Shared library for obsidian-wiki scripts.

NOT a standalone script. Imported by:
  - wiki-lint-links.py
  - wiki-crosslink.py
  - wiki-graph.py

Exports:
  read_md(path)           — read + CRLF-normalize a markdown file
  parse_link_target(inner) — extract target from wikilink inner text
  wikilink_re, fence_re, fence_unclosed_re, inline_code_re, comment_re, frontmatter_re  — shared regexes
  WikiMap(vault_path)     — build title/alias/filename maps + resolve
"""
import os, re, glob
from collections import defaultdict

# ── Shared regexes ────────────────────────────────────────

wikilink_re    = re.compile(r"\[\[([^\]]+)\]\]")
fence_re       = re.compile(r"^ {0,3}(`{3,}|~{3,}).*?^ {0,3}\1", re.MULTILINE | re.DOTALL)  # CommonMark: 0-3 leading spaces, matched types
fence_unclosed_re = re.compile(r"^ {0,3}(?:`{3,}|~{3,}).*", re.MULTILINE | re.DOTALL)  # fallback for unclosed fences
inline_code_re = re.compile(r"(`+)(?!`)(.+?)\1")  # handles 1+ backtick delimiters
comment_re     = re.compile(r"%%.*?%%", re.DOTALL)
frontmatter_re = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def read_md(path):
    """Read a markdown file, normalizing CRLF. Returns content or None on error."""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError):
        return None


def parse_link_target(inner):
    """Extract target from wikilink inner text (strips display text and section)."""
    if "\\|" in inner:
        target_full = inner.split("\\|", 1)[0]
    elif "|" in inner:
        target_full = inner.split("|", 1)[0]
    else:
        target_full = inner
    return target_full.split("#", 1)[0] if "#" in target_full else target_full


class WikiMap:
    """Build and query the title/alias/filename maps for a wiki vault.

    Attributes (public):
        vault_path          — absolute path to vault root
        wiki_path           — absolute path to vault/wiki/
        title_to_file       — {title_or_alias: basename}  (case-sensitive)
        file_to_title       — {basename: title}
        known_files         — set of all basenames in wiki/**/*.md
        warnings            — list of (kind, *args) tuples collected during build

    Methods:
        resolve_target(target) → (status, canonical_filename)
        extract_links(filepath) → [target, ...]
        content_pages()        → sorted list of .md paths (excl. index.md, log.md)
    """

    def __init__(self, vault_path):
        self.vault_path = os.path.abspath(vault_path)
        self.wiki_path  = os.path.join(self.vault_path, "wiki")

        self.title_to_file  = {}
        self.file_to_title  = {}
        self.known_files    = set()
        self.warnings       = []

        # Internal state
        self._ambiguous_titles      = set()
        self._ambiguous_basenames   = set()  # basenames with duplicate paths only
        self._basename_paths        = {}
        self._lower_to_canonical    = {}
        self._title_to_file_lower   = {}

        self._build_maps()

    # ── Build Phase ───────────────────────────────────────

    def _build_maps(self):
        wiki = self.wiki_path
        title_to_file   = self.title_to_file
        file_to_title   = self.file_to_title
        warnings        = self.warnings
        ambiguous_titles = self._ambiguous_titles

        # 1. Title + alias maps (ordered subdirs only)
        for subdir in ["sources", "entities", "syntheses", "concepts", "reports"]:
            for md in sorted(glob.glob(os.path.join(wiki, subdir, "*.md"))):
                if not os.path.isfile(md):
                    continue
                bn = os.path.splitext(os.path.basename(md))[0]
                if bn in ("index", "log"):
                    continue
                content = read_md(md)
                if content is None:
                    warnings.append(("SKIP", os.path.relpath(md, self.vault_path), "read error"))
                    continue
                fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
                fm = fm_match.group(1) if fm_match else ""

                # title:
                m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
                if m:
                    title = m.group(1)
                    if title in title_to_file and title_to_file[title] != bn:
                        warnings.append(("AMBIG_TITLE", title, title_to_file[title], bn))
                        ambiguous_titles.add(title)
                    title_to_file[title] = bn
                    file_to_title[bn] = title

                # aliases:
                m = re.search(r"^aliases:\s*\[(.+?)\]\s*$", fm, re.MULTILINE)
                if m:
                    for alias in m.group(1).split(","):
                        alias = alias.strip().strip("'\"")
                        if alias:
                            if alias in title_to_file and title_to_file[alias] != bn:
                                warnings.append(("AMBIG_ALIAS", alias, title_to_file[alias], bn))
                                ambiguous_titles.add(alias)
                            title_to_file[alias] = bn

        # 2. Case-insensitive shadow map
        title_to_file_lower = self._title_to_file_lower
        for k, v in title_to_file.items():
            kl = k.lower()
            if kl in title_to_file_lower and title_to_file_lower[kl] != v:
                warnings.append(("AMBIG_CI", k, title_to_file_lower[kl], v))
                ambiguous_titles.add(k)
                for orig_k, orig_v in title_to_file.items():
                    if orig_k.lower() == kl and orig_v == title_to_file_lower[kl]:
                        ambiguous_titles.add(orig_k)
                        break
            title_to_file_lower[kl] = v

        # 3. All known filenames (detect duplicate basenames)
        known_files      = self.known_files
        basename_paths   = self._basename_paths
        ambiguous_bns    = self._ambiguous_basenames
        for md in glob.glob(os.path.join(wiki, "**", "*.md"), recursive=True):
            if os.path.isfile(md):
                bn      = os.path.splitext(os.path.basename(md))[0]
                relpath = os.path.relpath(md, self.vault_path)
                if bn in basename_paths:
                    warnings.append(("DUPLICATE", bn, basename_paths[bn], relpath))
                    ambiguous_titles.add(bn)
                    ambiguous_bns.add(bn)
                else:
                    basename_paths[bn] = relpath
                known_files.add(bn)

        # 4. Case-insensitive filename map
        lower_to_canonical = self._lower_to_canonical
        for f in sorted(known_files):
            fl = f.lower()
            if fl in lower_to_canonical and lower_to_canonical[fl] != f:
                warnings.append(("AMBIG_FILE", fl, lower_to_canonical[fl], f))
                ambiguous_titles.add(fl)
            lower_to_canonical[fl] = f

        # Recompute lowercase ambiguity set after all passes
        self._ambiguous_titles_lower = {t.lower() for t in ambiguous_titles}

    # ── Public API ────────────────────────────────────────

    def is_ambiguous(self, name):
        """Check if a title, alias, or filename is ambiguous (maps to multiple pages)."""
        return (name in self._ambiguous_titles
                or name.lower() in self._ambiguous_titles_lower
                or name in self._ambiguous_basenames)

    # ── Resolution ────────────────────────────────────────

    def resolve_target(self, target):
        """Resolve a wikilink target to a known filename.

        Returns (status, canonical_filename) where status is one of:
          "exact"     — target is a known filename
          "ci-file"   — case-insensitive filename match
          "title"     — matched via title or alias
          "ambiguous" — multiple candidates
          "broken"    — no match found
        """
        ambiguous_titles       = self._ambiguous_titles
        ambiguous_titles_lower = self._ambiguous_titles_lower
        known_files            = self.known_files
        ambiguous_bns          = self._ambiguous_basenames
        lower_to_canonical     = self._lower_to_canonical
        title_to_file          = self.title_to_file
        title_to_file_lower    = self._title_to_file_lower

        # 1. Exact filename match
        if target in known_files:
            if target in ambiguous_bns:
                return ("ambiguous", target)
            return ("exact", target)

        # 2. Case-insensitive filename match
        if target.lower() in lower_to_canonical:
            canonical = lower_to_canonical[target.lower()]
            if canonical in ambiguous_titles or canonical.lower() in ambiguous_titles_lower:
                return ("ambiguous", canonical)
            return ("ci-file", canonical)

        # 3. Title/alias match (case-sensitive, then case-insensitive)
        fn = title_to_file.get(target) or title_to_file_lower.get(target.lower())
        if fn:
            if (target in ambiguous_titles or target.lower() in ambiguous_titles_lower
                    or fn in ambiguous_titles or fn.lower() in ambiguous_titles_lower):
                return ("ambiguous", fn)
            return ("title", fn)

        # 4. No match
        return ("broken", None)

    # ── Link extraction ───────────────────────────────────

    def extract_links(self, filepath):
        """Extract unique wikilink targets from a file, skipping code/comments."""
        content = read_md(filepath)
        if content is None:
            return []
        content = fence_re.sub("", content)
        content = fence_unclosed_re.sub("", content)  # catch unclosed fences
        content = inline_code_re.sub("", content)
        content = comment_re.sub("", content)
        seen   = set()
        result = []
        for m in wikilink_re.finditer(content):
            t = parse_link_target(m.group(1))
            if t and t not in seen:
                seen.add(t)
                result.append(t)
        return result

    # ── Page enumeration ──────────────────────────────────

    def content_pages(self):
        """Return sorted list of .md paths in wiki/, excluding index.md and log.md."""
        wiki = self.wiki_path
        special = {
            os.path.join(wiki, "index.md"),
            os.path.join(wiki, "log.md"),
        }
        pages = []
        for md in glob.glob(os.path.join(wiki, "**", "*.md"), recursive=True):
            if os.path.isfile(md) and md not in special:
                pages.append(md)
        return sorted(pages)
