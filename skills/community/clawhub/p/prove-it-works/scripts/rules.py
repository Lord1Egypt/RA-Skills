#!/usr/bin/env python3
"""Project rules for Prove It Works.

Usage:
  python3 rules.py <repo> [--json]
      List the written rules found in CLAUDE.md, AGENTS.md, .cursorrules,
      .cursor/rules/*, .github/copilot-instructions.md, CONTRIBUTING.md,
      .windsurfrules and .shipsnag/rules.md: which became mechanical checks and
      which Claude must check by reading.

  python3 rules.py add --repo DIR --kind grep|forbid-path|require-cmd \
      --pattern PATTERN --why "what went wrong" [--glob GLOB]
      Never Twice: append a rule to <repo>/.shipsnag/rules.md, then dry-run it
      against the current change. The rule runs on every later proof.

Read-only except <repo>/.shipsnag/rules.md. Standard library only.
"""

import argparse
import json
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import (CODE_EXT, split_cmd, JS_EXT, JS_LOCKS, PY_EXT, TS_EXT, base_of, command_is_safe,  # noqa: E402
                    ext_of, finding, glob_match, is_comment_line, is_doc, is_test_path, load_change,
                    no_em_dash, posix, read_text, run_cmd, tail, today, PATH_TOKEN_RE)

RULE_FILES = [
    "CLAUDE.md", ".claude/CLAUDE.md", "CLAUDE.local.md", "AGENTS.md", "AGENT.md", "GEMINI.md",
    ".cursorrules", ".windsurfrules", ".github/copilot-instructions.md", "CONTRIBUTING.md",
    ".github/CONTRIBUTING.md", "docs/CONTRIBUTING.md",
]
RULE_DIRS = [(".cursor/rules", (".md", ".mdc")), (".windsurf/rules", (".md",)),
             (".github/instructions", (".md",)), (".claude/rules", (".md",))]
NEVER_TWICE = ".shipsnag/rules.md"

DIRECTIVE_RE = re.compile(
    r"\b(must|never|always|don't|do not|dont|should|shouldn't|avoid|prefer|only|required?|"
    r"forbidden|not allowed|make sure|ensure|use|run|keep|no)\b", re.I)
NEG_RE = re.compile(r"\b(never|don't|dont|do not|must not|mustn't|should not|shouldn't|"
                    r"no longer|not allowed|forbidden|banned|avoid|cannot|can't)\b", re.I)
CLAUSE_SPLIT_RE = re.compile(r"[;(]|\binstead\b|\bprefer\b|\brather\b|\bbut\b|,\s*(?:use|prefer|call|import)\b|\.\s+", re.I)
PMS = ("pnpm", "yarn", "bun", "npm")
CODE_WORDS = {"any", "var", "eval", "debugger", "alert", "innerhtml", "dangerouslysetinnerhtml",
              "settimeout", "setinterval", "document.write", "print", "console", "!important",
              "export default", "default export", "default exports", "ts-ignore", "@ts-ignore",
              "as any", "require", "with", "goto", "exec", "pickle", "assert"}
PKG_RE = re.compile(r"^@?[a-z0-9][a-z0-9._\-]*(/[a-z0-9._\-]+)?$")
TEXT_SUBJECT_RE = re.compile(r"\b(?:user[- ]facing|customer[- ]facing|reply|replies|response|error|ui|display|output|cli|bot|"
                             r"chat|ux|status|help|prompt|log|i18n)(?:\s+[a-z-]+)?\s+(?:texts?|messages?|strings?|copy|wording)\b", re.I)
TEXT_FREEZE_RE = re.compile(r"\b(?:part of the (?:contract|api|public api|interface)|are (?:a|the) contract|is (?:a|the) contract|"
                            r"(?:don't|do not|never|must not|mustn't|should not) (?:change|edit|reword|rephrase|alter)|"
                            r"change (?:them|it|these|those) only|only (?:be )?changed? (?:them |it )?when|"
                            r"keep (?:them|it|these|those) (?:stable|unchanged|as is|verbatim)|(?:are|is) frozen|parse[sd]? (?:them|it|these))\b",
                            re.I)
TASK_REWORD_RE = re.compile(r"\b(?:reword|rephrase|rewrite|rename|change|update|fix|edit|improve|translate)\b[^.\n]{0,40}"
                            r"\b(?:texts?|messages?|wording|copy|strings?|replies|reply text|labels?|error messages?)\b", re.I)
LITERAL_RE = re.compile(r"'((?:[^'\\\n]|\\.)*)'|\"((?:[^\"\\\n]|\\.)*)\"|`((?:[^`\\\n]|\\.)*)`")


