---
name: plutus
description: "Plutus — God of Wealth. Parse receipts and expense descriptions into a categorised expense report. Paste raw text, a list, or point to a CSV of transactions and get back a clean report with categories, totals, monthly trends, and a budget vs actual comparison. Works for personal finances, freelancers, or small business bookkeeping."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: []
      bins: [python3, pip3]
    primaryEnv: "EXPENSES_FILE"
    homepage: https://clawhub.ai/occupythemilkyway/plutus
    emoji: "💰📊"
    tags: [finance, expenses, budget, bookkeeping, tracker, plutus, receipts, categories]
    envVars:
      - name: EXPENSES_FILE
        description: "Path to a CSV file with columns: date, description, amount (or amount_usd). Amounts can be negative for credits."
        required: false
        default: ""
      - name: EXPENSES_TEXT
        description: "Raw expense list as text, one per line: 'Jan 5 Coffee 4.50' or 'Amazon Prime 14.99'. Used if EXPENSES_FILE is not set."
        required: false
        default: ""
      - name: BUDGET_JSON
        description: "JSON string of monthly budget limits per category, e.g. '{\"food\":500,\"transport\":150}'"
        required: false
        default: ""
      - name: CURRENCY
        description: "Currency symbol to display (e.g. USD, EUR, GBP, CAD)"
        required: false
        default: "USD"
      - name: REPORT_MONTH
        description: "Filter to a specific month (YYYY-MM format, e.g. 2025-01). Leave blank for all months."
        required: false
        default: ""
---

# Plutus — Expense Tracker & Budget Analyser

Turn a messy list of transactions into a clean, categorised expense report with totals, trends, and budget comparison — no spreadsheet required.

## What you get

- **Auto-categorisation** of transactions into 15+ categories using keyword matching
- **Totals by category** with percentage breakdown
- **Monthly trend table** showing spend per category per month
- **Budget vs actual** comparison (set your own limits via `BUDGET_JSON`)
- **Top 10 biggest transactions** highlighted
- **Export**: Markdown report + CSV summary saved to disk

## Input formats

**CSV file** (set `EXPENSES_FILE`):
```
date,description,amount
2025-01-05,Coffee at Starbucks,4.50
2025-01-10,Amazon Prime subscription,14.99
2025-01-15,Grocery run Walmart,-200.00
```

**Plain text** (set `EXPENSES_TEXT`):
```
Jan 5 Coffee 4.50
Amazon Prime 14.99
Jan 15 Groceries Walmart 200
Uber ride 22.50
```

## 🔒 Security

Runs entirely locally. No data transmitted. Your financial data stays on your machine.

---

## Step 1 — Install

```bash
pip3 install rich --break-system-packages --quiet
```

---


---

## ⚡ Upgrade to Plutus Pro

👉 **Get Plutus Pro** → **ko-fi.com/s/83c662001e** — $9 one-time

```bash
openclaw skills install plutus-pro
# Set LICENSE_KEY env var to your key from Ko-fi, then run
```

💰 **Bundle deal:** all 5 Pro skills for **$29** → **ko-fi.com/s/7625accf3f** (save $16)

## Step 2 — Analyse your expenses

