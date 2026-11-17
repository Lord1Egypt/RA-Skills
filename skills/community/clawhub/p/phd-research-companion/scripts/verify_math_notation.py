#!/usr/bin/env python3
"""
Mathematical Notation Verifier

Scans LaTeX sources, extracts every math command actually used, and compares
it against the symbols the file DEFINES (notation table rows, \\newcommand,
\\DeclareMathOperator) plus a whitelist of standard LaTeX/AMS commands.

Anything left over is reported as potentially undefined. This is a linter, not
a proof: it narrows the search space, it does not certify correctness.

Usage:
    python verify_math_notation.py -i main.tex -o math-notation-check.md
    python verify_math_notation.py -i main.tex sec-theory.tex --strict
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

# Standard LaTeX / AMS / common packages: not the author's responsibility.
STANDARD = {
    # greek
    "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta", "eta",
    "theta", "vartheta", "iota", "kappa", "lambda", "mu", "nu", "xi", "pi",
    "rho", "varrho", "sigma", "varsigma", "tau", "upsilon", "phi", "varphi",
    "chi", "psi", "omega", "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi",
    "Sigma", "Upsilon", "Phi", "Psi", "Omega",
    # operators
    "frac", "dfrac", "tfrac", "sqrt", "sum", "prod", "int", "iint", "oint",
    "lim", "liminf", "limsup", "log", "ln", "exp", "sin", "cos", "tan",
    "max", "min", "arg", "sup", "inf", "deg", "det", "dim", "ker", "hom",
    "Pr", "mathbb", "mathcal", "mathbf", "mathrm", "mathit", "mathsf",
    "mathtt", "boldsymbol", "bm", "operatorname", "DeclareMathOperator",
    "text", "mbox", "textbf", "textit", "texttt", "textsc", "emph",
    # relations
    "leq", "le", "geq", "ge", "neq", "ne", "approx", "equiv", "sim", "simeq",
    "propto", "ll", "gg", "subset", "subseteq", "supset", "supseteq", "in",
    "notin", "cup", "cap", "setminus", "times", "cdot", "circ", "ast", "star",
    "mid", "parallel", "perp", "prec", "succ", "preceq", "succeq",
    # logic / sets
    "forall", "exists", "nexists", "neg", "lnot", "land", "lor", "implies",
    "iff", "leftarrow", "rightarrow", "Leftarrow", "Rightarrow", "leftrightarrow",
    "mapsto", "to", "gets", "uparrow", "downarrow", "Uparrow", "Downarrow",
    "emptyset", "varnothing", "infty", "partial", "nabla", "top", "bot",
    # delimiters & sizing
    "left", "right", "big", "Big", "bigg", "Bigg", "bigl", "bigr", "biggl",
    "biggr", "langle", "rangle", "lceil", "rceil", "lfloor", "rfloor",
    "vert", "Vert", "lvert", "rvert", "lVert", "rVert",
    # accents & style
    "hat", "widehat", "tilde", "widetilde", "bar", "vec", "dot", "ddot",
    "overline", "underline", "overbrace", "underbrace", "stackrel", "overset",
    "underset", "binom", "choose", "bmod", "pmod", "substack",
    # spacing & layout
    "quad", "qquad", "hspace", "vspace", "ldots", "cdots", "vdots", "ddots",
    "dots", "nonumber", "notag", "label", "ref", "eqref", "cite", "citep",
    "citet", "caption", "centering", "array", "nonumber",
    # ams theorem-ish / misc
    "begin", "end", "displaystyle", "textstyle", "scriptstyle", "limits",
    "nolimits", "mathopen", "mathclose", "mathbin", "mathrel", "mathop",
    "newline", "linebreak", "allowbreak", "phantom", "hfill", "vspace",
    "boxed", "footnotesize", "small", "large", "normalsize",
}

ENV_RE = re.compile(
    r"\\begin\{(equation|equation\*|align|align\*|gather|gather\*|multline|"
    r"eqnarray|flalign|alignat)\}.*?\\end\{\1\}", re.S)

DISPLAY_RE = re.compile(r"\\\[.*?\\\]", re.S)
INLINE_RE = re.compile(r"\$[^$]+\$", re.S)
PAREN_RE = re.compile(r"\\\((?:[^\\]|\\.)*?\\\)", re.S)
CMD_RE = re.compile(r"\\([A-Za-z]+)")


def strip_comments(src: str) -> str:
    out = []
    for line in src.splitlines():
        line = re.sub(r"(?<!\\)%.*$", "", line)
        out.append(line)
    return "\n".join(out)


def collect_math(src: str) -> list[tuple[str, int]]:
    """Return (math_snippet, line_number) for every math region found."""
    found: list[tuple[str, int]] = []
    for m in ENV_RE.finditer(src):
        found.append((m.group(0), src[:m.start()].count("\n") + 1))
    for rx in (DISPLAY_RE, INLINE_RE, PAREN_RE):
        for m in rx.finditer(src):
            found.append((m.group(0), src[:m.start()].count("\n") + 1))
    return found


def defined_symbols(src: str) -> set[str]:
    """Symbols the author explicitly introduces."""
    out: set[str] = set()
    out |= set(re.findall(r"\\newcommand\{\\([A-Za-z]+)\}", src))
    out |= set(re.findall(r"\\DeclareMathOperator\{\\([A-Za-z]+)\}", src))
    out |= set(re.findall(r"\\def\\([A-Za-z]+)", src))
    # notation table rows:  $sym$ & description \\
    for row in re.findall(r"\$([^$]{1,40})\$\s*&", src):
        out |= set(CMD_RE.findall(row))
    # "let $x$ denote/be ..." style inline definitions
    for m in re.finditer(r"let\s+\$?\\?([A-Za-z]{1,20})\$?\s+(?:denote|be)\b", src):
        out.add(m.group(1))
    return out


def theorem_envs(src: str) -> list[dict]:
    out = []
    for rx in (r"\\begin\{(theorem|lemma|proposition|corollary|definition|assumption)\}",
               r"\\begin\{(theorem|lemma|proposition|corollary|definition|assumption)\*}"):
        for m in re.finditer(rx, src):
            out.append({"kind": m.group(1),
                        "line": src[:m.start()].count("\n") + 1})
    out.sort(key=lambda d: d["line"])
    return out


def env_labels(src: str, envs: list[dict]) -> list[dict]:
    """Flag numbered statements whose \\label is never \\ref'd."""
    labels = set(re.findall(r"\\label\{([^}]+)\}", src))
    refs = set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}", src))
    return [{"label": lab, "referenced": lab in refs} for lab in sorted(labels)]