# ---------------------------------------------------------------------------
# Finding rule files and sentences
# ---------------------------------------------------------------------------

def find_rule_files(repo):
    out = []
    seen = set()
    for rel in RULE_FILES:
        p = os.path.join(repo, rel)
        if os.path.isfile(p) and rel.lower() not in seen:
            seen.add(rel.lower())
            txt = read_text(p)
            if txt is not None:
                out.append((rel, txt))
    for d, exts in RULE_DIRS:
        full = os.path.join(repo, d)
        if os.path.isdir(full):
            for fn in sorted(os.listdir(full)):
                if fn.lower().endswith(exts):
                    txt = read_text(os.path.join(full, fn))
                    if txt is not None:
                        out.append((posix(os.path.join(d, fn)), txt))
    return out


def _units(text):
    """Logical prose units: a bullet plus its wrapped continuation lines, or a wrapped paragraph
    line. A continuation is an indented line, or one that starts in lower case or with a backtick
    (a sentence that wraps). Yields (first_line_no, text, is_bullet)."""
    lines = text.splitlines()
    in_code = False
    in_front = bool(lines) and lines[0].strip() == "---"
    cur = None
    for i, raw in enumerate(lines, 1):
        s = raw.strip()
        if in_front:
            if i > 1 and s == "---":
                in_front = False
            continue
        if s.startswith("```") or s.startswith("~~~"):
            if cur:
                yield cur
                cur = None
            in_code = not in_code
            continue
        if in_code or not s or s.startswith("#") or s.startswith("<!--") or s.startswith("|"):
            if cur:
                yield cur
                cur = None
            if s.startswith("|") and not s.startswith("|---") and not in_code:
                yield (i, s.strip("|").strip(), False)
            continue
        bullet = bool(re.match(r"^(?:[-*+]|\d+[.)])\s+", s))
        if bullet:
            if cur:
                yield cur
            cur = (i, re.sub(r"^(?:[-*+]|\d+[.)])\s+(\[[ xX]\]\s+)?", "", s), True)
            continue
        cont = cur is not None and (raw[:1] in (" ", "\t") or re.match(r"^[a-z`(]", s))
        if cont:
            cur = (cur[0], cur[1] + " " + s, cur[2])
            continue
        if cur:
            yield cur
        cur = (i, s, False)
    if cur:
        yield cur


def sentences(text):
    """Yield (line_no, sentence, is_bullet) for prose, skipping code fences and frontmatter.
    Wrapped lines are joined first, so a rule split over two lines is read as one sentence."""
    for i, s, bullet in _units(text):
        for part in re.split(r"(?<=[.!?])\s+(?=[A-Z`*])", s):
            part = part.strip()
            if len(part) >= 6:
                yield i, part, bullet


# ---------------------------------------------------------------------------
# Converting sentences into checks
# ---------------------------------------------------------------------------

def _ticks(s):
    return [t.strip() for t in re.findall(r"`([^`]+)`", s) if t.strip()]


def _is_pathish(tok):
    t = tok.strip()
    if " " in t or t.startswith(("-", "$")):
        return False
    if "/" in t or "*" in t:
        return True
    return bool(re.match(r"^[\w.@\-]+\.(js|mjs|cjs|jsx|ts|tsx|py|rb|go|rs|java|sql|json|ya?ml|toml|md|css|scss|html|vue|svelte|sh|lock|prisma|proto|graphql|env|txt)$", t)) \
        or t.startswith(".") and len(t) > 1 and not t.startswith("..")


def _is_command(tok):
    t = tok.strip()
    first = t.split()[0] if t.split() else ""
    return (" " in t or first in ("make",)) and first in (
        "npm", "pnpm", "yarn", "bun", "make", "python", "python3", "node", "pytest", "ruff", "mypy",
        "tsc", "eslint", "cargo", "go", "deno", "uv", "poetry", "just", "npx", "pre-commit", "pyright",
        "flake8", "black", "prettier", "biome", "vitest", "jest", "golangci-lint", "rubocop", "bundle")


