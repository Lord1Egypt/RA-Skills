#!/usr/bin/env python3
"""What this machine can and cannot do, and how to fix what it cannot.

Run it once for a new user, before the first mode. Every check answers a
CAPABILITY question rather than a binary-name question, because the binary-name
version has already been wrong here: an earlier check looked for `xelatex`, did
not find it, and concluded PDF rendering was at risk — while `tectonic` was
installed and every PDF rendered fine. So the PDF check renders a PDF.

This diagnostic's --install option handles requirements.txt Python packages.
The agent performs other needed setup using references/agent-setup.md, including
system tools and daily-browser CDP. The user grants browser connection consent.
A diagnostic run alone never installs system tools.

Exit codes: 0 everything the skill needs is present, 1 something is missing
(the report says what it costs), 2 the check itself could not run.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import tempfile

from opencli_compat import installed_package, prepared_opencli
from host_execution import HOST_EXECUTION_REQUIRED, tectonic_needs_host_execution

REPO = pathlib.Path(__file__).resolve().parent.parent
REQUIREMENTS = REPO / "requirements.txt"
RENDER_CV = REPO / "scripts" / "render_cv.py"

# The engines render_cv.find_latex_engine accepts, and where it looks besides
# PATH. Copied rather than imported: render_cv imports PyYAML and python-docx,
# and this diagnostic has to run before requirements.txt is installed.
# test_doctor.py holds the two in step. CV and letter PDFs never use pandoc —
# an earlier version of this check required it, and a machine with only
# tectonic was told on every mode entry that it could not render a CV PDF.
CV_ENGINES = ("tectonic", "xelatex", "lualatex", "pdflatex")
CJK_CV_ENGINES = ("xelatex", "tectonic")
ENGINE_DIRS = ["/opt/homebrew/bin", "/usr/local/bin", "/Library/TeX/texbin",
               "~/.cargo/bin", "/usr/bin", "/bin"]

# A tiny, fictional profile. JSON is valid YAML, so writing it needs no PyYAML.
_PROBE_PROFILE = {
    "meta": {"name": "Probe Candidate", "language": "en", "target_market": "uk"},
    "contact": {"email": "probe@example.invalid"},
    "experience": [{"title": "Engineer", "org": "Example Ltd", "start": "2020",
                    "end": "2022", "bullets": ["Built a small renderer probe."]}],
}

# Which import each requirement actually provides. A requirement's install name
# and its module name differ often enough (python-docx -> docx, PyYAML -> yaml)
# that guessing from the install name reports a working machine as broken.
IMPORT_NAME = {"pyyaml": "yaml", "python-docx": "docx", "pymupdf": "pymupdf"}


def requirements() -> list[tuple[str, str]]:
    """[(install name, import name)] parsed from requirements.txt."""
    out = []
    if not REQUIREMENTS.is_file():
        return out
    for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        pkg = re.split(r"[<>=!~\[]", line, maxsplit=1)[0].strip()
        out.append((pkg, IMPORT_NAME.get(pkg.lower(), pkg.replace("-", "_"))))
    return out


def importable(module: str) -> bool:
    try:
        return importlib.util.find_spec(module) is not None
    except (ImportError, ValueError):
        return False


def _process_output(result) -> str:
    """Decode a subprocess result without assuming a particular capture mode."""
    def text(value):
        if isinstance(value, bytes):
            return value.decode("utf-8", "replace")
        return str(value or "")
    return text(getattr(result, "stdout", "")) + text(getattr(result, "stderr", ""))


def find_cv_engine(cjk: bool = False) -> str | None:
    """The engine render_cv would pick, found the same way: PATH, then ENGINE_DIRS."""
    for engine in (CJK_CV_ENGINES if cjk else CV_ENGINES):
        found = shutil.which(engine)
        if found:
            return found
        for directory in ENGINE_DIRS:
            candidate = pathlib.Path(directory).expanduser() / engine
            if candidate.is_file():
                return str(candidate)
    return None


def office_binary() -> str | None:
    """LibreOffice exactly as check_pages.py finds it to measure a .docx."""
    return shutil.which("soffice") or shutil.which("libreoffice")


def can_render_pdf() -> tuple[bool, str]:
    """Check the CV/letter PDF path by rendering a CV through render_cv itself.

    render_cv compiles its own LaTeX with tectonic/xelatex/lualatex/pdflatex;
    pandoc is not involved, so it is not asked for here.
    """
    engine = find_cv_engine()
    if engine is None:
        return False, ("no LaTeX engine render_cv can use "
                       "(tectonic, xelatex, lualatex or pdflatex)")
    name = pathlib.Path(engine).stem
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp)
        profile = d / "probe.yaml"
        profile.write_text(json.dumps(_PROBE_PROFILE), encoding="utf-8")
        pdf = d / "probe.pdf"
        try:
            result = subprocess.run([sys.executable, str(RENDER_CV), str(profile),
                                     "--format", "pdf", "--out", str(pdf)],
                                    capture_output=True, timeout=300, check=False)
        except (OSError, subprocess.SubprocessError) as exc:
            return False, f"render_cv + {name} failed to run: {exc}"
        output = _process_output(result)
        if result.returncode == 0 and pdf.is_file() and pdf.stat().st_size > 0:
            if find_cv_engine(cjk=True) is None:
                return True, (f"render_cv + {name}; Latin script only — CJK CVs need "
                              "xelatex or tectonic")
            return True, f"render_cv + {name}"
        if (tectonic_needs_host_execution(engine, output)
                or f"NOTICE_{HOST_EXECUTION_REQUIRED}" in output):
            return False, (f"{HOST_EXECUTION_REQUIRED}: Tectonic is installed, but this "
                           "restricted macOS process cannot initialize SystemConfiguration; "
                           "rerun PDF rendering and verification through the host's approved "
                           "trusted or elevated execution route")
    reason = next((line.strip() for line in output.splitlines() if line.strip()), "")
    return False, f"render_cv + {name} produced no PDF" + (f": {reason[:200]}" if reason else "")


def can_render_report() -> tuple[bool, str]:
    """The common report path uses PyMuPDF and bundled fonts, without TeX."""
    if not importable("pymupdf") or not importable("yaml"):
        return False, "report Python dependencies are missing"
    try:
        from deliver import render_pdf
        with tempfile.TemporaryDirectory() as tmp:
            md = pathlib.Path(tmp) / "report.md"
            md.write_text("# Career report\n\n求职建议。Résumé. 日本語。한국어.\n", encoding="utf-8")
            ok, detail = render_pdf(md, md.with_suffix(".pdf"), None)
            return ok, "PyMuPDF + bundled fonts" if ok else detail
    except (ImportError, OSError, ValueError, RuntimeError) as exc:
        return False, str(exc)


def fast_capabilities() -> list[str]:
    """What is missing, decided WITHOUT rendering anything. Milliseconds.

    `enter_mode.py` runs on every mode entry and cannot afford `checks()`, which
    renders a PDF. So this trades one direction of accuracy away, deliberately,
    and the asymmetry is the point:

      it is SOUND about missing   -- no engine render_cv can find means no CV PDF
      it is UNSOUND about present -- an engine can be installed and still fail
                                     to produce a file

    A warning may only fire when it is sure, or it becomes the line everyone
    filters out. Confirming that a capability WORKS stays with `doctor.py`, which
    renders one. This function never claims anything works; it only names what
    demonstrably cannot.
    """
    missing = []
    for pkg, module in requirements():
        if not importable(module):
            missing.append(f"python package {pkg}")
    if find_cv_engine() is None:
        missing.append("CV/letter PDF rendering (tectonic or another LaTeX engine; "
                       "optional for reports)")
    elif find_cv_engine(cjk=True) is None:
        missing.append("CJK CV/letter PDF rendering (xelatex or tectonic; "
                       "lualatex/pdflatex cannot typeset CJK)")
    if not shutil.which("pdftotext"):
        missing.append("pdftotext")
    if not office_binary():
        missing.append("LibreOffice (soffice) to measure Word page counts")
    if not opencli_tools()[0]:
        missing.append("opencli")
    return missing


def install_hint(binary: str) -> str:
    if binary == "opencli":
        return "Agent: prepare a dedicated opencli prefix via references/agent-setup.md"
    if platform.system() == "Windows":
        return (f"Agent: install {binary} with a verified Windows package or portable "
                "release; follow references/agent-setup.md")
    mac = platform.system() == "Darwin"
    brew = {"pandoc": "brew install pandoc", "tectonic": "brew install tectonic",
            "pdftotext": "brew install poppler",
            "soffice": "brew install --cask libreoffice"}
    apt = {"pandoc": "sudo apt install pandoc", "tectonic": "sudo apt install tectonic",
           "pdftotext": "sudo apt install poppler-utils",
           "soffice": "sudo apt install libreoffice-writer"}
    return (brew if mac else apt).get(binary, f"install {binary}")


def opencli_tools() -> tuple[str | None, str | None, str]:
    """`(opencli, node, problem)`: the OpenCLI run_tool.py runs, and its Node.

    The prepared runtime comes first, because every recorded read goes through
    it; PATH is used only when no runtime with OpenCLI was prepared. A runtime
    that records a missing package is reported, never replaced by whatever
    `opencli` PATH happens to hold.
    """
    try:
        prepared = prepared_opencli()
    except ValueError as exc:
        return None, None, str(exc)
    if prepared:
        node, package = prepared
        return str(package), node or shutil.which("node"), ""
    return shutil.which("opencli"), shutil.which("node"), ""


def can_use_opencli_cdp() -> tuple[bool, str]:
    """Inspect website routing without connecting to any browser or extension.

    A CDP class existing in the package is insufficient: 1.8.7 exports one but
    selects BrowserBridge for website adapters. Probe the installed factory,
    never instantiate its result. Live endpoint/profile verification is separate.
    """
    opencli, node, problem = opencli_tools()
    if problem:
        return False, problem
    if not opencli:
        return False, "opencli is not installed"
    if not node:
        return False, "Node.js is unavailable; OpenCLI CDP routing is unverified"
    try:
        package = installed_package()
        runtime = package / "dist/src/runtime.js"
        browser = package / "dist/src/browser/index.js"
        if not runtime.is_file() or not browser.is_file():
            return False, "installed OpenCLI layout is unknown; inspect its documented CDP route"
        # The endpoint is a child-process probe value, not a connection target.
        # No connect(), browserSession(), CLI doctor or daemon command is called.
        probe = """
