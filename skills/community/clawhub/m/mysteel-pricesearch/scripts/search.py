#!/usr/bin/env python3
"""
Mysteel Price Search API Client

Queries the Mysteel AI search API for commodity price data.
Supports futures, spot prices, macroeconomic indicators, and more.

Usage:
    python search.py "<query_text>"

Examples:
    python search.py "鸡蛋最新收盘价"
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

API_URL = "https://mcp.mysteel.com/mcp/info/ai-search/search"
DEFAULT_SOURCE = "MyClaw模式"
SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
API_KEY_FILE = SKILL_DIR / "references" / "api_key.md"
DEFAULT_OUTPUT_DIR = SKILL_DIR / "output"


def load_api_key() -> str | None:
    """
    Load API key from file.
    Returns the API key if found and valid, None otherwise.
    """
    if API_KEY_FILE.exists():
        content = API_KEY_FILE.read_text(encoding="utf-8")
        lines = content.strip().splitlines()
        if len(lines) >= 1 and lines[0] and not lines[0].startswith("YOUR_API_KEY"):
            return lines[0].strip()
    return None


def sanitize_filename(name: str) -> str:
    """
    Clean filename by replacing invalid characters.
    Returns a sanitized filename safe for filesystem.
    """
    # Replace invalid characters: : / \ * ? " < > |
    return re.sub(r'[:/\\*?"<>|]', '_', name).strip()


def cleanup_old_files(output_dir: Path, max_age_hours: int = 24) -> int:
    """
    Delete CSV files older than specified age.
    Returns the number of files deleted.
    """
    if not output_dir.exists():
        return 0

    deleted_count = 0
    cutoff_time = datetime.now() - timedelta(hours=max_age_hours)

    for file in output_dir.glob("*.csv"):
        try:
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if mtime < cutoff_time:
                file.unlink()
                deleted_count += 1
        except Exception:
            # Skip files that can't be accessed
            pass

    return deleted_count


def cleanup_excess_files(output_dir: Path, max_files: int = 100) -> int:
    """
    Delete oldest CSV files when file count exceeds limit.
    Returns the number of files deleted.
    """
    if not output_dir.exists():
        return 0

    # Get all CSV files with their modification times
    files = []
    for file in output_dir.glob("*.csv"):
        try:
            files.append((file, file.stat().st_mtime))
        except Exception:
            pass

    # Sort by modification time (newest first)
    files.sort(key=lambda x: x[1], reverse=True)

    # Delete files exceeding the limit
    deleted_count = 0
    if len(files) > max_files:
        for file, _ in files[max_files:]:
            try:
                file.unlink()
                deleted_count += 1
            except Exception:
                # Continue on error
                pass

    return deleted_count


def save_to_csv(result: dict, output_dir: Path, options: dict | None = None) -> list[dict]:
    """
    Save API response data to CSV files.
    Returns list of saved file info.
    """
    if options is None:
        options = {}

    limit = options.get("limit", 0)
    start_date = options.get("start_date")
    end_date = options.get("end_date")
    cleanup = options.get("cleanup", True)
    max_files = options.get("max_files", 100)

    saved_files = []

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Clean up old CSV files (older than 1 day)
    if cleanup:
        deleted = cleanup_old_files(output_dir)
        if deleted > 0:
            print(f"Cleaned up {deleted} old CSV file(s).")

    # Clean up excess files (keep only max_files newest files)
    deleted = cleanup_excess_files(output_dir, max_files)
    if deleted > 0:
        print(f"Removed {deleted} excess CSV file(s) (keeping {max_files} newest).")

    # Extract indexData from response
    index_data = result.get("data", {}).get("indexData", [])

    if not index_data:
        return saved_files

    for item in index_data:
        # Get index name (prefer indexName over indexShortName)
        index_name = item.get("indexName") or item.get("indexShortName") or "unknown"
        unit = item.get("unitName", "")
        data_map = item.get("dataMap", {})

        if not data_map:
            continue

        # Create safe filename
        safe_name = sanitize_filename(index_name)
        filename = f"{safe_name}.csv"
        filepath = output_dir / filename

        # Sort dates in descending order (newest first)
        sorted_dates = sorted(data_map.keys(), reverse=True)

        # Apply date filters
        if start_date:
            sorted_dates = [d for d in sorted_dates if d >= start_date]
        if end_date:
            sorted_dates = [d for d in sorted_dates if d <= end_date]

        # Apply limit (if specified)
        if limit > 0 and len(sorted_dates) > limit:
            sorted_dates = sorted_dates[:limit]

        if not sorted_dates:
            continue

        # Calculate changes and build rows
        rows = []
        prev_price = None

        for date in sorted_dates:
            price_str = data_map[date]
            change = ""
            change_pct = ""

            if prev_price is not None:
                try:
                    price = float(price_str)
                    diff = price - prev_price
                    if diff != 0:
                        change = f"+{diff:.2f}" if diff >= 0 else f"{diff:.2f}"
                    else:
                        change = "0"
                    if prev_price != 0:
                        pct = (diff / prev_price) * 100
                        change_pct = f"+{pct:.2f}%" if pct >= 0 else f"{pct:.2f}%"
                except (ValueError, TypeError):
                    # Ignore parsing errors
                    pass

            rows.append({
                "date": date,
                "price": price_str,
                "unit": unit,
                "change": change,
                "change_pct": change_pct
            })

            # Update prev_price for next iteration
            try:
                prev_price = float(price_str)
            except (ValueError, TypeError):
                prev_price = None

        # Write CSV file with metadata header
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        lines = []
        lines.append(f"# index_name: {index_name}")
        lines.append(f"# unit: {unit}")
        lines.append(f"# total_rows: {len(rows)}")
        lines.append(f"# date_range: {sorted_dates[-1]} ~ {sorted_dates[0]}")
        if start_date:
            lines.append(f"# filter_start: {start_date}")
        if end_date:
            lines.append(f"# filter_end: {end_date}")
        if limit > 0:
            lines.append(f"# limit: {limit}")
        lines.append(f"# generated: {timestamp}")
        lines.append("#")

        # Write CSV header and rows
        lines.append("date,price,unit,change,change_pct")
        for row in rows:
            lines.append(f"{row['date']},{row['price']},{row['unit']},{row['change']},{row['change_pct']}")

        filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")

        saved_files.append({
            "filename": filename,
            "rows": len(rows),
            "index_name": index_name,
            "date_range": f"{sorted_dates[-1]} ~ {sorted_dates[0]}"
        })

    return saved_files


def search_price(text: str, api_key: str, options: dict | None = None) -> dict:
    """
    Query the Mysteel price search API.
    Returns the API response as a dictionary.
    """
    if options is None:
        options = {}

    index_search = options.get("index_search", True)
    info_search = options.get("info_search", False)
    static_knowledge_enable = options.get("static_knowledge_enable", True)

    payload = {
        "source": DEFAULT_SOURCE,
        "text": text,
        "indexSearchEnable": index_search,
        "infoSearchEnable": info_search,
        "staticKnowledgeEnable": static_knowledge_enable
    }

    headers = {
        "Content-Type": "application/json",
        "token": api_key
    }

    try:
        import urllib.request
        import urllib.error

        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=60) as response:
            if response.status != 200:
                error_body = response.read().decode("utf-8", errors="ignore")
                return {
                    "error": True,
                    "status_code": response.status,
                    "message": error_body
                }
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        return {
            "error": True,
            "status_code": e.code,
            "message": error_body
        }
    except urllib.error.URLError as e:
        return {
            "error": True,
            "message": f"URL Error: {e.reason}"
        }
    except json.JSONDecodeError as e:
        return {
            "error": True,
            "message": f"JSON Decode Error: {e}"
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"Error: {e}"
        }


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Mysteel Price Search API Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python search.py "螺纹钢最新价格"
    python search.py "螺纹钢最新价格" --csv --limit 10
    python search.py "铜期货价格" --csv --days 30
    python search.py "热卷价格" --csv --start-date 2024-01-01 --end-date 2024-03-31
        """
    )

    parser.add_argument("text", nargs="?", help="Query text to search")
    parser.add_argument("--csv", action="store_true", help="Save results to CSV files in output directory")
    parser.add_argument("--output-dir", help="Output directory for CSV files (default: skill/output)")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of data rows per CSV file (0 = no limit)")
    parser.add_argument("--start-date", help="Start date filter (YYYY-MM-DD format, inclusive)")
    parser.add_argument("--end-date", help="End date filter (YYYY-MM-DD format, inclusive)")
    parser.add_argument("--days", type=int, default=0, help="Query last N days of data (alternative to start-date)")
    parser.add_argument("--max-files", type=int, default=100, help="Maximum number of CSV files to keep (default: 100)")

    return parser.parse_args()


