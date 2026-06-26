import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CATALOG_PATH = BASE_DIR / "catalog.json"

AUTOMATED_SOURCES = {"flatpak", "snap", "apt", "dnf", "zypper", "pacman", "aur", "nix"}
SKIPPED_SOURCES = {"manual", "wine", "appimage"}
SOURCE_TOOLS = {
    "flatpak": ("flatpak",),
    "snap": ("snap",),
    "apt": ("apt-cache",),
    "dnf": ("dnf",),
    "zypper": ("zypper",),
    "pacman": ("pacman",),
    "aur": ("yay", "paru"),
    "nix": ("nix",),
}
COMMAND_TIMEOUTS = {
    "flatpak": 20,
    "snap": 15,
    "apt": 10,
    "dnf": 15,
    "zypper": 15,
    "pacman": 10,
    "aur": 20,
    "nix": 20,
}


def load_catalog():
    with CATALOG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_command(parts, timeout=None):
    return subprocess.run(parts, capture_output=True, text=True, check=False, timeout=timeout)


def detect_available_tools():
    available = {}
    for source, tool_names in SOURCE_TOOLS.items():
        available[source] = next((tool for tool in tool_names if shutil.which(tool)), None)
    return available


def normalize_whitespace(value):
    return re.sub(r"\s+", " ", value.strip())


def validate_flatpak(package):
    result = run_command(
        ["flatpak", "search", "--columns=application", package],
        timeout=COMMAND_TIMEOUTS["flatpak"],
    )
    if result.returncode != 0:
        return False, f"flatpak search failed: {normalize_whitespace(result.stderr or result.stdout)}"
    matches = [line.strip() for line in result.stdout.splitlines() if line.strip() and line.strip().lower() != "application"]
    if package in matches:
        return True, None
    return False, "Exact Flatpak app ID not found in search results"


def validate_snap(package):
    result = run_command(["snap", "find", package], timeout=COMMAND_TIMEOUTS["snap"])
    output = normalize_whitespace(result.stderr or result.stdout)
    lower_output = output.lower()
    if result.returncode != 0:
        if (
            "cannot communicate with server" in lower_output
            or "/run/snapd.socket" in lower_output
            or "snapd.socket" in lower_output
        ):
            return None, f"Snap search is unavailable on this host: {output}"
        return False, f"snap find failed: {output}"
    for raw_line in result.stdout.splitlines():
        line = raw_line.rstrip()
        if not line or line.startswith("Name") or line.startswith("---"):
            continue
        parts = re.split(r"\s{2,}", line.strip())
        if parts and parts[0] == package:
            return True, None
    return False, "Exact snap name not found in search results"


def validate_apt(package):
    result = run_command(["apt-cache", "show", package], timeout=COMMAND_TIMEOUTS["apt"])
    if result.returncode == 0 and "Package:" in result.stdout:
        return True, None
    return False, f"apt-cache show did not find package {package}"


def validate_dnf(package):
    result = run_command(["dnf", "info", package], timeout=COMMAND_TIMEOUTS["dnf"])
    if result.returncode == 0 and normalize_whitespace(result.stdout):
        return True, None
    return False, f"dnf info did not find package {package}"


def validate_zypper(package):
    result = run_command(
        ["zypper", "--non-interactive", "info", package],
        timeout=COMMAND_TIMEOUTS["zypper"],
    )
    output = normalize_whitespace(result.stdout + "\n" + result.stderr)
    if result.returncode == 0 and "not found" not in output.lower():
        return True, None
    return False, f"zypper info did not find package {package}"


def validate_pacman(package):
    result = run_command(["pacman", "-Si", package], timeout=COMMAND_TIMEOUTS["pacman"])
    if result.returncode == 0 and normalize_whitespace(result.stdout):
        return True, None
    return False, f"pacman -Si did not find package {package}"


def validate_aur(package, helper):
    result = run_command([helper, "-Si", package], timeout=COMMAND_TIMEOUTS["aur"])
    if result.returncode == 0 and normalize_whitespace(result.stdout):
        return True, None
    return False, f"{helper} -Si did not find package {package}"