def _grep_regex(tok):
    low = tok.lower()
    if low in ("any", "as any", ": any"):
        return r"(?::\s*|\bas\s+|<)any\b", "ts"
    if low in ("print", "print()", "print("):
        return r"(?<![\w.])print\s*\(", "py"
    if low in ("@ts-ignore", "ts-ignore"):
        return r"@ts-ignore", None
    if low in ("default export", "default exports", "export default"):
        return r"\bexport\s+default\b", "js"
    if low in ("var",):
        return r"(?<![\w.$])var\s+[A-Za-z_$]", "js"
    t = tok.rstrip("()")
    rx = re.escape(t)
    if re.match(r"\w", t):
        rx = r"(?<![\w$])" + rx
    if re.search(r"\w$", t):
        rx += r"(?![\w$])"
    if tok.endswith("()") or tok.endswith("("):
        rx += r"\s*\("
    return rx, None


def import_regex(pkg):
    p = re.escape(pkg)
    return (r"(?:\bfrom\s+['\"]%s(?:/[^'\"]*)?['\"]|\brequire\s*\(\s*['\"]%s(?:/[^'\"]*)?['\"]\s*\)|"
            r"\bimport\s*\(?\s*['\"]%s(?:/[^'\"]*)?['\"]|^\s*import\s+%s(?:\.\w+)*(?:\s|,|$)|"
            r"^\s*from\s+%s(?:\.\w+)*\s+import\b)" % (p, p, p, p.replace("\\-", "_"), p.replace("\\-", "_")))