def main():
    args = parse_args()

    if not args.text:
        parser = argparse.ArgumentParser()
        parser.print_help()
        sys.exit(1)

    # Load API key from file
    api_key = load_api_key()
    if not api_key:
        print("Error: API key is required. Save it in references/api_key.md", file=sys.stderr)
        sys.exit(1)

    result = search_price(
        args.text,
        api_key,
        {
            "index_search": True,
            "info_search": False,
            "static_knowledge_enable": True
        }
    )

    # Handle errors
    if result.get("error"):
        print(f"Error: {result.get('message', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)

    # Calculate start_date from --days if specified
    start_date = args.start_date
    if args.days > 0 and not start_date:
        date = datetime.now() - timedelta(days=args.days)
        start_date = date.strftime("%Y-%m-%d")

    # CSV output mode
    if args.csv:
        output_dir = Path(args.output_dir) if args.output_dir else DEFAULT_OUTPUT_DIR
        saved_files = save_to_csv(result, output_dir, {
            "limit": args.limit,
            "start_date": start_date,
            "end_date": args.end_date,
            "max_files": args.max_files
        })

        if saved_files:
            print(f"Generated {len(saved_files)} CSV file(s) in {output_dir}:")
            for file in saved_files:
                print(f"  - {file['filename']} ({file['rows']} rows, {file['date_range']})")
        else:
            print("No data found to save to CSV.", file=sys.stderr)
        return

    # Raw or pretty JSON output
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()