def validate_nix(package):
    result = run_command(["nix", "search", "nixpkgs", package], timeout=COMMAND_TIMEOUTS["nix"])
    output = result.stdout + "\n" + result.stderr
    normalized_output = normalize_whitespace(output)
    lower_output = normalized_output.lower()
    if result.returncode != 0 and not normalized_output:
        return False, "nix search failed without output"
    if (
        "permission denied" in lower_output
        or "experimental nix feature 'nix-command' is disabled" in lower_output
        or "experimental feature 'nix-command' is disabled" in lower_output
    ):
        return None, f"Nix search is unavailable on this host: {normalized_output}"

    normalized_package = re.escape(package).replace(r"\-", r"[-_]")
    pattern = re.compile(rf"(legacyPackages\.[^.]+\.)?{normalized_package}\b")
    if pattern.search(output):
        return True, None
    return False, "Exact nix attribute was not visible in search results"


def validate_candidate(candidate, available_tools):
    source = candidate["source"]
    package = candidate["package"]

    if source in SKIPPED_SOURCES:
        return {"status": "skipped", "detail": f"Source {source} is intentionally not machine-validated"}

    if source not in AUTOMATED_SOURCES:
        return {"status": "skipped", "detail": f"Unsupported source {source}"}

    tool = available_tools.get(source)
    if not tool:
        return {"status": "skipped", "detail": f"Required tool for {source} is not installed"}

    try:
        if source == "flatpak":
            ok, detail = validate_flatpak(package)
        elif source == "snap":
            ok, detail = validate_snap(package)
        elif source == "apt":
            ok, detail = validate_apt(package)
        elif source == "dnf":
            ok, detail = validate_dnf(package)
        elif source == "zypper":
            ok, detail = validate_zypper(package)
        elif source == "pacman":
            ok, detail = validate_pacman(package)
        elif source == "aur":
            ok, detail = validate_aur(package, tool)
        elif source == "nix":
            ok, detail = validate_nix(package)
        else:
            return {"status": "skipped", "detail": f"No validator implemented for {source}"}
    except Exception as exc:  # pragma: no cover - defensive fallback
        if isinstance(exc, subprocess.TimeoutExpired):
            return {
                "status": "skipped",
                "detail": f"Validation timed out for {source} candidate {package}",
            }
        return {"status": "error", "detail": str(exc)}

    if ok is None:
        return {"status": "skipped", "detail": detail}
    return {"status": "ok" if ok else "missing", "detail": detail}


def iter_catalog_candidates(catalog):
    for app_key, app in catalog["apps"].items():
        for index, candidate in enumerate(app["candidates"]):
            yield app_key, app, index, candidate


def format_result_line(item):
    line = f"[{item['status'].upper()}] {item['display_name']} :: {item['source']} :: {item['package']}"
    if item["detail"]:
        line = f"{line} :: {item['detail']}"
    return line


def validate_catalog(source_filter=None, on_result=None):
    catalog = load_catalog()
    available_tools = detect_available_tools()
    results = []

    for app_key, app, index, candidate in iter_catalog_candidates(catalog):
        if source_filter and candidate["source"] != source_filter:
            continue
        verdict = validate_candidate(candidate, available_tools)
        item = {
            "app_key": app_key,
            "display_name": app["display_name"],
            "candidate_index": index,
            "source": candidate["source"],
            "package": candidate["package"],
            "status": verdict["status"],
            "detail": verdict["detail"],
        }
        results.append(item)
        if on_result:
            on_result(item)
    return results


def summarize_results(results):
    summary = {"ok": 0, "missing": 0, "skipped": 0, "error": 0}
    for item in results:
        summary[item["status"]] += 1
    summary["checked"] = len(results)
    return summary


def print_text_report(results):
    for item in results:
        print(format_result_line(item))
    summary = summarize_results(results)
    print(
        "Summary:"
        f" checked={summary['checked']}"
        f" ok={summary['ok']}"
        f" missing={summary['missing']}"
        f" skipped={summary['skipped']}"
        f" error={summary['error']}"
    )


def build_parser():
    parser = argparse.ArgumentParser(prog="validate_catalog")
    parser.add_argument(
        "--source",
        choices=sorted(AUTOMATED_SOURCES | SKIPPED_SOURCES),
        help="Validate only candidates from a specific source",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the full report as JSON",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    on_result = (lambda item: print(format_result_line(item), flush=True)) if not args.json else None
    results = validate_catalog(source_filter=args.source, on_result=on_result)
    summary = summarize_results(results)

    if args.json:
        json.dump({"results": results, "summary": summary}, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(
            "Summary:"
            f" checked={summary['checked']}"
            f" ok={summary['ok']}"
            f" missing={summary['missing']}"
            f" skipped={summary['skipped']}"
            f" error={summary['error']}"
        )

    return 1 if summary["missing"] or summary["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
