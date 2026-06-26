---
name: plutus-lite
description: "Plutus Lite — Expense Tracker (Free). Categorise up to 15 transactions and see a basic spend breakdown. A free preview of what Plutus Pro does for your full financial picture."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: []
      bins: [python3, pip3]
    primaryEnv: "EXPENSES_TEXT"
    homepage: https://clawhub.ai/occupythemilkyway/plutus-lite
    emoji: "💰"
    tags: [finance, expenses, budget, tracker, plutus, free, lite]
    envVars:
      - name: EXPENSES_TEXT
        required: false
        description: "Paste up to 15 expenses, one per line: 'Jan 5 Coffee 4.50' or 'Amazon 34.99'"
        default: ""
      - name: CURRENCY
        required: false
        description: "Currency: USD, EUR, GBP"
        default: "USD"
---

# Plutus Lite — Free Expense Preview

Paste up to 15 expenses and get a quick category breakdown.

## Free vs Pro

| Feature | Plutus Lite (Free) | Plutus Pro |
|---------|-------------------|-----------|
| Transactions | **15 max** | Unlimited |
| CSV file input | ❌ | ✅ |
| Budget comparison | ❌ | ✅ |
| Monthly trends | ❌ | ✅ |
| Tax deduction tracking | ❌ | ✅ |
| Savings rate analysis | ❌ | ✅ |
| Spending forecast | ❌ | ✅ 1-12 months |
| Export (CSV + JSON) | ❌ | ✅ |

👉 **Upgrade:** `openclaw skills install plutus-pro` — key at **ko-fi.com/s/83c662001e**

💰 **Bundle deal:** all 5 Pro skills for **$29** → **ko-fi.com/s/7625accf3f** (save $16)

---

## Step 1 — Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 — Quick expense scan (Lite)

```python
import os, re
from datetime import date
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

EXPENSES_TEXT = os.environ.get("EXPENSES_TEXT","").strip()
CURRENCY      = os.environ.get("CURRENCY","USD").upper()
SYM           = {"USD":"$","EUR":"€","GBP":"£"}.get(CURRENCY,"$")
TODAY         = date.today()
TX_LIMIT      = 15

def fmt(a): return f"{SYM}{a:,.2f}"

def parse_amount(raw):
    c = re.sub(r"[^0-9.]","",str(raw)) or "0"
    try: return float(c) if c.count(".")<=1 else None
    except: return None

CATEGORIES = {
    "Food & Dining":  ["coffee","starbucks","restaurant","pizza","burger","cafe","food","doordash","grubhub","grocery","walmart","whole foods"],
    "Transport":      ["uber","lyft","taxi","gas","fuel","parking","transit","bus","train","flight"],
    "Shopping":       ["amazon","ebay","etsy","target","bestbuy","clothing","shoes"],
    "Subscriptions":  ["netflix","spotify","hulu","disney","prime","subscription","membership","software"],
    "Utilities":      ["electric","water","internet","phone","mobile","utility","bill"],
    "Health":         ["pharmacy","doctor","dentist","medical","gym","fitness","cvs","walgreens"],
    "Entertainment":  ["movie","cinema","concert","ticket","game","gaming","book"],
    "Other":          [],
}

def categorise(desc):
    dl = desc.lower()
    for cat, kws in CATEGORIES.items():
        if cat == "Other": continue
        if any(k in dl for k in kws): return cat
    return "Other"

transactions = []

if EXPENSES_TEXT:
    for line in EXPENSES_TEXT.strip().splitlines():
        if len(transactions) >= TX_LIMIT:
            console.print(f"[yellow]⚠️  Lite limit: showing first {TX_LIMIT} transactions. Upgrade to Pro for unlimited.[/yellow]")
            break
        line = line.strip()
        if not line: continue
        tokens = line.split()
        amt = None
        for tok in reversed(tokens):
            a = parse_amount(tok)
            if a is not None: amt = a; break
        if amt is None: continue
        desc_tokens = tokens[:-1] if tokens[-1] == str(amt) else [t for t in tokens if parse_amount(t) != amt]
        # Strip leading date tokens (simple heuristic)
        if len(desc_tokens) >= 2:
            try:
                int(desc_tokens[0]); desc_tokens = desc_tokens[1:]
            except ValueError:
                pass
        description = " ".join(desc_tokens) or "Expense"
        transactions.append({"description": description, "amount": amt, "category": categorise(description)})
else:
    # Demo data
    console.print("[yellow]ℹ️  No EXPENSES_TEXT set — running with demo data.[/yellow]")
    console.print("[dim]Set EXPENSES_TEXT='Coffee 4.50\\nAmazon 34.99\\nUber 18.30' to use your own.\n[/dim]")
    demo = [
        ("Starbucks coffee",5.50),("Uber ride",18.30),("Netflix",15.99),
        ("Groceries Walmart",87.45),("Amazon order",34.99),("Restaurant dinner",62.00),
        ("Gas station",55.00),("Spotify premium",9.99),("CVS pharmacy",22.10),("Gym membership",45.00),
    ]
    for desc,amt in demo:
        transactions.append({"description":desc,"amount":amt,"category":categorise(desc)})

if not transactions:
    console.print("[yellow]No transactions found.[/yellow]")
    raise SystemExit(0)

total_spend = sum(t["amount"] for t in transactions)

console.print()
console.print(Panel.fit(
    f"[bold green]💰 Plutus Lite — Expense Snapshot[/bold green]\n"
    f"Transactions: [yellow]{len(transactions)}/{TX_LIMIT}[/yellow]  Total: [red]{fmt(total_spend)}[/red]\n"
    f"[dim]Lite: {TX_LIMIT} transactions max — upgrade to Pro for unlimited + full analytics[/dim]",
    border_style="green"
))

# Category totals
cat_totals = defaultdict(float)
for t in transactions: cat_totals[t["category"]] += t["amount"]

console.print()
tbl = Table(title="Spend by Category", box=box.ROUNDED, border_style="green")
tbl.add_column("Category", width=20, style="cyan")
tbl.add_column(f"Total ({CURRENCY})", width=14, justify="right", style="red")
tbl.add_column("% of spend", width=12, justify="right", style="yellow")

for cat,total in sorted(cat_totals.items(),key=lambda x:-x[1]):
    pct = total/total_spend*100 if total_spend else 0
    tbl.add_row(cat, fmt(total), f"{pct:.1f}%")
console.print(tbl)

# Transaction list
console.print()
tx_tbl = Table(title="Transactions", box=box.SIMPLE, border_style="dim")
tx_tbl.add_column("#",           width=4,  style="dim")
tx_tbl.add_column("Description", width=28, style="white")
tx_tbl.add_column("Category",    width=18, style="cyan")
tx_tbl.add_column("Amount",      width=12, justify="right", style="red")
for i,t in enumerate(transactions,1):
    tx_tbl.add_row(str(i), t["description"][:26], t["category"], fmt(t["amount"]))
console.print(tx_tbl)

console.print()
console.print(Panel(
    f"[bold yellow]🔓 Want your full financial picture?[/bold yellow]\n\n"
    f"Plutus Pro handles [bold]unlimited transactions[/bold] from any bank CSV, tracks "
    f"[bold]tax-deductible expenses[/bold], shows [bold]monthly trends[/bold], "
    f"calculates your [bold]savings rate[/bold], and forecasts spending up to 12 months ahead.\n\n"
    f"[bold cyan]openclaw skills install plutus-pro[/bold cyan]\n"
    f"Get your key → [bold]ko-fi.com/s/83c662001e[/bold]",
    title="Upgrade to Plutus Pro",
    border_style="cyan"
))
```