process.env.OPENCLI_CDP_ENDPOINT ||= 'http://127.0.0.1:0';
const {getBrowserFactory} = await import(process.argv[1]);
const {CDPBridge} = await import(process.argv[2]);
const sites = ['51job', 'indeed', 'boss', 'linkedin'];
console.log(JSON.stringify(sites.map(site => ({site,
  cdp: typeof CDPBridge === 'function' && getBrowserFactory(site) === CDPBridge}))));
"""
        result = subprocess.run([node, "--input-type=module", "-e", probe,
                                 runtime.as_uri(), browser.as_uri()], capture_output=True,
                                text=True, encoding="utf-8", timeout=15, check=False)
        routes = json.loads(result.stdout or "null") if result.returncode == 0 else None
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        return False, f"OpenCLI CDP routing check could not complete: {exc}"
    sites = {"51job", "indeed", "boss", "linkedin"}
    if (isinstance(routes, list) and len(routes) == len(sites)
            and all(isinstance(route, dict) and isinstance(route.get("site"), str)
                    for route in routes)
            and {route.get("site") for route in routes} == sites
            and all(route.get("cdp") is True for route in routes)):
        return True, "website factories select CDP; verify the selected live endpoint and adapter before reading"
    return False, ("website CDP routing is not confirmed; use the diagnosed browser CDP fallback, "
                   "never an extension-backed connection")


def checks() -> list[dict]:
    """Every capability, what it costs when absent, and how to get it."""
    out = []
    for pkg, module in requirements():
        out.append({
            "what": f"python package {pkg}",
            "ok": importable(module),
            "cost": ("nothing in this skill runs without it"
                     if module == "yaml" else
                     ".docx output is unavailable" if module == "docx" else
                     "PDF glyph verification and delivery are unavailable" if module == "pymupdf" else
                     f"features using {module} are unavailable"),
            "fix": f"{sys.executable} -m pip install {pkg}",
            "auto": True,
            "install_argv": [sys.executable, "-m", "pip", "install", pkg],
        })
    ok, detail = can_render_report()
    out.append({
        "what": "consultation report PDF (bundled fonts)", "ok": ok,
        "cost": "consultation report PDF delivery is unavailable",
        "fix": "run scripts/setup_dependencies.py and verify the bundled report fonts",
        "auto": False, "detail": detail,
    })
    ok, detail = can_render_pdf()
    pdf_fix = ("rerun only the PDF render and verification through the host's approved "
               "trusted or elevated execution route; do not reinstall Tectonic"
               if detail.startswith(HOST_EXECUTION_REQUIRED) else install_hint("tectonic"))
    out.append({
        "what": "template-based CV/letter PDF (render_cv; optional for reports)", "ok": ok,
        "cost": "PDF CVs and letters from render_cv/render_letter are unavailable; "
                "bundled report PDFs, Markdown and .docx use separate capabilities",
        "fix": pdf_fix,
        "auto": False, "detail": detail,
    })
    out.append({
        "what": "read text back out of a PDF (pdftotext)",
        "ok": bool(shutil.which("pdftotext")),
        "cost": "check_pages cannot verify a template-based CV; "
                "report delivery can still verify text using PyMuPDF",
        "fix": install_hint("pdftotext"), "auto": False,
    })
    office = office_binary()
    out.append({
        "what": "measure Word page counts (LibreOffice soffice)",
        "ok": bool(office),
        "cost": "check_pages reports DOCX_NOT_MEASURED for cv.docx and letter.docx, "
                "so check_apply cannot pass a delivery that includes Word files",
        "fix": install_hint("soffice"), "auto": False,
        **({"detail": office} if office else {}),
    })
    out.append({
        "what": "job adapters (opencli)", "ok": bool(opencli_tools()[0]),
        "cost": "OpenCLI adapters are unavailable; verify daily-browser CDP separately "
                "or use a pasted posting",
        "fix": install_hint("opencli"), "auto": False,
    })
    if opencli_tools()[0]:
        connected, detail = can_use_opencli_cdp()
        out.append({
            "what": "OpenCLI website CDP routing", "ok": connected,
            "cost": detail + "; this OpenCLI route is unverified, not an empty result; check CDP separately",
            "fix": "verify the daily-browser CDP route in references/daily-browser.md",
            "auto": False, "detail": detail,
        })
    return out


def install_python(missing: list[dict]) -> int:
    installed = 0
    for c in missing:
        print(f"installing: {c['fix']}")
        r = subprocess.run(c["install_argv"], capture_output=True, text=True, encoding="utf-8")
        if r.returncode == 0:
            installed += 1
            print(f"  ok: {c['what']}")
        else:
            print(f"  FAILED: {c['what']}\n{(r.stderr or '').strip()[:400]}",
                  file=sys.stderr)
    return installed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--install", action="store_true",
                    help="install missing Python packages; agent handles other tools via references/agent-setup.md")
    args = ap.parse_args(argv)

    results = checks()
    if args.install:
        auto = [c for c in results if not c["ok"] and c.get("auto")]
        if auto:
            install_python(auto)
            results = checks()
        else:
            print("nothing to install: no Python package is missing")

    print(f"job-hunt environment — {platform.system()}, python "
          f"{sys.version.split()[0]}\n")
    for c in results:
        mark = "OK  " if c["ok"] else "MISS"
        extra = f"  ({c['detail']})" if c.get("detail") else ""
        print(f"  [{mark}] {c['what']}{extra}")

    missing = [c for c in results if not c["ok"]]
    if not missing:
        print("\nEverything this skill needs is present.")
        return 0

    print("\nMissing, and what each one costs:\n")
    for c in missing:
        print(f"  {c['what']}")
        print(f"    without it: {c['cost']}")
        print(f"    fix:        {c['fix']}")
    auto = [c for c in missing if c.get("auto")]
    if auto and not args.install:
        print("\nRe-run with --install to install the missing Python packages.")
    print("\nAgent: resolve required missing capabilities using "
          "references/agent-setup.md, then re-run the checks. "
          "Prepare the selected browser's CDP connection.")
    return 1


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