def convert_sentence(src, line, s):
    """Return (mechanical_rules, is_directive)."""
    out = []
    low = s.lower()
    ticks = _ticks(s)
    neg = NEG_RE.search(low)
    directive = bool(DIRECTIVE_RE.search(low))
    where = "%s:%d" % (src, line)
    # 0. User-facing text is a contract ("reply texts are part of the contract; change them only when
    #    the task says so", "don't change error messages, clients parse them"). Checked against the
    #    task, so "unless the task asks" is built in.
    if TEXT_SUBJECT_RE.search(s) and TEXT_FREEZE_RE.search(s) and not re.search(r"\bcommit messages?\b", low) and \
            not any(_is_pathish(t) for t in ticks):
        out.append({"kind": "keep-text", "source": where, "text": s})
        return out, True
    if re.search(r"\b(except|unless|when needed|if needed|where possible|if possible|when possible)\b", low):
        return out, directive

    # 1. Package manager
    pos = set()
    for m in re.finditer(r"\b(use|using|uses|always use|only use|run with|we use|prefer)\s+(?:only\s+)?`?(pnpm|yarn|bun|npm)`?(?![\w-])", low):
        before = low[max(0, m.start() - 14):m.start()]
        if not NEG_RE.search(before):
            pos.add(m.group(2))
    for m in re.finditer(r"`?(pnpm|yarn|bun|npm)`?\s+only\b", low):
        pos.add(m.group(1))
    negpm = set()
    for m in re.finditer(r"\b(?:never|don't|dont|do not|must not|should not|not)\s+(?:use\s+|with\s+)?`?(pnpm|yarn|bun|npm|npx)`?(?![\w-])(?!\s+(?:install|i|add|run|publish|test|exec|dlx|x|ci|start|build|audit|update|upgrade|remove|link|pack|version|init|create|dedupe|prune|outdated)\b)", low):
        negpm.add("npm" if m.group(1) == "npx" else m.group(1))
    for m in re.finditer(r"`?(pnpm|yarn|bun|npm)`?\s*(?:,|or|and)\s*`?(pnpm|yarn|bun|npm)`?(?![\w-])(?!\s+(?:install|i|add|run|publish|test|exec|dlx|x|ci|start|build|audit|update|upgrade|remove|link|pack|version|init|create|dedupe|prune|outdated)\b)", low):
        before = low[max(0, m.start() - 25):m.start()]
        if re.search(r"\b(?:never|don't|dont|do not|must not|should not|not)\s+(?:use\s+)?$", before):
            negpm |= {m.group(1), m.group(2)}
    if len(pos) == 1 or negpm:
        req = list(pos)[0] if len(pos) == 1 else None
        forb = set(negpm)
        if req:
            forb |= set(p for p in PMS if p != req)
        forb.discard(req)
        if forb:
            out.append({"kind": "pm", "pm": req, "forbid": sorted(forb), "source": where, "text": s})

    # 2. Required commands
    if re.search(r"\b(run|runs|execute|pass|passes|green|succeed)\b", low) and \
            re.search(r"\b(always|must|before|after|make sure|ensure|should|required|need to|needs to|every)\b", low):
        for t in ticks:
            if _is_command(t) and re.search(r"test|lint|check|build|typecheck|type-check|types|tsc|mypy|pyright|ruff|flake8|eslint|"
                                            r"pytest|unittest|vet|clippy|verify|validate|format|fmt|prettier|biome|\bci\b", t, re.I) and \
                    not re.search(r"\b(install|add|setup|bootstrap|init|dev|start|serve|watch|publish|deploy)\b", t):
                pre = low[:low.find(t.lower())] if t.lower() in low else ""
                if NEG_RE.search(pre[-30:]):
                    continue
                out.append({"kind": "require-cmd", "pattern": t, "source": where, "text": s,
                            "safe": command_is_safe(t)})

    # 3. Paths that must not be edited
    edit_neg = re.search(r"\b(never|don't|dont|do not|must not|should not|shouldn't|no)\s+(?:\w+\s+){0,2}?"
                         r"(edit|edits|modify|modifying|change|changing|touch|update|write to|hand-edit|alter|commit)\b", low)
    generated = re.search(r"\b(auto-?generated|generated (?:by|from|code|files?|automatically)|are generated|is generated|read-only|readonly|do not edit|don't edit)\b", low)
    if (edit_neg or generated) and re.search(r"\b(api|behaviou?r|signature|interface|contract|semantics|output|format)\s+of\b", low):
        edit_neg = generated = None
    if edit_neg or generated:
        # "X is generated from Y by Z": X is protected, Y is the source; "never edit X": tokens after the verb
        scope_txt = ""
        if generated:
            scope_txt += s[:generated.start()] + " "
        if edit_neg:
            scope_txt += s[edit_neg.end():]
        toks = [t for t in _ticks(scope_txt) if _is_pathish(t) and not _is_command(t)]
        if not toks and not _ticks(scope_txt):
            toks = [m.group(0) for m in PATH_TOKEN_RE.finditer(scope_txt) if not m.group(0).startswith("http")]
        for t in toks:
            t = t.strip().lstrip("./") if t.startswith("./") else t.strip()
            if t in ("/", "*", "**"):
                continue
            out.append({"kind": "forbid-path", "pattern": t, "source": where, "text": s})

    # 4. Forbidden imports and patterns
    if neg and not edit_neg and not any(r["kind"] == "pm" for r in out):
        verb_m = re.search(r"\b(import|imports|importing|require|requires|depend on|add|adding|use|using|call|calling|introduce|no)\b", low[neg.start():])
        if verb_m:
            clause_start = neg.start() + verb_m.start()
            rest = s[clause_start:]
            cut = CLAUSE_SPLIT_RE.search(rest[3:])
            clause = rest[:cut.start() + 3] if cut else rest
            verb = verb_m.group(1)
            ctoks = _ticks(clause)
            scope = None
            for m in re.finditer(r"\b(?:in|inside|under|within|from)\s+`([^`]+)`", clause):
                if _is_pathish(m.group(1)):
                    scope = m.group(1)
            for t in ctoks:
                if t == scope or _is_command(t) or (_is_pathish(t) and "/" in t):
                    continue
                if t.lower() in PMS:
                    continue
                tl = t.lower()
                is_pkg = bool(PKG_RE.match(t)) and tl not in CODE_WORDS
                if verb.startswith(("import", "require", "depend", "add")) and is_pkg:
                    out.append({"kind": "forbid-import", "pattern": t, "glob": scope, "source": where, "text": s})
                elif verb.startswith(("use", "using", "call", "no", "introduce")) and is_pkg and "." not in t:
                    out.append({"kind": "forbid-import", "pattern": t, "glob": scope, "source": where, "text": s})
                else:
                    rx, lang = _grep_regex(t)
                    out.append({"kind": "grep", "pattern": rx, "lang": lang, "glob": scope, "source": where,
                                "text": s, "literal": t})

    # 5. File naming
    styles = []
    for name, rx in (("kebab-case", r"kebab[- ]case"), ("snake_case", r"snake[_ ]case"),
                     ("camelCase", r"camel ?case"), ("PascalCase", r"pascal ?case")):
        if re.search(rx, low):
            styles.append(name)
    if len(styles) == 1 and re.search(r"\b(file ?names?|files|modules?|filenames?)\b", low):
        scope = None
        for t in ticks:
            if _is_pathish(t) and "/" in t:
                scope = t
        out.append({"kind": "naming", "style": styles[0], "glob": scope, "source": where, "text": s})
    return out, directive