def analyse(path: Path) -> dict:
    src = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
    regions = collect_math(src)
    used: dict[str, list[int]] = {}
    for snippet, line in regions:
        for cmd in CMD_RE.findall(snippet):
            used.setdefault(cmd, []).append(line)

    defined = defined_symbols(src)
    unknown = {c: sorted(set(lines)) for c, lines in used.items()
               if c not in STANDARD and c not in defined}

    envs = theorem_envs(src)
    labels = env_labels(src, envs)
    proofs = len(re.findall(r"\\begin\{proof\}", src))
    unref = [l["label"] for l in labels if not l["referenced"]]

    return {"file": str(path), "math_regions": len(regions),
            "distinct_commands": len(used), "defined": sorted(defined),
            "unknown": unknown,
            "theorem_envs": envs,
            "env_counts": {k: sum(1 for e in envs if e["kind"] == k)
                           for k in {e["kind"] for e in envs}},
            "proofs": proofs,
            "unreferenced_labels": unref}


def render(reports: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_unknown = sum(len(r["unknown"]) for r in reports)
    total_envs = sum(len(r["theorem_envs"]) for r in reports)
    total_proofs = sum(r["proofs"] for r in reports)
    total_unref = sum(len(r["unreferenced_labels"]) for r in reports)

    lines = ["# Mathematical Notation Verification Report", "",
             f"Scan date: {now}",
             f"Files scanned: {len(reports)}", "",
             "## Summary", "",
             f"- Formal statement environments found: {total_envs}",
             f"- Proof environments found: {total_proofs}",
             f"- Notation Discrepancies Identified: {total_unknown}",
             f"- Labels never referenced: {total_unref}", ""]

    if total_envs and total_proofs < total_envs:
        lines += [f"> Warning: {total_envs - total_proofs} formal statement(s) have no "
                  "matching `proof` environment.", ""]

    for r in reports:
        lines += [f"## {r['file']}", "",
                  f"- Math regions: {r['math_regions']}",
                  f"- Distinct commands used: {r['distinct_commands']}",
                  f"- Explicitly defined symbols: {len(r['defined'])}"]
        if r["env_counts"]:
            lines.append("- Environments: " + ", ".join(
                f"{k}={v}" for k, v in sorted(r["env_counts"].items())))
        lines.append("")
        if r["unknown"]:
            lines += ["### Commands used but not defined in this file", "",
                      "| Command | Lines |", "|---|---|"]
            for cmd, ls in sorted(r["unknown"].items()):
                lines.append(f"| `\\{cmd}` | {', '.join(map(str, ls[:8]))} |")
            lines += ["", "These may be defined in a file not passed to this scan, "
                           "or genuinely undefined. Verify each by hand."]
        else:
            lines.append("Every math command used is either standard LaTeX or "
                         "explicitly defined in this file.")
        if r["unreferenced_labels"]:
            lines += ["", "### Labels defined but never referenced", ""]
            lines += [f"- `{l}`" for l in r["unreferenced_labels"]]
        lines.append("")

    lines += ["---", "Auto-generated by phd-research-companion 2.4.0",
              "This is a lint pass, not a correctness proof."]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify LaTeX math notation consistency")
    ap.add_argument("--input", "-i", nargs="+", required=True, help="LaTeX files (pass all of them)")
    ap.add_argument("--output", "-o", default="math-notation-check.md")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any undefined command or unreferenced label is found")
    args = ap.parse_args()

    paths = [Path(p).expanduser() for p in args.input]
    missing = [p for p in paths if not p.is_file()]
    if missing:
        for p in missing:
            print(f"error: input file not found: {p}", file=sys.stderr)
        return 2

    reports = [analyse(p) for p in paths]
    out = Path(args.output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(reports), encoding="utf-8")

    n_unknown = sum(len(r["unknown"]) for r in reports)
    n_unref = sum(len(r["unreferenced_labels"]) for r in reports)
    print(f"Scanned {len(paths)} file(s): "
          f"{n_unknown} potentially undefined command(s), "
          f"{n_unref} unreferenced label(s).")
    print(f"Report: {out}")

    return 1 if (args.strict and (n_unknown or n_unref)) else 0


if __name__ == "__main__":
    sys.exit(main())
