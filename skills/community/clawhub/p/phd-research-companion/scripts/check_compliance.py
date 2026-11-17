#!/usr/bin/env python3
"""
Pre-Submission Compliance Check

Every checklist item is either IMPLEMENTED or reported as UNVERIFIED.
There are no dead entries that silently default to "failed", and none that
default to "passed". A check that cannot be evaluated says so explicitly.

Usage:
    python check_compliance.py --project-dir ./my-project
    python check_compliance.py --project-dir ./my-project --strict   # exit 1 on any fail
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

MIN_PAPERS = 50
MIN_ROUNDS = 5


class ComplianceChecker:
    def __init__(self, project_dir: Path, track: str | None = None):
        self.project_dir = Path(project_dir).expanduser().resolve()
        self.checks: dict[str, dict] = {}
        self.track = track or self._detect_track()

    def _detect_track(self) -> str | None:
        """Read the track recorded by `init`, so theory papers are not graded
        on experiments they will never run."""
        meta = self.project_dir / "project.json"
        if not meta.is_file():
            return None
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
        except Exception:
            return None
        t = data.get("track")
        return t if t in ("theory", "empirical") else None

    def _record(self, key: str, name: str, passed: bool, message: str,
                status: str = "evaluated") -> bool:
        self.checks[key] = {"name": name, "passed": bool(passed),
                            "status": status, "message": message}
        return bool(passed)

    # ---------------------------------------------------------- checks

    def check_literature(self) -> None:
        lit = self.project_dir / "01-literature-survey"
        if not lit.is_dir():
            self._record("literature", "Literature survey", False,
                         "01-literature-survey/ not found", "unverified")
            return
        n = 0
        for f in list(lit.glob("*.bib")) + list(lit.glob("*.bibtex")):
            n += len(re.findall(r"^\s*@\w+\s*\{", f.read_text(encoding="utf-8", errors="replace"),
                                re.M))
        self._record("literature", f"Literature survey (>= {MIN_PAPERS} entries)",
                     n >= MIN_PAPERS, f"{n} BibTeX entries parsed from "
                     f"{len(list(lit.glob('*.bib')) + list(lit.glob('*.bibtex')))} file(s)")

    def _experiment_check(self, key: str, name: str, glob: str) -> None:
        if self.track == "theory":
            # A theory paper has no baselines/ablations/robustness suite.
            # Demanding one is a category error, not a strictness setting.
            self._record(key, name, True,
                         "not applicable: project track is 'theory'", "n/a")
            return
        exp = self.project_dir / "04-experiments"
        hits = sorted(exp.glob(glob)) if exp.is_dir() else []
        self._record(key, name, bool(hits),
                     f"{len(hits)} {glob.strip('*')} config(s)" if hits
                     else f"no {glob} config in 04-experiments/")

    def check_baselines(self) -> None:
        self._experiment_check("baselines", "Baseline comparison design", "*comparison*")

    def check_ablations(self) -> None:
        self._experiment_check("ablations", "Ablation study design", "*ablation*")

    def check_robustness(self) -> None:
        self._experiment_check("robustness", "Robustness stress-test design", "*robustness*")

    def check_theory_artifacts(self) -> None:
        """Theory counterpart of the experiment checks: claims + certificates."""
        if self.track != "theory":
            self._record("theory_artifacts", "Theory artifacts", True,
                         "not applicable: project track is 'empirical'", "n/a")
            return
        ledger = self.project_dir / "02-methodology-dev" / "claims.json"
        audit_dir = self.project_dir / "07-audit-trail"
        certs = sorted(audit_dir.glob("*")) if audit_dir.is_dir() else []
        claims = 0
        if ledger.is_file():
            try:
                data = json.loads(ledger.read_text(encoding="utf-8"))
                claims = len(data.get("claims", data if isinstance(data, list) else []))
            except Exception:
                claims = -1
        ok = claims > 0 and len(certs) > 0
        self._record("theory_artifacts", "Theory artifacts (ledger + certificate)", ok,
                     f"{claims} claim(s) in claims.json, "
                     f"{len(certs)} certificate file(s) in 07-audit-trail/")

    def check_latex(self) -> None:
        draft = self.project_dir / "03-paper-drafting"
        if not draft.is_dir():
            self._record("latex", "LaTeX structure", False,
                         "03-paper-drafting/ not found", "unverified")
            return
        tex = sorted(draft.glob("*.tex"))
        if not tex:
            self._record("latex", "LaTeX structure", False,
                         "no .tex file in 03-paper-drafting/", "unverified")
            return
        src = tex[0].read_text(encoding="utf-8", errors="replace")
        # NOTE: regex chars must be escaped (r"\d" would mean "a digit").
        need = {"documentclass": r"\\documentclass",
                "begin_document": r"\\begin\s*\{document\}",
                "bibliography": r"\\bibliography|bibliography\s*\{",
                "abstract": r"\\begin\s*\{abstract\}"}
        missing = [k for k, p in need.items() if not re.search(p, src)]
        self._record("latex", "LaTeX structure", not missing,
                     f"{tex[0].name}: missing {missing}" if missing
                     else f"{tex[0].name}: all required macros present")

    def check_revisions(self) -> None:
        h = self.project_dir / "05-revision-rounds" / "revision-history.json"
        if not h.exists():
            self._record("revisions", f"Revision rounds (>= {MIN_ROUNDS})", False,
                         "revision-history.json not found")
            return
        try:
            data = json.loads(h.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            self._record("revisions", f"Revision rounds (>= {MIN_ROUNDS})", False,
                         f"revision-history.json unreadable: {e}")
            return
        done = int(data.get("rounds_completed", 0))
        self._record("revisions", f"Revision rounds (>= {MIN_ROUNDS})", done >= MIN_ROUNDS,
                     f"{done} round(s) recorded")

    def check_math(self) -> None:
        reports = sorted((self.project_dir / "03-paper-drafting").glob("math-notation-check*.md"))
        if not reports:
            self._record("math", "Math notation check", False,
                         "no math-notation-check report found; run verify_math_notation.py",
                         "unverified")
            return
        src = reports[-1].read_text(encoding="utf-8", errors="replace")
        m = re.search(r"Notation Discrepancies Identified:\s*(\d+)", src)
        if not m:
            self._record("math", "Math notation check", False,
                         f"cannot parse discrepancy count from {reports[-1].name}", "unverified")
            return
        n = int(m.group(1))
        self._record("math", "Math notation check", n == 0,
                     f"{n} undefined symbol(s) per {reports[-1].name}")

    @staticmethod
    def dpi_of(path: Path) -> int | None:
        """Read embedded DPI from PNG (pHYs) or JPEG (JFIF APP0) headers.

        Pure stdlib: no Pillow needed. Returns None when the file carries no
        density information, which is reported as UNVERIFIED rather than as a
        pass or a fail.
        """
        try:
            head = path.read_bytes()[:64]
        except OSError:
            return None
        if path.suffix.lower() == ".png" and head[:8] == b"\x89PNG\r\n\x1a\n":
            data = path.read_bytes()
            i = 8
            while i + 8 <= len(data):
                length = int.from_bytes(data[i:i + 4], "big")
                ctype = data[i + 4:i + 8]
                # payload: ppux(4) ppuy(4) unit(1); chunk header is 8 bytes
                if ctype == b"pHYs" and i + 17 <= len(data):
                    ppux = int.from_bytes(data[i + 8:i + 12], "big")
                    unit = data[i + 16]
                    if unit == 1 and ppux:            # pixels per metre
                        return round(ppux * 0.0254)
                    return None
                i += 12 + length
                if ctype == b"IEND":
                    break
            return None
        if path.suffix.lower() in (".jpg", ".jpeg") and head[:2] == b"\xff\xd8":
            i = 2
            data = path.read_bytes()
            while i + 4 <= len(data):
                if data[i] != 0xFF:
                    i += 1
                    continue
                marker = data[i + 1]
                if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                    i += 2
                    continue
                seglen = int.from_bytes(data[i + 2:i + 4], "big")
                if marker == 0xE0 and data[i + 4:i + 9] == b"JFIF\x00":
                    units = data[i + 9]
                    xden = int.from_bytes(data[i + 10:i + 12], "big")
                    if xden:
                        return xden if units == 1 else round(xden * 2.54)
                    return None
                i += 2 + seglen
                if marker == 0xDA:
                    break
            return None
        return None

    def check_figures(self) -> None:
        fig_dirs = [self.project_dir / "03-paper-drafting" / "figures",
                    self.project_dir / "03-paper-drafting"]
        files = []
        for d in fig_dirs:
            if d.is_dir():
                files += [f for f in d.iterdir()
                          if f.suffix.lower() in {".pdf", ".eps", ".svg", ".png", ".jpg"}]
        files = sorted(set(files))
        if not files:
            self._record("figures", "Figure assets", False,
                         "no figure files found", "unverified")
            return
        raster = [f for f in files if f.suffix.lower() in {".png", ".jpg", ".jpeg"}]
        vector = [f for f in files if f.suffix.lower() in {".pdf", ".eps", ".svg"}]
        if not raster:
            self._record("figures", "Figure assets", True,
                         f"{len(vector)} vector figure(s); DPI criterion N/A for vector")
            return

        measured, unknown = {}, []
        for f in raster:
            d = self.dpi_of(f)
            (measured.__setitem__(f.name, d) if d else unknown.append(f.name))
        low = sorted(n for n, d in measured.items() if d < 300)

        if low:
            self._record("figures", "Figure assets (>= 300 DPI)", False,
                         f"below 300 DPI: {', '.join(low)} "
                         f"(measured from file headers: "
                         f"{', '.join(f'{n}={d}' for n, d in sorted(measured.items()))})"
                         + (f"; no density header: {', '.join(unknown)}" if unknown else ""))
        elif unknown:
            self._record("figures", "Figure assets (>= 300 DPI)", False,
                         f"{len(measured)} figure(s) >= 300 DPI OK, but "
                         f"{len(unknown)} carry no density header: {', '.join(unknown)}",
                         "unverified")
        else:
            self._record("figures", "Figure assets (>= 300 DPI)", True,
                         f"{len(measured)} raster figure(s) all >= 300 DPI: "
                         f"{', '.join(f'{n}={d}' for n, d in sorted(measured.items()))}")

    def run_all(self) -> None:
        for fn in (self.check_literature, self.check_baselines, self.check_ablations,
                   self.check_robustness, self.check_theory_artifacts,
                   self.check_latex, self.check_revisions,
                   self.check_math, self.check_figures):
            try:
                fn()
            except Exception as e:  # noqa: BLE001
                self._record(fn.__name__, fn.__name__, False,
                             f"checker raised {type(e).__name__}: {e}", "error")


def render_report(checks: dict, project_dir: Path) -> Path:
    live = [c for c in checks.values() if c["status"] != "n/a"]
    passed = sum(1 for c in live if c["passed"])
    total = len(live)
    unver = sum(1 for c in live if c["status"] != "evaluated")
    na = len(checks) - len(live)
    verdict = "READY" if passed == total and unver == 0 else "NOT READY"

    lines = ["# Pre-Submission Compliance Audit", "",
             f"Project: {project_dir.name}",
             f"Audit date: {datetime.now().isoformat(timespec='seconds')}",
             f"Result: {verdict}  ({passed}/{total} passed, {unver} unverified"
             + (f", {na} not applicable)" if na else ")"), "",
             "| Check | Result | Status | Detail |", "|---|:-:|---|---|"]
    for c in checks.values():
        if c["status"] == "n/a":
            mark = "N/A"
        elif c["passed"] and c["status"] == "evaluated":
            mark = "PASS"
        elif c["status"] == "evaluated":
            mark = "FAIL"
        else:
            mark = f"UNVERIFIED ({c['status']})"
        lines.append(f"| {c['name']} | {mark} | {c['status']} | {c['message']} |")
    lines += ["", "---",
              "Unverified rows are NOT passes. Resolve them before relying on this report.",
              "Generated by phd-research-companion 2.4.0"]
    out = project_dir / f"compliance-audit-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Pre-submission compliance audit")
    ap.add_argument("--project-dir", "-p", required=True)
    ap.add_argument("--strict", action="store_true", help="exit 1 if any check fails")
    ap.add_argument("--json", dest="json_out", default=None, help="also write JSON here")
    args = ap.parse_args()

    project_dir = Path(args.project_dir).expanduser().resolve()
    if not project_dir.is_dir():
        print(f"error: project dir not found: {project_dir}", file=sys.stderr)
        return 2

    checker = ComplianceChecker(project_dir)
    checker.run_all()

    print(f"\nCompliance audit: {project_dir}"
          + (f"  [track: {checker.track}]" if checker.track else ""))
    for c in checker.checks.values():
        tag = "N/A" if c["status"] == "n/a" else (
            "PASS" if c["passed"] and c["status"] == "evaluated" else (
                "FAIL" if c["status"] == "evaluated" else "UNVERIFIED"))
        print(f"  [{tag:<10}] {c['name']}: {c['message']}")

    report = render_report(checker.checks, project_dir)
    print(f"\nReport: {report}")

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(checker.checks, indent=2), encoding="utf-8")

    n_fail = sum(1 for c in checker.checks.values()
                 if not c["passed"] and c["status"] != "n/a")
    return 1 if (args.strict and n_fail) else 0


if __name__ == "__main__":
    sys.exit(main())
