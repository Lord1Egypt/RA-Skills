#!/usr/bin/env python3
"""noteclaw html2md.py — OneNote page HTML → markdown snapshot → git commit

Reads manifest.json and cache/pages/<section>/<pageid>.html produced by
graph_sync.py, converts every page into markdown mirrored under store/, then runs
git commit (each snapshot = one commit).

Conversion rules:
- page title authoritative source = manifest (some page HTML lacks <title>, the
  title is given by the Graph API)
- page order = insertion order of pages inside a manifest section (= Graph API
  return order, not creation-time order)
- body headings: h1→#, h2→##, h3→###, h4→#### (levels kept as-is)
- MathML: extract text as far as possible (token concatenation + super/subscript
  and fraction notation), no alt available
- images: [image: <resource-id>] placeholder (the rid is there for a later
  download if needed)
- lists: ol/ul recursion, up to 8 levels deep; treated as a list only when ul
  directly contains li
- div: transparent grouping (OneNote absolute positioning layout), children only
- OneNote line-based layout: no blank line between p elements, block structures
  (headings/lists/tables/rules) get a blank line before and after

Usage:
    python3 html2md.py                  # convert every manifest section and commit
    python3 html2md.py --section <section name>
    python3 html2md.py --no-commit      # convert only, no git snapshot
    python3 html2md.py --commit-msg X
"""
import argparse
import html.parser
import json
import os
import re
import subprocess
import sys
import time

# Working directory = the cwd the command was run from (NOTECLAW_HOME overrides).
NOTECLAW = os.environ.get("NOTECLAW_HOME") or os.getcwd()
STORE_BASE = os.path.join(NOTECLAW, "store")
CACHE_BASE = os.path.join(NOTECLAW, "cache", "pages")
# After loading the manifest, narrow down to the <notebook> subdirectory
# (must match the naming used by graph_sync.py)
STORE_DIR = STORE_BASE
CACHE_DIR = CACHE_BASE
MANIFEST = os.path.join(NOTECLAW, "manifest.json")

BLOCK_TAGS = {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
              "ul", "ol", "li", "table", "tr", "td", "th", "pre", "br"}
LIST_TAGS = {"ul", "ol"}
TABLE_TAGS = {"table", "thead", "tbody", "tr", "td", "th"}
SKIP_TAGS = {"head", "meta", "title", "style", "script"}
INLINE_IMG = re.compile(r"/resources/([^/]+)/\$value")