def parse_rules(repo):
    """Return (mechanical rules, rules Claude must check by reading, files read)."""
    files = find_rule_files(repo)
    mech, read = [], []
    for rel, txt in files:
        agent_file = not rel.lower().endswith("contributing.md")
        converted_lines = set()
        for ln, s, bullet in sentences(txt):
            rules, directive = convert_sentence(rel, ln, s)
            if rules:
                mech.extend(rules)
                converted_lines.add(ln)
            elif ln in converted_lines and re.search(r"\b(them|it|this|these|those)\b", s, re.I) and len(s) < 60:
                continue
            elif (bullet and agent_file) or directive and re.search(r"\b(must|never|always|don't|do not|dont|should|shouldn't|avoid|prefer|only|required|forbidden|not allowed|make sure|ensure)\b|^(keep|use|write|add|put|name|follow|run|avoid)\b", s, re.I):
                read.append({"source": "%s:%d" % (rel, ln), "text": s})
    nt = load_never_twice(repo)
    mech.extend(nt)
    # de-duplicate
    seen, uniq = set(), []
    for r in mech:
        k = (r["kind"], r.get("pattern") or r.get("pm") or r.get("style"), r.get("glob"), tuple(r.get("forbid") or ()))
        if k in seen:
            continue
        seen.add(k)
        uniq.append(r)
    return uniq, read[:60], [f for f, _ in files] + ([NEVER_TWICE] if nt else [])


# ---------------------------------------------------------------------------
# Never Twice rules (.shipsnag/rules.md)
# ---------------------------------------------------------------------------

NT_HEADER = ("# Never Twice rules (ShipSnag Prove It Works)\n\n"
             "Each rule here was added after a mistake was corrected. Prove It Works checks every rule on every proof:\n"
             "`grep` = the regex must not appear in added lines, `forbid-path` = files matching the glob must not change,\n"
             "`require-cmd` = the command must pass. Edit or remove rules freely.\n\n")


def load_never_twice(repo):
    path = os.path.join(repo, NEVER_TWICE)
    txt = read_text(path) if os.path.isfile(path) else None
    if not txt:
        return []
    rules, cur, start = [], None, 0
    for i, raw in enumerate(txt.splitlines(), 1):
        m = re.match(r"^- kind:\s*(\S+)\s*$", raw)
        if m:
            if cur:
                rules.append(cur)
            cur = {"kind": m.group(1).strip(), "source": "%s:%d" % (NEVER_TWICE, i), "never_twice": True}
            continue
        m = re.match(r"^\s+(pattern|glob|why|added):\s?(.*)$", raw)
        if m and cur is not None:
            cur[m.group(1)] = m.group(2).rstrip("\n")
    if cur:
        rules.append(cur)
    good = []
    for r in rules:
        if r["kind"] not in ("grep", "forbid-path", "require-cmd") or not r.get("pattern"):
            continue
        if r["kind"] == "grep":
            try:
                re.compile(r["pattern"])
            except re.error:
                continue
        if r["kind"] == "require-cmd":
            r["safe"] = command_is_safe(r["pattern"])
        r["text"] = r.get("why") or ""
        if not r.get("glob"):
            r["glob"] = None
        good.append(r)
    return good


# ---------------------------------------------------------------------------
# Checking the change against mechanical rules
# ---------------------------------------------------------------------------

def _in_scope(path, glob):
    return glob_match(path, glob) if glob else True


def _code_line(text):
    return text.strip() and not is_comment_line(text)


