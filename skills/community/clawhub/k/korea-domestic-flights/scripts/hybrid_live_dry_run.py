#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common_cli import normalize_airport



def main():
    parser = argparse.ArgumentParser(description="Shallow live dry-run / DOM drift sanity check for korea-domestic-flights")
    parser.add_argument("--origin", default="김포")
    parser.add_argument("--destination", default="제주")
    parser.add_argument("--departure", default="내일", help="Currently informational only; live probe uses broad date-range scanner.")
    parser.add_argument("--probe", action="store_true", help="Actually attempt a 1-day broad scan. Without this flag, only environment/import checks run.")
    args = parser.parse_args()

    workspace = Path(__file__).resolve().parents[3]
    repo_path = workspace / "tmp" / "Scraping-flight-information"
    report = {
        "status": "ok",
        "mode": "live_probe" if args.probe else "env_only",
        "checks": [],
        "repo_path": str(repo_path),
        "probe": None,
    }

    report["checks"].append({"name": "repo_exists", "ok": repo_path.exists()})
    if not repo_path.exists():
        report["status"] = "degraded"
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(0)

    sys.path.insert(0, str(repo_path))

    try:
        from scraping.parallel import ParallelSearcher
    except Exception as exc:
        report["status"] = "degraded"
        report["checks"].append({"name": "import_parallel_searcher", "ok": False, "error": str(exc)})
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(0)

    report["checks"].append({"name": "import_parallel_searcher", "ok": True})

    if not args.probe:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    try:
        origin = normalize_airport(args.origin)
        destination = normalize_airport(args.destination)
    except Exception as exc:
        report["status"] = "degraded"
        report["probe"] = {"ok": False, "error": f"invalid route input: {exc}"}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(0)

    searcher = ParallelSearcher()
    probe_logs = []
    try:
        raw = searcher.search_date_range(
            origin=origin,
            destination=destination,
            dates=[],
            return_offset=0,
            adults=1,
            cabin_class="ECONOMY",
            progress_callback=lambda msg: probe_logs.append(str(msg)),
        )
        report["probe"] = {
            "ok": isinstance(raw, dict),
            "route": f"{origin}-{destination}",
            "raw_type": type(raw).__name__,
            "keys": list(raw.keys())[:5],
            "log_preview": probe_logs[:10],
            "note": "Empty-date broad scan probe completed. This validates import + shallow execution path without asserting fare availability.",
        }
    except TypeError as exc:
        report["status"] = "degraded"
        report["probe"] = {
            "ok": False,
            "route": f"{origin}-{destination}",
            "error": str(exc),
            "note": "ParallelSearcher.search_date_range signature or call contract may have drifted.",
        }
    except Exception as exc:
        report["status"] = "degraded"
        report["probe"] = {
            "ok": False,
            "route": f"{origin}-{destination}",
            "error": str(exc),
            "log_preview": probe_logs[:10],
            "note": "Live probe failed; inspect upstream scraper/browser environment or DOM drift.",
        }
    finally:
        close_fn = getattr(searcher, "close", None)
        if callable(close_fn):
            try:
                close_fn()
            except Exception:
                pass

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