class Node:
    """Minimal DOM node: tag / attributes / children / text"""
    __slots__ = ("tag", "attrs", "children", "text")

    def __init__(self, tag, attrs=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.children = []
        self.text = ""

    def text_all(self):
        """All visible text under the node (recursive, including #text children)"""
        parts = []
        if self.text:
            parts.append(self.text)
        for c in self.children:
            parts.append(c.text_all())
        return "".join(parts)


class OneNoteParser(html.parser.HTMLParser):
    """Parse OneNote page HTML into a Node tree (transparently ignoring layout
    styling)"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("body")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.stack.append(Node("_skip"))
            return
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        if tag in SKIP_TAGS:
            return
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        if len(self.stack) > 1:
            self.stack.pop()

    def handle_data(self, data):
        # Strip OneNote object replacement characters (U+FFFC) / zero-width
        # characters so they do not pollute the text
        data = data.replace("\ufffc", "").replace("\u200b", "")
        if data.strip():
            # non-blank text → ordered text child node (preserves order against
            # sibling elements)
            tnode = Node("#text")
            tnode.text = data
            self.stack[-1].children.append(tnode)
        else:
            # blank/newline → pile onto the node text (only used to tell whether
            # there is content)
            self.stack[-1].text += data

    def parse(self, html_text):
        self.feed(html_text)
        # penetrate the HTML document wrapper (html>head/body): return the real
        # <body> node
        def find_real_body(n):
            if n.tag == "body" and n is not self.root:
                return n
            for c in n.children:
                r = find_real_body(c)
                if r:
                    return r
            return None
        return find_real_body(self.root) or self.root


# ---------- math → text ----------
MATH_OP_SPACE = {"×", "=", "+", "−", "-", "±", "<", ">", "≤", "≥", "≠",
                 "∈", "→", "⇒", "≈", "÷", "(", ")", ",", ";"}

def math_node_text(node):
    """MathML subtree → readable text (best effort, not LaTeX grade)"""
    def toks(n):
        return n.text_all().strip()
    tag = node.tag
    if tag == "mtext":
        return toks(node)
    if tag in ("mi", "mn", "mo", "ms"):
        t = toks(node)
        return f" {t} " if t in MATH_OP_SPACE and tag == "mo" else t
    if tag == "mspace":
        return " "
    if tag in ("mrow", "math", "mstyle", "merror", "menclose", "semantics", "annotation", "mpadded"):
        parts = []
        for c in node.children:
            if c.tag == "annotation":   # prefer the TeX annotation
                ann = c.text_all().strip()
                if ann:
                    return ann
            parts.append(math_node_text(c))
        s = "".join(parts).strip()
        return s
    if tag == "msup":
        base = math_node_text(node.children[0]) if node.children else ""
        sup = math_node_text(node.children[1]) if len(node.children) > 1 else ""
        return f"{base}^{{{sup}}}"
    if tag == "msub":
        base = math_node_text(node.children[0]) if node.children else ""
        sub = math_node_text(node.children[1]) if len(node.children) > 1 else ""
        return f"{base}_{{{sub}}}"
    if tag == "msubsup":
        return (math_node_text(node.children[0]) + "^{"
                + (math_node_text(node.children[2]) if len(node.children) > 2 else "")
                + "}_{" + (math_node_text(node.children[1]) if len(node.children) > 1 else "") + "}")
    if tag == "mfrac":
        num = math_node_text(node.children[0]) if node.children else ""
        den = math_node_text(node.children[1]) if len(node.children) > 1 else ""
        return f"({num})/({den})"
    if tag == "msqrt":
        return "sqrt(" + "".join(math_node_text(c) for c in node.children) + ")"
    if tag == "mfenced":
        inner = "".join(math_node_text(c) for c in node.children)
        return f"({inner})"
    # fallback: take all text
    return node.text_all().strip()


# ---------- HTML → text lines ----------
def is_blank(s):
    return not s.strip()


class MdRenderer:
    """Node tree → list of markdown lines. Every element yields a flat
    structure of (lines)."""

    def __init__(self):
        self.lines = []
        self.pending_blank = False

    def blank(self):
        self.pending_blank = True

    def emit(self, line):
        if self.pending_blank and self.lines and not is_blank(self.lines[-1]):
            self.lines.append("")
        self.pending_blank = False
        if is_blank(line):
            if self.lines and not is_blank(self.lines[-1]):
                self.lines.append("")
        else:
            self.lines.append(line)

    # ---- inline collection ----
    BLOCK_STOP = {"ul", "ol", "table", "thead", "tbody", "tr", "pre", "li", "br"}

    def inline(self, node_or_list):
        """Return the inline text (for p/h1/td/li and similar contexts).
        Accepts a Node or a list of children; stops descending at block level
        (ul/ol/table/pre/li), which the outer block renderer handles separately;
        math→text, img→placeholder."""
        # if a math/img/br node itself was passed in (li_inline and similar
        # paths), recognize it first
        if hasattr(node_or_list, "tag"):
            t0 = node_or_list.tag
            if t0 == "math":
                return math_node_text(node_or_list)
            if t0 == "img":
                return self.img_placeholder(node_or_list)
            if t0 == "br":
                return ""
        nodes = node_or_list.children if hasattr(node_or_list, "children") else node_or_list
        out = []
        for c in nodes:
            if isinstance(c, str):
                out.append(c)
                continue
            t = c.tag
            if t == "br":
                continue
            if t == "table":
                # nested table (table inside td) → flatten to text (md has no
                # nested tables)
                out.append(collapse_ws(c.text_all()))
                continue
            if t in self.BLOCK_STOP:
                continue
            if t == "math":
                out.append(math_node_text(c))
                continue
            if t == "img":
                out.append(self.img_placeholder(c))
                continue
            if t in ("object", "embed"):
                out.append("[attachment]")
                continue
            if t == "a":
                href = c.attrs.get("href", "")
                # OneNote often writes href as read:https://… or an onenote:
                # internal link
                inner = collapse_ws(self.inline(c))
                if href.startswith("read:"):
                    href = href[5:]
                if href.startswith("http"):
                    if inner == href:
                        out.append(href)   # text is the URL itself, do not repeat
                    else:
                        out.append(f"[{inner}]({href})")
                else:
                    out.append(inner)
                continue
            if c.text:
                out.append(c.text)
            out.append(self.inline(c))
        return "".join(out)

    def collect_inline(self, node):
        """Public wrapper around inline: collapses whitespace"""
        return collapse_ws(self.inline(node))

    # ---- block rendering ----
    def render_children(self, parent):
        i = 0
        kids = parent.children
        while i < len(kids):
            c = kids[i]
            if c.tag == "br":
                i += 1
                continue
            if c.tag in ("p",):
                self.render_p(c)
            elif c.tag == "div":
                self.render_children(c)
            elif c.tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
                self.render_heading(c)
            elif c.tag in LIST_TAGS:
                self.render_list(c)
            elif c.tag == "table":
                self.render_table(c)
            elif c.tag == "pre":
                self.render_pre(c)
            elif c.tag == "img":
                self.emit(self.img_placeholder(c))
            elif c.tag in ("object", "embed"):
                self.emit("[attachment]")
            elif c.tag == "hr":
                self.blank()
                self.lines.append("---")
                self.blank()
            elif c.tag == "math":
                self.emit(math_node_text(c).strip())
            elif c.text.strip():
                # bare text (text directly inside a div)
                for ln in collapse_ws(c.text).splitlines():
                    self.emit(ln)
            elif not any(k.tag in ("p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
                                   "ul", "ol", "table", "pre", "br", "img") for k in c.children):
                # unknown inline container (span/cite/a/strong hanging directly
                # off a block level) → inline the whole thing into one line
                txt = self.collect_inline(c)
                if txt:
                    self.emit(txt)
            else:
                self.render_children(c)
            i += 1

    def render_p(self, node):
        # code block detection: OneNote sometimes renders a whole monospaced code
        # paragraph as p (cannot be told apart reliably, so output as-is)
        parts = self.split_on_br(node)
        first_out = True
        for j, part in enumerate(parts):
            txt = collapse_ws(self.inline(part))
            if not txt:
                continue
            # data-tag marker (OneNote importance tag)
            tagv = node.attrs.get("data-tag", "")
            if tagv:
                txt = f"**[{tagv}]** {txt}"
            if first_out or (self.lines and is_blank(self.lines[-1])):
                self.emit(txt)
                first_out = False
            else:
                # <br> inside p splits paragraphs → new line without a blank line
                # (keeps the line-based layout)
                self.lines.append(txt)

    def split_on_br(self, node):
        """Split the children of a p on <br> into several segments"""
        segs, cur = [], []
        for c in node.children:
            if c.tag == "br":
                if cur:
                    segs.append(cur)
                    cur = []
            else:
                cur.append(c)
        if cur or not segs:
            segs.append(cur)
        return segs

    def render_heading(self, node):
        level = int(node.tag[1])
        txt = self.collect_inline(node)
        if not txt:
            return
        self.blank()
        self.emit("#" * level + " " + txt)

    def render_list(self, node, depth=0):
        ordered = (node.tag == "ol")
        counter = 1
        any_li = any(c.tag == "li" for c in node.children)
        if not any_li:
            # ul wrapping <p> directly (an OneNote quirk) → treat as a plain
            # paragraph flow
            for c in node.children:
                if c.tag == "br":
                    continue
                if c.tag in ("p", "div"):
                    self.render_p(c)
                elif c.tag in LIST_TAGS:
                    self.render_list(c, depth)
                elif c.text and c.text.strip():
                    self.emit(collapse_ws(c.text))
            return
        indent = "    " * depth
        for c in node.children:
            if c.tag != "li":
                continue
            marker = f"{counter}. " if ordered else "- "
            counter += 1
            txt = collapse_ws(self.li_inline(c))
            # skip empty li (only whitespace/newlines)
            nested = self.li_nested_blocks(c)
            if not txt and not nested:
                continue
            if txt:
                self.emit(indent + marker + txt)
            elif nested:
                self.lines.append(indent + marker.rstrip())
            # nested list/table inside li → depth+1
            for kind, sub in nested:
                if kind == "list":
                    self.render_list(sub, depth + 1)
                else:
                    self.render_table(sub)
        self.pending_blank = False

    def li_inline(self, li):
        """Text of the li itself (excluding nested ul/ol/table content; text
        keeps its order via #text child nodes)"""
        return self.inline(li)

    def li_nested_blocks(self, li):
        """Lists/tables nested inside li (penetrating div wrappers)"""
        found = []
        def scan(node):
            for c in node.children:
                if c.tag in LIST_TAGS:
                    found.append(("list", c))
                elif c.tag == "table":
                    found.append(("table", c))
                elif c.tag == "div":
                    scan(c)
        scan(li)
        return found

    def render_table(self, node):
        rows = []
        for tr in node.children:
            if tr.tag != "tr":
                continue
            cells = []
            for td in tr.children:
                if td.tag not in ("td", "th"):
                    continue
                cells.append(collapse_ws(self.inline(td)))
            if cells:
                rows.append(cells)
        if not rows:
            return
        # pad columns for alignment
        ncol = max(len(r) for r in rows)
        rows = [r + [""] * (ncol - len(r)) for r in rows]
        self.blank()
        self.emit("| " + " | ".join(rows[0]) + " |")
        self.emit("|" + "---|" * ncol)
        for r in rows[1:]:
            self.emit("| " + " | ".join(r) + " |")
        self.blank()

    def render_pre(self, node):
        code = node.text_all()
        if not code.strip():
            return
        self.blank()
        self.lines.append("```")
        for ln in code.rstrip("\n").splitlines():
            self.lines.append(ln)
        self.lines.append("```")
        self.blank()

    def img_placeholder(self, node):
        rid = ""
        src = node.attrs.get("data-fullres-src") or node.attrs.get("src") or ""
        m = INLINE_IMG.search(src)
        if m:
            rid = m.group(1)
        return f"[image: {rid}]" if rid else "[image]"


def collapse_ws(s):
    """Collapse runs of whitespace into a single space and strip the ends"""
    return re.sub(r"\s+", " ", s).strip()


# ---------- page conversion ----------
def convert_page(page_id, page_meta, html_text):
    """Single page HTML → markdown text.
    page_meta: {title, lastModifiedDateTime, createdDateTime} (manifest is
    authoritative)
    """
    tree = OneNoteParser().parse(html_text)
    title = page_meta.get("title", "").strip() or "untitled"

    r = MdRenderer()
    r.emit(f"# {title}")
    r.blank()
    r.render_children(tree)
    return "\n".join(r.lines) + "\n", title


def safe_filename(title):
    s = re.sub(r'[/\\:*?"<>|\x00-\x1f]', "_", title).strip()
    return s or "untitled"


def bounded_name(order, title, ext=".md", max_bytes=200):
    """NNN_<title>.ext with the whole name ≤ max_bytes (Linux component limit is
    255 bytes, leaving some margin)"""
    base = f"{order:03d}_"
    t = safe_filename(title)
    while len((base + t + ext).encode("utf-8")) > max_bytes and t:
        t = t[:-1]
    t = t.rstrip(" .")
    if not t:
        return base + "untitled" + ext
    return base + t + ext


def manifest_unusable_msg(why):
    """Single wording used when manifest.json exists but is unusable (the literal
    is kept identical across the three scripts)"""
    return (f"manifest.json is unusable ({why})\n"
            f"  → back it up, delete manifest.json and cold start again: graph_sync.py --all && html2md.py")


def main():
    ap = argparse.ArgumentParser(description="noteclaw HTML→md snapshot")
    ap.add_argument("--section", default=None, help="only convert the given section (relpath)")
    ap.add_argument("--no-commit", action="store_true")
    ap.add_argument("--commit-msg", default=None)
    args = ap.parse_args()

    if not os.path.exists(MANIFEST):
        print("✗ no manifest.json: run graph_sync.py cold start first (--all)", file=sys.stderr)
        sys.exit(2)
    with open(MANIFEST, encoding="utf-8") as f:
        m = json.load(f)
    if m.get("schema") != 3:
        print("✗ " + manifest_unusable_msg(f"schema={m.get('schema')}, needs 3"),
              file=sys.stderr)
        sys.exit(2)
    if not isinstance(m.get("sections"), dict):
        print("✗ " + manifest_unusable_msg("sections missing, file is corrupt"), file=sys.stderr)
        sys.exit(2)

    # Data is grouped per notebook (same layout as graph_sync.py writes)
    global STORE_DIR, CACHE_DIR
    nb = m.get("notebook") or {}
    nb_key = safe_filename(nb.get("displayName") or "")
    STORE_DIR = os.path.join(STORE_BASE, nb_key)
    CACHE_DIR = os.path.join(CACHE_BASE, nb_key)

    sections = m["sections"]
    if args.section:
        hit = [rel for rel in sections if rel == args.section
               or rel.startswith(args.section + os.sep)]
        if not hit:
            print(f"manifest has no section {args.section!r}, available: {list(sections)}")
            sys.exit(1)
        sections = {rel: sections[rel] for rel in hit}

    written, failed, purged = 0, 0, 0
    for rel, sec in sections.items():
        cache_dir = os.path.join(CACHE_DIR, safe_filename(rel))
        pages = list(sec["pages"].items())   # insertion order = API page order
        # orphan cleanup baseline = the artifacts the manifest should have (named
        # by order+title), not the files actually written this run: a page whose
        # html cache is missing/deleted keeps its store snapshot; real orphans
        # caused by a rename/reorder/deletion (present in store but no longer
        # expected by the manifest) are still cleaned up as usual.
        expected = set()
        for order, (_pid, pmeta) in enumerate(pages, 1):
            title = (pmeta.get("title") or "").strip() or "untitled"
            expected.add(os.path.join(rel, bounded_name(order, title)).replace(os.sep, "/"))
        if not os.path.isdir(cache_dir):
            print(f"⚠ cache missing: {cache_dir} (skipping {rel})")
            failed += 1
            continue
        print(f"▸ {rel}  ({len(pages)} pages)")
        for order, (pid, pmeta) in enumerate(pages, 1):
            src = os.path.join(cache_dir, safe_filename(pid) + ".html")
            if not os.path.exists(src):
                print(f"  ✗ html missing: {pid[:30]}… (store snapshot kept, not cleaned)")
                failed += 1
                continue
            with open(src, encoding="utf-8") as f:
                html_text = f.read()
            md, title = convert_page(pid, pmeta, html_text)
            fn = bounded_name(order, title)
            dest_dir = os.path.join(STORE_DIR, rel)
            os.makedirs(dest_dir, exist_ok=True)
            dest = os.path.join(dest_dir, fn)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(md)
            written += 1
        # orphan cleanup: delete files inside this section's store that are not in
        # the manifest's expected artifact list. Only files this tool named itself
        # (NNN_*.md) are deleted: a real orphan from a rename/reorder/deletion
        # always has that shape; files the user put in store are left untouched
        # (otherwise they would be silently deleted).
        sec_store = os.path.join(STORE_DIR, rel)
        if os.path.isdir(sec_store):
            foreign = 0
            for root, _, files in os.walk(sec_store):
                for fn in files:
                    full = os.path.join(root, fn)
                    relp = os.path.relpath(full, STORE_DIR).replace(os.sep, "/")
                    if relp in expected:
                        continue
                    if not re.match(r"^\d+_.*\.md$", fn):
                        foreign += 1
                        continue
                    os.remove(full)
                    print(f"  🧹 orphan cleanup: {relp}")
                    purged += 1
            if foreign:
                print(f"  ↷ keeping {foreign} file(s) not produced by this tool (no cleanup)")

    print(f"\nwrote {written} page(s) → store/ (failed {failed}, orphan cleanup {purged})")
    # a page that did not convert → finish with exit code 1 overall so scheduling
    # jobs/callers notice the snapshot is incomplete; pages that did convert are
    # still written and committed, the snapshot is not lost.
    rc = 1 if failed else 0
    if failed:
        print(f"⚠ {failed} page(s) not converted (html cache missing) — this snapshot is incomplete, exit code 1")

    if args.no_commit:
        print("(--no-commit, skipping git)")
        sys.exit(rc)

    # git check: not only must this be inside a repository, the repository root
    # must be the data directory itself (so that git add -A in a data directory
    # living inside a bigger git repository does not stage the outer files)
    top = subprocess.run(["git", "-C", NOTECLAW, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    if top.returncode != 0:
        print("⚠ the current directory is not a git repository: md was written to store/, committing the snapshot was skipped")
        print("  → for snapshot history: git init && git config user.name <you> && git config user.email <you@x> && git add . && git commit")
        sys.exit(1)
    if os.path.realpath(top.stdout.strip()) != os.path.realpath(NOTECLAW):
        print(f"⚠ data directory {NOTECLAW} lives inside a bigger git repository ({top.stdout.strip()})")
        print("  to avoid committing outer files by mistake, this script does not commit automatically.")
        print("  → run git init in the data directory (see SKILL.md), or cd into the data directory and commit store/ manually")
        sys.exit(1)

    subprocess.run(["git", "add", "-A"], cwd=NOTECLAW, check=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=NOTECLAW)
    if diff.returncode == 0:
        print("store/ unchanged, skipping commit")
        sys.exit(rc)

    ts = time.strftime("%Y-%m-%d %H:%M")
    msg = args.commit_msg or f"snapshot {ts}: {written} page(s) (Graph HTML→md, orphan cleanup {purged})"
    # check the git identity: a missing user.name / user.email always makes commit
    # fail, so warn early in a friendly way
    def git_cfg(key):
        out = subprocess.run(["git", "-C", NOTECLAW, "config", key],
                             capture_output=True, text=True)
        return out.returncode == 0 and bool(out.stdout.strip())

    if not (git_cfg("user.name") and git_cfg("user.email")):
        print("⚠ git identity not configured (user.name / user.email missing), cannot commit the snapshot")
        print("  → run first: git config user.name \"your name\" && git config user.email \"your email\"")
        print("  → then rerun this script to finish the commit; the md files are already in store/ and will not be lost")
        sys.exit(1)
    r = subprocess.run(["git", "commit", "-m", msg], cwd=NOTECLAW, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"⚠ git commit failed: {r.stderr.strip() or r.stdout.strip()}")
        print("  → the md files are already on disk in store/; fix git and rerun this script to commit")
        sys.exit(1)
    print(f"git commit: {msg}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