def check_rules(rules, change, rule_files=(), task=None):
    """Findings (cause 8) for mechanical rules. require-cmd rules are run by prove.py."""
    out = []
    if not change or not change.ok:
        return out
    rule_files = set(rule_files)
    for r in rules:
        k = r["kind"]
        why = r.get("why") or r.get("text") or ""
        label = "Never Twice rule" if r.get("never_twice") else "Project rule"
        src = r["source"]
        if k == "pm":
            forb = set(r.get("forbid") or ())
            for f in change.files:
                b = base_of(f.path).lower()
                if f.status in ("A", "M", "R") and b in JS_LOCKS and JS_LOCKS[b] in forb:
                    out.append(finding(
                        8, "Wrong package manager: %s in the change" % f.path,
                        "%s says to use %s, but the change %s %s, which only %s writes." % (
                            src, r.get("pm") or "another package manager", "adds" if f.status == "A" else "changes",
                            f.path, JS_LOCKS[b]),
                        ["%s: \"%s\"" % (src, _short(r["text"])), "%s (%s)" % (f.path, "new file" if f.status == "A" else "modified")],
                        "Two lockfiles drift apart: CI and teammates install different dependency versions than you tested.",
                        ["Remove %s from the change and redo the install with %s." % (f.path, r.get("pm") or "the project's package manager")],
                        file=f.path, also=[11] if f.status == "A" else []))
            rx = re.compile(r"(?<![\w-])(%s)\s+(install|i|add|ci|run|test|exec|dlx|x|start|build)\b|(?<![\w-])(npx)\s" % "|".join(sorted(forb - {"npx"})) if forb else r"$^")
            for f in change.files:
                if f.path in rule_files or base_of(f.path).lower() in JS_LOCKS or f.binary:
                    continue
                for ln, text in f.added:
                    m = rx.search(text)
                    if not m:
                        continue
                    used = m.group(1) or "npm"
                    if used not in forb:
                        continue
                    out.append(finding(
                        8, "Wrong package manager command in %s" % f.path,
                        "%s says to use %s, but the change adds a `%s` command." % (src, r.get("pm") or "another package manager", used),
                        ["%s:%d: %s" % (f.path, ln, text.strip()[:160]), "%s: \"%s\"" % (src, _short(r["text"]))],
                        "Running it creates the wrong lockfile and installs untested versions.",
                        ["Use `%s` instead." % (r.get("pm") or "the project's package manager")],
                        file=f.path, line=ln))
                    break
        elif k == "forbid-path":
            for f in change.files:
                hit = glob_match(f.path, r["pattern"]) or (f.old_path != f.path and glob_match(f.old_path, r["pattern"]))
                if not hit:
                    continue
                verb = {"A": "adds", "D": "deletes", "R": "renames"}.get(f.status, "edits")
                out.append(finding(
                    8, "%s broken: the change %s %s" % (label, verb, f.path),
                    "%s says not to edit `%s`, and the change %s %s." % (src, r["pattern"], verb, f.path),
                    ["%s: \"%s\"" % (src, _short(why)), "%s (%s, +%d/-%d lines)" % (f.path, verb, len(f.added), len(f.removed))],
                    "Hand edits to protected or generated files are overwritten on the next generation, or break whatever owns them.",
                    ["Revert the edit to %s and make the change at its source (the generator, schema or owning module)." % f.path],
                    file=f.path))
        elif k in ("grep", "forbid-import"):
            if k == "forbid-import":
                rx = re.compile(import_regex(r["pattern"]))
            else:
                try:
                    rx = re.compile(r["pattern"])
                except re.error:
                    continue
            lang = r.get("lang")
            for f in change.files:
                if f.binary or f.path in rule_files or not _in_scope(f.path, r.get("glob")):
                    continue
                e = ext_of(f.path)
                if lang == "ts" and e not in TS_EXT:
                    continue
                if lang == "py" and e not in PY_EXT:
                    continue
                if lang == "js" and e not in JS_EXT:
                    continue
                if not r.get("never_twice") and (e not in CODE_EXT or is_doc(f.path)):
                    continue
                hits = [(ln, t) for ln, t in f.added if (_code_line(t) or r.get("never_twice")) and rx.search(t)]
                if not hits:
                    continue
                what = ("imports `%s`" % r["pattern"]) if k == "forbid-import" else ("uses `%s`" % (r.get("literal") or r["pattern"]))
                out.append(finding(
                    8, "%s broken in %s: %s" % (label, f.path, what),
                    "%s forbids it, and the change %s in %s." % (src, what, f.path),
                    ["%s:%d: %s" % (f.path, ln, t.strip()[:160]) for ln, t in hits[:4]] + ["%s: \"%s\"" % (src, _short(why))],
                    "The project asked for this never to happen; it will be caught in review or break the convention it protects.",
                    ["Remove it and follow the rule: \"%s\"." % _short(why, 140)],
                    file=f.path, line=hits[0][0]))
        elif k == "keep-text":
            out += _check_keep_text(r, change, task, src, label)
        elif k == "naming":
            style = r["style"]
            rxs = {"kebab-case": r"^[a-z0-9]+(?:-[a-z0-9]+)*$", "snake_case": r"^[a-z0-9]+(?:_[a-z0-9]+)*$",
                   "camelCase": r"^[a-z][a-zA-Z0-9]*$", "PascalCase": r"^[A-Z][a-zA-Z0-9]*$"}
            for f in change.files:
                if f.status != "A" or ext_of(f.path) not in CODE_EXT or not _in_scope(f.path, r.get("glob")):
                    continue
                if base_of(f.path).startswith("."):
                    continue
                stem = base_of(f.path).rsplit(".", 1)[0]
                stem = re.sub(r"\.(test|spec|stories|d|module|config)$", "", stem)
                if not stem or stem in ("index", "__init__", "__main__", "main", "conftest") or stem.startswith("_"):
                    continue
                if not re.match(rxs[style], stem):
                    out.append(finding(
                        8, "File naming rule broken: %s" % f.path,
                        "%s asks for %s file names, and the change adds %s." % (src, style, f.path),
                        ["%s: \"%s\"" % (src, _short(r["text"])), "%s (new file)" % f.path],
                        "Inconsistent names break imports on case-sensitive systems and the project's conventions.",
                        ["Rename %s to %s style and update its imports." % (f.path, style)],
                        file=f.path))
    return out


