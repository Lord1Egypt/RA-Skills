#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_CSV="$SKILL_DIR/sample-data/sample-transactions.csv"
DEFAULT_RULES="$SKILL_DIR/config/category-rules.json"

usage() {
  cat <<'USAGE'
Usage: personal-finance.sh <command> [--csv <path>] [--config <path>] [--period <month|quarter|year>] [--output <path>]
Commands:
  validate   Verify CSV schema (date, description, amount, account_number) and numeric amounts.
  summarize  Show income/expense totals grouped by the selected period (default: month).
  categorize Match transactions to categories via keyword rules and optionally write a categorized CSV.
  report     Print a quick-run insights summary (top merchants/categories, totals).

All commands default to read-only mode unless you pass --output to categorize. Passage of --csv and --config overrides the bundled samples.
USAGE
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

COMMAND="$1"
shift

CSV_PATH="$DEFAULT_CSV"
RULES_PATH="$DEFAULT_RULES"
PERIOD="month"
OUTPUT_PATH=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --csv)
      CSV_PATH="$2"
      shift 2
      ;;
    --config)
      RULES_PATH="$2"
      shift 2
      ;;
    --period)
      PERIOD="$2"
      shift 2
      ;;
    --output)
      OUTPUT_PATH="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ ! -f "$CSV_PATH" ]]; then
  echo "CSV file not found: $CSV_PATH" >&2
  exit 1
fi

if [[ ! -f "$RULES_PATH" ]]; then
  echo "Rules file not found: $RULES_PATH" >&2
  exit 1
fi

python3 - "$COMMAND" "$CSV_PATH" "$RULES_PATH" "$PERIOD" "$OUTPUT_PATH" <<'PY'
import sys
import csv
import json
from pathlib import Path
from decimal import Decimal, InvalidOperation
from datetime import datetime

COMMAND = sys.argv[1]
CSV_PATH = Path(sys.argv[2])
RULES_PATH = Path(sys.argv[3])
PERIOD = sys.argv[4].lower()
OUTPUT_PATH = sys.argv[5]

REQUIRED_COLUMNS = {"date", "description", "amount", "account_number"}
PERIOD_OPTIONS = {"month", "quarter", "year"}

class FinanceError(Exception):
    pass


def mask_account(value):
    if value is None:
        return ""
    text = str(value)
    digit_positions = [idx for idx, ch in enumerate(text) if ch.isdigit()]
    mask_count = max(len(digit_positions) - 4, 0)
    mask_positions = set(digit_positions[:mask_count])
    return "".join("*" if idx in mask_positions else ch for idx, ch in enumerate(text))


def normalize_amount(raw):
    if raw is None:
        raise FinanceError("Missing amount")
    text = str(raw).strip()
    if not text:
        raise FinanceError("Amount empty")
    clean = text.replace("$", "").replace(",", "")
    if clean.startswith("(") and clean.endswith(")"):
        clean = "-" + clean[1:-1]
    try:
        return Decimal(clean)
    except InvalidOperation as exc:
        raise FinanceError(f"Invalid amount in row (value redacted)") from exc


def parse_date(raw):
    if not raw:
        return None
    text = raw.strip()
    try:
        parsed = datetime.fromisoformat(text)
        return parsed.date()
    except ValueError:
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(text, fmt).date()
            except ValueError:
                continue
    return None