```python
import os, re, json, csv
from datetime import datetime, date
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

EXPENSES_FILE  = os.environ.get("EXPENSES_FILE", "").strip()
EXPENSES_TEXT  = os.environ.get("EXPENSES_TEXT", "").strip()
BUDGET_RAW     = os.environ.get("BUDGET_JSON", "").strip()
CURRENCY       = os.environ.get("CURRENCY", "USD").upper()
REPORT_MONTH   = os.environ.get("REPORT_MONTH", "").strip()
TODAY          = date.today()

# ── Category rules ────────────────────────────────────────────────────────────
CATEGORIES = {
    "Food & Dining":    ["coffee", "starbucks", "restaurant", "pizza", "burger", "sushi", "cafe",
                         "dining", "food", "doordash", "uber eats", "grubhub", "mcdonalds",
                         "chipotle", "subway", "lunch", "dinner", "breakfast", "grocery", "groceries",
                         "walmart", "whole foods", "trader joe", "supermarket"],
    "Transport":        ["uber", "lyft", "taxi", "gas", "fuel", "parking", "transit", "metro",
                         "bus", "train", "amtrak", "airline", "flight", "airfare", "car rental",
                         "toll", "mileage", "petrol"],
    "Shopping":         ["amazon", "ebay", "etsy", "target", "bestbuy", "best buy", "ikea",
                         "clothing", "apparel", "shoes", "fashion", "zara", "h&m", "gap",
                         "nordstrom", "mall", "store", "shop"],
    "Subscriptions":    ["netflix", "spotify", "hulu", "disney", "apple music", "youtube",
                         "prime", "subscription", "membership", "monthly", "annual fee",
                         "software", "saas", "adobe", "microsoft", "google"],
    "Utilities":        ["electric", "electricity", "water", "gas bill", "internet", "phone",
                         "mobile", "cellular", "at&t", "verizon", "comcast", "xfinity",
                         "hydro", "utility", "bill"],
    "Health":           ["pharmacy", "doctor", "dentist", "medical", "hospital", "clinic",
                         "prescription", "medicine", "health", "gym", "fitness", "yoga",
                         "cvs", "walgreens", "rite aid"],
    "Entertainment":    ["movie", "cinema", "theatre", "concert", "event", "ticket",
                         "game", "gaming", "steam", "playstation", "xbox", "nintendo",
                         "book", "kindle", "audible", "museum", "sport"],
    "Travel":           ["hotel", "airbnb", "hostel", "motel", "resort", "booking",
                         "expedia", "trip", "vacation", "holiday", "travel", "tour"],
    "Education":        ["course", "udemy", "coursera", "tuition", "textbook", "school",
                         "university", "college", "training", "workshop", "class", "lesson"],
    "Home":             ["rent", "mortgage", "furniture", "home depot", "lowes", "hardware",
                         "repair", "maintenance", "cleaning", "plumber", "electrician"],
    "Insurance":        ["insurance", "premium", "policy", "coverage", "geico", "allstate",
                         "progressive", "state farm"],
    "Business":         ["invoice", "client", "freelance", "office", "supplies", "coworking",
                         "conference", "advertising", "marketing", "domain", "hosting"],
    "Personal Care":    ["salon", "haircut", "barber", "spa", "beauty", "cosmetics",
                         "skincare", "makeup", "nails"],
    "Income / Credit":  [],  # used for negative amounts
}

def categorise(description: str, amount: float) -> str:
    if amount < 0:
        return "Income / Credit"
    desc_low = description.lower()
    for cat, keywords in CATEGORIES.items():
        if cat == "Income / Credit":
            continue
        for kw in keywords:
            if kw in desc_low:
                return cat
    return "Other"

# ── Parse amount string ───────────────────────────────────────────────────────
def parse_amount(raw: str) -> float | None:
    raw = raw.strip().lstrip("$£€").replace(",", "")
    try:
        return float(raw)
    except ValueError:
        return None

# ── Parse date string ─────────────────────────────────────────────────────────
MONTH_MAP = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,
             "jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}

def parse_date(raw: str) -> date | None:
    raw = raw.strip()
    # Try ISO format first
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%m-%d-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            pass
    # Try "Jan 5" or "Jan 5 2025"
    m = re.match(r"([A-Za-z]+)\s+(\d{1,2})(?:\s+(\d{4}))?", raw)
    if m:
        mon_str = m.group(1)[:3].lower()
        mon = MONTH_MAP.get(mon_str)
        if mon:
            day = int(m.group(2))
            yr  = int(m.group(3)) if m.group(3) else TODAY.year
            try:
                return date(yr, mon, day)
            except ValueError:
                pass
    return None

# ── Load transactions ─────────────────────────────────────────────────────────
transactions = []

if EXPENSES_FILE:
    if not os.path.exists(EXPENSES_FILE):
        console.print(f"[red]❌ File not found: {EXPENSES_FILE}[/red]")
        raise SystemExit(1)
    with open(EXPENSES_FILE, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        headers = [h.lower().strip() for h in (reader.fieldnames or [])]
        amt_col = next((h for h in headers if "amount" in h or "amt" in h or "cost" in h or "price" in h), None)
        date_col = next((h for h in headers if "date" in h or "day" in h), None)
        desc_col = next((h for h in headers if "desc" in h or "name" in h or "memo" in h or "narration" in h or "payee" in h), None)
        if not amt_col:
            console.print(f"[red]❌ CSV must have an 'amount' column. Found: {headers}[/red]")
            raise SystemExit(1)
        for row in reader:
            raw_keys = {k.lower().strip(): v for k, v in row.items()}
            raw_amt  = raw_keys.get(amt_col, "0")
            amt      = parse_amount(raw_amt)
            if amt is None:
                continue
            raw_desc = raw_keys.get(desc_col, "Unknown") if desc_col else "Unknown"
            raw_date = raw_keys.get(date_col, "") if date_col else ""
            txn_date = parse_date(raw_date) or TODAY
            transactions.append({"date": txn_date, "description": raw_desc.strip(), "amount": amt})

elif EXPENSES_TEXT:
    for line in EXPENSES_TEXT.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # Extract amount (last number-like token)
        tokens = line.split()
        amt = None
        for tok in reversed(tokens):
            amt = parse_amount(tok)
            if amt is not None:
                break
        if amt is None:
            continue
        # Try to extract date from beginning
        txn_date = None
        desc_start = 0
        if len(tokens) >= 2:
            date_try = parse_date(tokens[0] + " " + tokens[1])
            if date_try:
                txn_date = date_try
                desc_start = 2
            else:
                date_try = parse_date(tokens[0])
                if date_try:
                    txn_date = date_try
                    desc_start = 1
        # Description is everything between date and amount
        desc_tokens = [t for t in tokens[desc_start:] if parse_amount(t) != amt]
        description = " ".join(desc_tokens) or "Unknown"
        transactions.append({"date": txn_date or TODAY, "description": description, "amount": amt})
else:
    # Demo data so users can see the skill working
    console.print("[yellow]ℹ️  No EXPENSES_FILE or EXPENSES_TEXT set — running with demo data.[/yellow]")
    console.print("[dim]Set EXPENSES_FILE=path/to/transactions.csv or EXPENSES_TEXT='...' to use your own data.[/dim]\n")
    demo = [
        ("2025-01-05", "Starbucks coffee", 5.50),
        ("2025-01-08", "Uber ride downtown", 18.30),
        ("2025-01-10", "Netflix monthly subscription", 15.99),
        ("2025-01-12", "Grocery run Walmart", 87.45),
        ("2025-01-14", "Amazon order", 34.99),
        ("2025-01-18", "Restaurant dinner", 62.00),
        ("2025-01-20", "Gas station fuel", 55.00),
        ("2025-01-22", "Spotify premium", 9.99),
        ("2025-01-25", "Pharmacy CVS", 22.10),
        ("2025-01-28", "Gym membership", 45.00),
        ("2025-02-02", "Coffee shop", 4.80),
        ("2025-02-05", "Electric bill", 110.00),
        ("2025-02-08", "Uber eats delivery", 28.50),
        ("2025-02-12", "Whole Foods groceries", 93.20),
        ("2025-02-15", "Client payment", -500.00),
        ("2025-02-18", "Amazon Prime annual", 139.00),
        ("2025-02-20", "Doctor visit copay", 30.00),
        ("2025-02-25", "Movie tickets", 28.00),
    ]
    for d, desc, amt in demo:
        transactions.append({"date": parse_date(d) or TODAY, "description": desc, "amount": amt})

# ── Filter by month ───────────────────────────────────────────────────────────
if REPORT_MONTH:
    try:
        filter_dt = datetime.strptime(REPORT_MONTH, "%Y-%m")
        transactions = [t for t in transactions
                        if t["date"].year == filter_dt.year and t["date"].month == filter_dt.month]
        if not transactions:
            console.print(f"[yellow]⚠️  No transactions found for {REPORT_MONTH}[/yellow]")
            raise SystemExit(0)
    except ValueError:
        console.print("[red]❌ REPORT_MONTH must be YYYY-MM format (e.g. 2025-01)[/red]")
        raise SystemExit(1)

# ── Categorise all transactions ───────────────────────────────────────────────
for t in transactions:
    t["category"] = categorise(t["description"], t["amount"])

# ── Parse budget ──────────────────────────────────────────────────────────────
budget = {}
if BUDGET_RAW:
    try:
        budget = {k.title(): float(v) for k, v in json.loads(BUDGET_RAW).items()}
    except (json.JSONDecodeError, ValueError):
        console.print("[yellow]⚠️  BUDGET_JSON is not valid JSON — budget comparison skipped.[/yellow]")

# ── Aggregate: totals by category ────────────────────────────────────────────
cat_totals: dict[str, float] = defaultdict(float)
for t in transactions:
    cat_totals[t["category"]] += t["amount"]

expenses_only = {k: v for k, v in cat_totals.items() if v > 0}
total_spend = sum(expenses_only.values())
credits     = abs(cat_totals.get("Income / Credit", 0))

# ── Aggregate: monthly trends ─────────────────────────────────────────────────
monthly: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
for t in transactions:
    if t["amount"] > 0:
        mo = t["date"].strftime("%Y-%m")
        monthly[mo][t["category"]] += t["amount"]

months_sorted = sorted(monthly.keys())
all_cats = sorted(expenses_only.keys())

# ── Display header ────────────────────────────────────────────────────────────
console.print()
console.print(Panel.fit(
    f"[bold green]💰 Plutus — Expense Report[/bold green]\n"
    f"Transactions: [yellow]{len(transactions)}[/yellow]  |  "
    f"Total spend: [red]{CURRENCY} {total_spend:,.2f}[/red]  |  "
    f"Credits: [green]{CURRENCY} {credits:,.2f}[/green]",
    border_style="green"
))

# ── Display: Category totals ──────────────────────────────────────────────────
console.print()
cat_table = Table(
    title=f"Spend by Category",
    box=box.ROUNDED, border_style="green"
)
cat_table.add_column("Category",    style="cyan",   width=20)
cat_table.add_column(f"Total ({CURRENCY})", style="red", justify="right", width=14)
cat_table.add_column("% of Total",  style="yellow", justify="right", width=12)
cat_table.add_column("Budget",      style="dim",    justify="right", width=12)
cat_table.add_column("Status",      style="white",  width=12)

for cat, total in sorted(expenses_only.items(), key=lambda x: -x[1]):
    pct = (total / total_spend * 100) if total_spend else 0
    bgt = budget.get(cat, None)
    if bgt:
        status = "[green]✅ OK[/green]" if total <= bgt else f"[red]⚠ +{CURRENCY}{total-bgt:.0f}[/red]"
        bgt_str = f"{CURRENCY}{bgt:,.0f}"
    else:
        status = ""
        bgt_str = "—"
    cat_table.add_row(cat, f"{total:,.2f}", f"{pct:.1f}%", bgt_str, status)

if credits:
    cat_table.add_row("─" * 18, "─" * 10, "", "", "")
    cat_table.add_row("[green]Income / Credits[/green]", f"[green]-{credits:,.2f}[/green]", "", "", "")

console.print(cat_table)

# ── Display: Monthly trends ───────────────────────────────────────────────────
if len(months_sorted) > 1:
    console.print()
    trend_table = Table(
        title="Monthly Spend Trends",
        box=box.SIMPLE, border_style="blue"
    )
    trend_table.add_column("Month", style="cyan", width=10)
    trend_table.add_column(f"Total ({CURRENCY})", style="red", justify="right", width=12)
    for cat in all_cats[:6]:  # show top 6 categories in trends
        trend_table.add_column(cat[:12], justify="right", width=12)

    for mo in months_sorted:
        mo_total = sum(monthly[mo].values())
        row = [mo, f"{mo_total:,.2f}"]
        for cat in all_cats[:6]:
            v = monthly[mo].get(cat, 0)
            row.append(f"{v:,.2f}" if v else "—")
        trend_table.add_row(*row)
    console.print(trend_table)

# ── Display: Top transactions ─────────────────────────────────────────────────
console.print()
top_txns = sorted([t for t in transactions if t["amount"] > 0], key=lambda x: -x["amount"])[:10]
top_table = Table(title="Top 10 Transactions", box=box.ROUNDED, border_style="yellow")
top_table.add_column("Date",        style="dim",    width=12)
top_table.add_column("Description", style="white",  width=30)
top_table.add_column("Category",    style="cyan",   width=20)
top_table.add_column(f"Amount ({CURRENCY})", style="red", justify="right", width=12)

for t in top_txns:
    top_table.add_row(
        t["date"].strftime("%b %d, %Y"),
        t["description"][:28],
        t["category"],
        f"{t['amount']:,.2f}"
    )
console.print(top_table)

# ── Save outputs ──────────────────────────────────────────────────────────────
slug  = TODAY.strftime("%Y-%m")
if REPORT_MONTH:
    slug = REPORT_MONTH
md_path  = f"expense_report_{slug}.md"
csv_path = f"expense_summary_{slug}.csv"

with open(md_path, "w", encoding="utf-8") as f:
    f.write(f"# 💰 Expense Report — {slug}\n\n")
    f.write(f"**Total spend:** {CURRENCY} {total_spend:,.2f}  ")
    if credits:
        f.write(f"**Credits:** {CURRENCY} {credits:,.2f}  ")
    f.write(f"**Transactions:** {len(transactions)}\n\n")
    f.write("## By Category\n\n| Category | Amount | % |\n|----------|--------|---|\n")
    for cat, total in sorted(expenses_only.items(), key=lambda x: -x[1]):
        pct = (total / total_spend * 100) if total_spend else 0
        f.write(f"| {cat} | {CURRENCY} {total:,.2f} | {pct:.1f}% |\n")
    f.write("\n## All Transactions\n\n| Date | Description | Category | Amount |\n|------|-------------|----------|--------|\n")
    for t in sorted(transactions, key=lambda x: x["date"]):
        sign = "-" if t["amount"] < 0 else ""
        f.write(f"| {t['date'].strftime('%b %d')} | {t['description']} | {t['category']} | {sign}{CURRENCY}{abs(t['amount']):,.2f} |\n")

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["category", f"total_{CURRENCY.lower()}", "pct_of_spend"])
    for cat, total in sorted(expenses_only.items(), key=lambda x: -x[1]):
        pct = (total / total_spend * 100) if total_spend else 0
        writer.writerow([cat, f"{total:.2f}", f"{pct:.1f}"])

console.print()
console.print(Panel(
    f"[green]✅ Report complete![/green]\n\n"
    f"📝 [cyan]{md_path}[/cyan] — full markdown report\n"
    f"📊 [cyan]{csv_path}[/cyan] — category summary CSV\n\n"
    f"[dim]Set EXPENSES_FILE or EXPENSES_TEXT to analyse your own transactions.[/dim]",
    title="[bold]📤 Exports[/bold]",
    border_style="green"
))
```