def _literals(text):
    return [next(g for g in m.groups() if g is not None) for m in LITERAL_RE.finditer(text)]


def _texty(lit):
    """A string a person reads: two or more words with letters, not a path, URL, query or format code."""
    t = lit.strip()
    if len(t) < 8 or not re.search(r"[A-Za-z]{2,}\s+\S*[A-Za-z]", t):
        return False
    if re.match(r"^(?:SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|WITH)\b", t, re.I) or "://" in t:
        return False
    if re.search(r"^[\^(\[]|\\[dswb]|[|]{1}.*[|]", t):
        return False
    return True


def _words(t):
    return set(w.lower() for w in re.findall(r"[A-Za-z]{3,}", t))


def _check_keep_text(r, change, task, src, label):
    """Existing user-facing strings the change rewrote or removed, when a project rule says those
    texts are a contract and the task does not ask for new wording."""
    out = []
    task = task or ""
    if TASK_REWORD_RE.search(task):
        return out
    all_added = "\n".join(t for f in change.files for _, t in f.added)
    for f in change.files:
        p = f.path
        if f.status != "M" or f.binary or ext_of(p) not in CODE_EXT or is_doc(p) or is_test_path(p):
            continue
        new_txt = change.new_text(p) or ""
        added_lits = [(ln, lit) for ln, t in f.added if _code_line(t) for lit in _literals(t)]
        hits = []
        for ln, t in f.removed:
            if not _code_line(t):
                continue
            for lit in _literals(t):
                if not _texty(lit) or lit in new_txt or lit in all_added or lit in task:
                    continue
                w = _words(lit)
                best = max(added_lits, key=lambda a: len(w & _words(a[1])), default=None)
                if best is not None and not (w & _words(best[1])):
                    best = None
                hits.append((lit, best))
        if not hits:
            continue
        ev = []
        for lit, best in hits[:3]:
            if best:
                ev.append("%s:%d: \"%s\" became \"%s\"" % (p, best[0], _short(lit, 70), _short(best[1], 70)))
            else:
                ev.append("%s: \"%s\" removed" % (p, _short(lit, 70)))
        out.append(finding(
            8, "%s broken in %s: user-facing text changed" % (label, p),
            "%s says these texts are a contract, the task does not ask for new wording, and the change rewrites %d existing "
            "string%s in %s." % (src, len(hits), "" if len(hits) == 1 else "s", p),
            ev + ["%s: \"%s\"" % (src, _short(r["text"]))],
            "Whatever depends on the exact text (an integration, a parser, people's habits, a test) breaks, and the task never "
            "asked for it.",
            ["Restore the original text. If the new wording is better, propose it to the person as a separate change."],
            file=p, line=hits[0][1][0] if hits[0][1] else None))
    return out


def _short(s, n=110):
    s = re.sub(r"\s+", " ", s or "").strip().rstrip(".")
    return s if len(s) <= n else s[:n - 3] + "..."


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _describe(r):
    k = r["kind"]
    if k == "keep-text":
        return "existing user-facing texts must not change unless the task asks for new wording"
    if k == "pm":
        return "use %s; changes from %s are flagged" % (r.get("pm") or "(any)", ", ".join(r["forbid"]))
    if k == "forbid-path":
        return "files matching `%s` must not change" % r["pattern"]
    if k == "forbid-import":
        return "no imports of `%s`%s" % (r["pattern"], (" in %s" % r["glob"]) if r.get("glob") else "")
    if k == "grep":
        return "added lines must not match `%s`%s" % (r.get("literal") or r["pattern"], (" in %s" % r["glob"]) if r.get("glob") else "")
    if k == "require-cmd":
        return "`%s` must pass%s" % (r["pattern"], "" if r.get("safe", True) else " (not run: it looks like it changes things; check it by hand)")
    if k == "naming":
        return "new file names use %s%s" % (r["style"], (" in %s" % r["glob"]) if r.get("glob") else "")
    return k