def read_rows():
    file_size = CSV_PATH.stat().st_size
    MAX_SIZE = 50 * 1024 * 1024  # 50MB
    if file_size > MAX_SIZE:
        raise FinanceError(f"CSV file too large ({file_size} bytes). Max: {MAX_SIZE}")
    
    with CSV_PATH.open(newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise FinanceError("CSV has no header")
        headers = []
        for name in reader.fieldnames:
            if not name:
                continue
            trimmed = name.strip()
            if not trimmed:
                continue
            headers.append((name, trimmed.lower()))
        canonical = [canonical for _, canonical in headers]
        rows = []
        for row in reader:
            if all((cell is None or not cell.strip()) for cell in row.values()):
                continue
            normalized = {}
            for raw, canonical_name in headers:
                cell = row.get(raw, "")
                normalized[canonical_name] = cell.strip() if cell is not None else ""
            rows.append(normalized)
        return canonical, rows


def load_rules():
    raw = RULES_PATH.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FinanceError(f"Rules file is not valid JSON ({exc})") from exc
    if not isinstance(data, list):
        raise FinanceError("Rules file must be a list of category objects")
    cleaned = []
    for entry in data:
        category = entry.get("category")
        keywords = entry.get("keywords")
        if not category or not keywords:
            continue
        cleaned.append({"category": category, "keywords": [kw.strip().lower() for kw in keywords if kw]})
    return cleaned


def check_required(fieldnames):
    missing = REQUIRED_COLUMNS - set(fieldnames)
    if missing:
        raise FinanceError(f"Missing required columns: {', '.join(sorted(missing))}")


def validate_rows(fieldnames, rows):
    check_required(fieldnames)
    issues = []
    for idx, row in enumerate(rows, start=2):
        try:
            normalize_amount(row.get("amount"))
        except FinanceError as exc:
            issues.append(f"Row {idx}: Invalid amount in row (value redacted)")
    if issues:
        raise FinanceError("\n".join(issues))
    print(f"Validation succeeded: {len(rows)} transaction(s) look good.")


def period_key(date_obj):
    if date_obj is None:
        return "Unknown"
    if PERIOD == "month":
        return date_obj.strftime("%Y-%m")
    if PERIOD == "quarter":
        quarter = (date_obj.month - 1) // 3 + 1
        return f"{date_obj.year}-Q{quarter}"
    if PERIOD == "year":
        return str(date_obj.year)
    raise FinanceError(f"Unsupported period: {PERIOD}")


def summarize_rows(rows):
    if PERIOD not in PERIOD_OPTIONS:
        raise FinanceError(f"Invalid period '{PERIOD}' (choose: month, quarter, year)")
    totals = {}
    for idx, row in enumerate(rows, start=2):
        try:
            amt = normalize_amount(row.get("amount"))
        except FinanceError:
            raise FinanceError(f"Row {idx}: Amount validation failed")
        dt = parse_date(row.get("date", ""))
        key = period_key(dt)
        period_data = totals.setdefault(key, {"income": Decimal("0"), "expense": Decimal("0")})
        if amt >= 0:
            period_data["income"] += amt
        else:
            period_data["expense"] += -amt
    print(f"Summary by {PERIOD}:" )
    print(f"{'Period':<12} {'Income':>12} {'Expense':>12} {'Net':>12}")
    for key in sorted(totals):
        data = totals[key]
        income = data["income"]
        expense = data["expense"]
        net = income - expense
        print(f"{key:<12} {format_money(income):>12} {format_money(expense):>12} {format_money(net):>12}")


def format_money(value):
    return f"${value:,.2f}"


def assign_category(row, rules):
    existing = row.get("category")
    if existing:
        return existing
    text = " ".join(filter(None, [row.get("description", ""), row.get("merchant", "")])).lower()
    for rule in rules:
        for keyword in rule["keywords"]:
            if keyword in text:
                return rule["category"]
    return "Uncategorized"


def categorize_rows(fieldnames, rows):
    rules = load_rules()
    categorized = []
    for row in rows:
        category = assign_category(row, rules)
        row["category"] = category
        categorized.append(row)
    headers = list(fieldnames)
    if "category" not in headers:
        headers.append("category")
    print("Categorized transactions (account numbers masked):")
    print(f"{'Date':<12} {'Description':<36} {'Amount':>10} {'Category':<20} {'Account':<15}")
    for row in categorized:
        amt = normalize_amount(row.get("amount"))
        masked = mask_account(row.get("account_number"))
        desc = row.get("description", "")[:34]
        print(f"{row.get('date',''):<12} {desc:<36} {format_money(amt):>10} {row.get('category',''):<20} {masked:<15}")
    if OUTPUT_PATH:
        out_path = Path(OUTPUT_PATH)
        if out_path.exists():
            print(f"Warning: {out_path} already exists and will be overwritten.", file=sys.stderr)
        if out_path.is_absolute() and not str(out_path).startswith(str(Path.home())):
            raise FinanceError(f"Output path must be in user home directory for safety")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", newline="", encoding="utf-8") as ostream:
            writer = csv.DictWriter(ostream, fieldnames=headers)
            writer.writeheader()
            for row in categorized:
                if "account_number" in row:
                    row["account_number"] = mask_account(row["account_number"])
                writer.writerow(row)
        print(f"Written categorized CSV to: {out_path}")
    else:
        print("No --output provided; transactions were not written back.")


def report_rows(rows):
    rules = load_rules()
    category_stats = {}
    merchant_stats = {}
    income = Decimal("0")
    expense = Decimal("0")
    for row in rows:
        amt = normalize_amount(row.get("amount"))
        if amt >= 0:
            income += amt
        else:
            expense += -amt
        category = assign_category(row, rules)
        category_data = category_stats.setdefault(category, {"amount": Decimal("0"), "count": 0})
        category_data["amount"] += amt
        category_data["count"] += 1
        merchant = row.get("merchant") or row.get("description")
        merchant_data = merchant_stats.setdefault(merchant, {"amount": Decimal("0"), "count": 0})
        merchant_data["amount"] += amt
        merchant_data["count"] += 1
    print("Personal-finance report")
    print("Totals:")
    print(f"  Income : {format_money(income)}")
    print(f"  Expense: {format_money(expense)}")
    print(f"  Net    : {format_money(income - expense)}")
    print("\nTop categories (by absolute spend):")
    for cat, stats in sorted(category_stats.items(), key=lambda item: abs(item[1]["amount"]), reverse=True)[:5]:
        print(f"  {cat:<22} {format_money(stats['amount']):>12} ({stats['count']} tx)")
    print("\nTop merchants (by absolute spend):")
    for merch, stats in sorted(merchant_stats.items(), key=lambda item: abs(item[1]["amount"]), reverse=True)[:5]:
        name = merch or "(unknown merchant)"
        print(f"  {name:<22} {format_money(stats['amount']):>12} ({stats['count']} tx)")


def main():
    fieldnames, rows = read_rows()
    if COMMAND == "validate":
        validate_rows(fieldnames, rows)
        return
    if COMMAND == "summarize":
        summarize_rows(rows)
        return
    if COMMAND == "categorize":
        categorize_rows(fieldnames, rows)
        return
    if COMMAND == "report":
        report_rows(rows)
        return
    raise FinanceError(f"Unknown command '{COMMAND}'")

if __name__ == "__main__":
    try:
        main()
    except FinanceError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
PY