def cmd_list(a):
    repo = os.path.abspath(a.repo)
    mech, read, files = parse_rules(repo)
    if a.json:
        sys.stdout.write(json.dumps({"files": files, "checks": mech, "read": read}, indent=2) + "\n")
        return 0
    L = ["%s from %s." % ("%d rules turned into checks, %d to check by reading" % (len(mech), len(read)),
                            ", ".join(files) if files else "no rule files")]
    L.append("")
    if mech:
        L.append("## Checked automatically on every proof (%d)" % len(mech))
        for r in mech:
            L.append("- %s: %s" % (r["source"], _describe(r)))
        L.append("")
    if read:
        L.append("## Rules Claude must check by reading (%d)" % len(read))
        for r in read:
            L.append("- %s: %s" % (r["source"], _short(r["text"], 160)))
        L.append("")
    sys.stdout.write(no_em_dash("\n".join(L)))
    return 0


def cmd_add(a):
    repo = os.path.abspath(a.repo)
    if not os.path.isdir(repo):
        sys.stderr.write("not a directory: %s\n" % a.repo)
        return 2
    pat = a.pattern.strip()
    if "\n" in pat or "\n" in a.why:
        sys.stderr.write("pattern and why must be one line each\n")
        return 2
    if a.kind == "grep":
        try:
            re.compile(pat)
        except re.error as e:
            sys.stderr.write("not a valid regular expression: %s\n" % e)
            return 2
    if a.kind == "require-cmd" and not command_is_safe(pat):
        sys.stderr.write("refusing: `%s` does not look like a read-only check (installs, deletes, git writes, "
                         "network and redirects are not allowed). Use a test, lint, build or typecheck command.\n" % pat)
        return 2
    rule = {"kind": a.kind, "pattern": pat, "glob": a.glob, "why": a.why.strip(), "never_twice": True,
            "source": NEVER_TWICE, "text": a.why.strip(), "safe": True}
    # Dry run first (against the current change), then write.
    dry = []
    change = load_change(repo)
    if a.kind in ("grep", "forbid-path"):
        fs = check_rules([rule], change)
        if fs:
            dry.append("Dry run: it would fail right now (%d finding%s):" % (len(fs), "" if len(fs) == 1 else "s"))
            for f in fs[:6]:
                dry.append("  - " + "; ".join(f["evidence"][:2]))
            dry.append("  The current change already breaks it; fix that before claiming done.")
        else:
            dry.append("Dry run: passes now (%s; %d changed files checked)." % (change.how or change.reason, len(change.files)))
    else:
        argv, sh = split_cmd(pat, repo)
        res = run_cmd(argv, repo, a.timeout, shell=sh)
        st = "passes now" if res["exit"] == 0 and not res["timed_out"] else (
            "timed out after %ds" % a.timeout if res["timed_out"] else "FAILS now (exit %s)" % res["exit"])
        dry.append("Dry run: `%s` %s in %.1fs." % (pat, st, res["seconds"]))
        for l in tail(res["output"], 8):
            dry.append("    " + l)
    d = os.path.join(repo, ".shipsnag")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(repo, NEVER_TWICE)
    new = not os.path.exists(path)
    block = ["- kind: %s" % a.kind, "  pattern: %s" % pat]
    if a.glob:
        block.append("  glob: %s" % a.glob)
    block += ["  why: %s" % a.why.strip(), "  added: %s" % today()]
    with open(path, "a", encoding="utf-8") as fh:
        if new:
            fh.write(NT_HEADER)
        fh.write(no_em_dash("\n".join(block)) + "\n\n")
    L = ["Never Twice rule added to %s:" % NEVER_TWICE, ""] + ["    " + b for b in block] + [""] + dry + [
        "", "It now runs on every `prove.py` proof of this repo (%s)." % _describe(rule)]
    sys.stdout.write(no_em_dash("\n".join(L)) + "\n")
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    if argv and argv[0] == "add":
        ap = argparse.ArgumentParser(prog="rules.py add", description="Never Twice: add a checkable rule to .shipsnag/rules.md")
        ap.add_argument("--repo", required=True)
        ap.add_argument("--kind", required=True, choices=["grep", "forbid-path", "require-cmd"])
        ap.add_argument("--pattern", required=True, help="regex (grep), glob (forbid-path) or command (require-cmd)")
        ap.add_argument("--why", required=True, help="the mistake this rule prevents, in one line")
        ap.add_argument("--glob", default=None, help="grep only: limit to files matching this glob")
        ap.add_argument("--timeout", type=int, default=300)
        return cmd_add(ap.parse_args(argv[1:]))
    ap = argparse.ArgumentParser(description="List the project's written rules and how each is checked.")
    ap.add_argument("repo")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    return cmd_list(a)


if __name__ == "__main__":
    sys.exit(main())
