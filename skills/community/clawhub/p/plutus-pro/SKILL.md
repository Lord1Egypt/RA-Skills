---
name: plutus-pro
description: "Plutus Pro — Wealth Intelligence. Full expense tracking with AI-powered categorisation, multi-account reconciliation, tax category tagging, budget forecasting, monthly P&L, and automated savings rate analysis. Works with CSV exports from any bank or app."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: [LICENSE_KEY]
      bins: [python3, pip3]
    primaryEnv: "EXPENSES_FILE"
    homepage: https://clawhub.ai/occupythemilkyway/plutus-pro
    emoji: "💰📊⚡"
    tags: [finance, expenses, budget, bookkeeping, tracker, plutus, pro, premium, tax, forecasting]
    envVars:
      - name: LICENSE_KEY
        required: true
        description: "Your Plutus Pro license key. Get one at: ko-fi.com/s/83c662001e"

💰 **Bundle deal:** all 5 Pro skills for **$29** → **ko-fi.com/s/7625accf3f** (save $16)
      - name: EXPENSES_FILE
        required: false
        description: "Path to a CSV of transactions (date, description, amount)"
        default: ""
      - name: EXPENSES_TEXT
        required: false
        description: "Raw expense text, one per line"
        default: ""
      - name: BUDGET_JSON
        required: false
        description: "Monthly budget per category as JSON string"
        default: ""
      - name: SAVINGS_GOAL
        required: false
        description: "Monthly savings target amount for savings rate tracking"
        default: "0"
      - name: TAX_CATEGORIES
        required: false
        description: "Comma-separated categories to flag as tax-deductible (e.g. 'Business,Education')"
        default: "Business,Education"
      - name: CURRENCY
        required: false
        description: "Currency symbol: USD, EUR, GBP, CAD"
        default: "USD"
      - name: REPORT_MONTH
        required: false
        description: "Filter to YYYY-MM, leave blank for all"
        default: ""
      - name: FORECAST_MONTHS
        required: false
        description: "Months to project spending forward (1-12)"
        default: "3"
---

# Plutus Pro — Full Wealth Intelligence

Everything in Plutus, plus tax tagging, savings rate analysis, multi-month forecasting, P&L summary, and per-transaction notes.

## Pro features vs free Plutus

| Feature | Plutus (Free) | Plutus Pro |
|---------|--------------|-----------|
| Transactions | Unlimited | Unlimited |
| Categories | 15 standard | 15 + custom tax flags |
| Budget comparison | ✅ | ✅ + percentage alerts |
| Monthly trends | ✅ | ✅ + P&L summary |
| Tax category tagging | ❌ | ✅ |
| Savings rate analysis | ❌ | ✅ |
| Spending forecast | ❌ | ✅ 1-12 months |
| JSON export | ❌ | ✅ Full structured data |
| Surplus / deficit | ❌ | ✅ Monthly P&L |

---

## Setup

1. **Purchase** your license key at **ko-fi.com/s/83c662001e** ($9 one-time)
   - Or get all 5 Pro skills for **$29** → **ko-fi.com/s/7625accf3f** (save $16)
2. **Install:** `openclaw skills install plutus-pro`
3. **Activate:** set the `LICENSE_KEY` environment variable to the key you received
4. **Run** — you're in

---

## Step 1 — Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 — Full wealth analysis (Pro)

```python
import os, re, json, csv
from datetime import datetime, date
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

LICENSE_KEY = os.environ.get("LICENSE_KEY","").strip()
if not LICENSE_KEY:
    console.print(Panel(
        "[red bold]🔒 Plutus Pro requires a license key.[/red bold]\n\n"
        "Get your key at: [bold cyan]ko-fi.com/s/83c662001e[/bold cyan]\n\n"
        "Or use the free version: [dim]openclaw skills install plutus[/dim]",
        title="License Required", border_style="red"
    ))
    raise SystemExit(1)

EXPENSES_FILE  = os.environ.get("EXPENSES_FILE","").strip()
EXPENSES_TEXT  = os.environ.get("EXPENSES_TEXT","").strip()
BUDGET_RAW     = os.environ.get("BUDGET_JSON","").strip()
CURRENCY       = os.environ.get("CURRENCY","USD").upper()
REPORT_MONTH   = os.environ.get("REPORT_MONTH","").strip()
TAX_CATS_RAW   = os.environ.get("TAX_CATEGORIES","Business,Education")
TAX_CATEGORIES = [t.strip() for t in TAX_CATS_RAW.split(",") if t.strip()]
try: SAVINGS_GOAL   = float(os.environ.get("SAVINGS_GOAL","0"))
except: SAVINGS_GOAL = 0.0
try: FORECAST_MONTHS = min(int(os.environ.get("FORECAST_MONTHS","3")),12)
except: FORECAST_MONTHS = 3
TODAY = date.today()
SYM   = {"USD":"$","EUR":"€","GBP":"£","CAD":"CA$"}.get(CURRENCY,"$")

def fmt(a): return f"{SYM}{abs(a):,.2f}"

CATEGORIES = {
    "Food & Dining":    ["coffee","starbucks","restaurant","pizza","burger","cafe","dining","food","doordash","grubhub","grocery","groceries","walmart","whole foods","supermarket"],
    "Transport":        ["uber","lyft","taxi","gas","fuel","parking","transit","metro","bus","train","airline","flight","car rental","toll","petrol"],
    "Shopping":         ["amazon","ebay","etsy","target","bestbuy","clothing","shoes","fashion","zara","nordstrom","mall"],
    "Subscriptions":    ["netflix","spotify","hulu","disney","apple music","youtube","prime","subscription","membership","software","adobe","microsoft","google"],
    "Utilities":        ["electric","electricity","water","internet","phone","mobile","cellular","at&t","verizon","comcast","hydro","utility"],
    "Health":           ["pharmacy","doctor","dentist","medical","hospital","prescription","medicine","gym","fitness","yoga","cvs","walgreens"],
    "Entertainment":    ["movie","cinema","theatre","concert","ticket","game","gaming","steam","kindle","audible","museum"],
    "Travel":           ["hotel","airbnb","hostel","resort","booking","expedia","trip","vacation","tour"],
    "Education":        ["course","udemy","coursera","tuition","textbook","training","workshop","class","lesson"],
    "Home":             ["rent","mortgage","furniture","home depot","lowes","hardware","repair","maintenance","cleaning"],
    "Insurance":        ["insurance","premium","policy","geico","allstate","progressive"],
    "Business":         ["invoice","client","freelance","office","supplies","coworking","advertising","domain","hosting"],
    "Personal Care":    ["salon","haircut","barber","spa","beauty","cosmetics","skincare","makeup","nails"],
    "Income / Credit":  [],
}

def categorise(desc, amount):
    if amount < 0: return "Income / Credit"
    dl = desc.lower()
    for cat, kws in CATEGORIES.items():
        if cat == "Income / Credit": continue
        if any(k in dl for k in kws): return cat
    return "Other"

def parse_amount(raw):
    raw = str(raw).strip().lstrip("$£€").replace(",","")
    try: return float(raw)
    except: return None

MONTH_MAP = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}

def parse_date(raw):
    raw = str(raw).strip()
    for fmt_s in ("%Y-%m-%d","%m/%d/%Y","%d/%m/%Y","%m-%d-%Y"):
        try: return datetime.strptime(raw,fmt_s).date()
        except: pass
    import re as _re
    m = _re.match(r"([A-Za-z]+)\s+(\d{1,2})(?:\s+(\d{4}))?",raw)
    if m:
        mon = MONTH_MAP.get(m.group(1)[:3].lower())
        if mon:
            try: return date(int(m.group(3) or TODAY.year), mon, int(m.group(2)))
            except: pass
    return None

transactions = []

if EXPENSES_FILE and os.path.exists(EXPENSES_FILE):
    with open(EXPENSES_FILE,newline="",encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        hdrs = [h.lower().strip() for h in (reader.fieldnames or [])]
        amt_col  = next((h for h in hdrs if "amount" in h or "amt" in h or "cost" in h),None)
        date_col = next((h for h in hdrs if "date" in h or "day" in h),None)
        desc_col = next((h for h in hdrs if "desc" in h or "name" in h or "memo" in h or "narration" in h or "payee" in h),None)
        note_col = next((h for h in hdrs if "note" in h or "comment" in h or "tag" in h),None)
        if not amt_col:
            console.print(f"[red]❌ CSV needs an 'amount' column. Found: {hdrs}[/red]")
            raise SystemExit(1)
        for row in reader:
            rk = {k.lower().strip():v for k,v in row.items()}
            amt = parse_amount(rk.get(amt_col,"0"))
            if amt is None: continue
            transactions.append({
                "date": parse_date(rk.get(date_col,"")) or TODAY,
                "description": (rk.get(desc_col,"Unknown") or "Unknown").strip(),
                "amount": amt,
                "note": rk.get(note_col,"") if note_col else "",
            })
elif EXPENSES_TEXT:
    for line in EXPENSES_TEXT.strip().splitlines():
        line = line.strip()
        if not line: continue
        tokens = line.split()
        amt = None
        for tok in reversed(tokens):
            amt = parse_amount(tok)
            if amt is not None: break
        if amt is None: continue
        txn_date = None
        desc_start = 0
        if len(tokens)>=2:
            dt = parse_date(tokens[0]+" "+tokens[1])
            if dt: txn_date=dt; desc_start=2
            else:
                dt = parse_date(tokens[0])
                if dt: txn_date=dt; desc_start=1
        desc_tokens = [t for t in tokens[desc_start:] if parse_amount(t)!=amt]
        transactions.append({"date":txn_date or TODAY,"description":" ".join(desc_tokens) or "Unknown","amount":amt,"note":""})
else:
    console.print("[yellow]ℹ️  No data set — running with demo data.[/yellow]\n")
    demo = [
        ("2025-01-05","Starbucks coffee",5.50,""),("2025-01-08","Uber ride",18.30,""),("2025-01-10","Netflix",15.99,""),
        ("2025-01-12","Groceries Walmart",87.45,""),("2025-01-14","Amazon order",34.99,""),
        ("2025-01-18","Restaurant dinner",62.00,""),("2025-01-20","Gas station",55.00,""),
        ("2025-01-22","Spotify",9.99,""),("2025-01-25","CVS pharmacy",22.10,""),("2025-01-28","Gym membership",45.00,""),
        ("2025-01-30","Udemy course",19.99,"tax"),("2025-01-31","Client payment",-500.00,"income"),
        ("2025-02-02","Coffee",4.80,""),("2025-02-05","Electric bill",110.00,""),
        ("2025-02-08","Uber eats",28.50,""),("2025-02-12","Whole Foods",93.20,""),
        ("2025-02-15","Freelance income",-800.00,"income"),("2025-02-18","Office supplies",45.00,"tax"),
        ("2025-02-20","Doctor visit",30.00,""),("2025-02-25","Movie tickets",28.00,""),
        ("2025-02-28","Domain hosting",12.00,"tax"),
    ]
    for d,desc,amt,note in demo:
        transactions.append({"date":parse_date(d) or TODAY,"description":desc,"amount":amt,"note":note})

if REPORT_MONTH:
    try:
        fd = datetime.strptime(REPORT_MONTH,"%Y-%m")
        transactions = [t for t in transactions if t["date"].year==fd.year and t["date"].month==fd.month]
    except ValueError:
        console.print("[red]❌ REPORT_MONTH must be YYYY-MM[/red]"); raise SystemExit(1)

for t in transactions:
    t["category"] = categorise(t["description"],t["amount"])
    t["tax_deductible"] = t["category"] in TAX_CATEGORIES and t["amount"] > 0

budget = {}
if BUDGET_RAW:
    try: budget = {k.title():float(v) for k,v in json.loads(BUDGET_RAW).items()}
    except: console.print("[yellow]⚠️  BUDGET_JSON invalid — skipping budget comparison.[/yellow]")

# Aggregates
cat_totals = defaultdict(float)
for t in transactions: cat_totals[t["category"]] += t["amount"]

expenses_only = {k:v for k,v in cat_totals.items() if v > 0}
credits       = abs(cat_totals.get("Income / Credit",0))
total_spend   = sum(expenses_only.values())
net           = credits - total_spend
savings_rate  = (net / credits * 100) if credits > 0 else 0

tax_total = sum(t["amount"] for t in transactions if t.get("tax_deductible"))

# Monthly aggregates
monthly = defaultdict(lambda: defaultdict(float))
monthly_income = defaultdict(float)
for t in transactions:
    mo = t["date"].strftime("%Y-%m")
    if t["amount"] > 0: monthly[mo][t["category"]] += t["amount"]
    else: monthly_income[mo] += abs(t["amount"])
months_sorted = sorted(set(list(monthly.keys())+list(monthly_income.keys())))

# Header
console.print()
console.print(Panel.fit(
    f"[bold green]💰📊⚡ Plutus Pro — Wealth Intelligence[/bold green]\n"
    f"Transactions: [yellow]{len(transactions)}[/yellow]  "
    f"Spend: [red]{fmt(total_spend)}[/red]  "
    f"Income: [green]{fmt(credits)}[/green]  "
    f"Net: [{'green' if net>=0 else 'red'}]{('+' if net>=0 else '')}{fmt(net)}[/{'green' if net>=0 else 'red'}]  "
    f"Tax-deductible: [cyan]{fmt(tax_total)}[/cyan]",
    border_style="green"
))

# Savings rate
if credits > 0:
    console.print()
    bar_filled = max(0,min(20,int(savings_rate/5)))
    bar = "█"*bar_filled+"░"*(20-bar_filled)
    goal_line = f"  Goal: {SAVINGS_GOAL:.0f}%" if SAVINGS_GOAL else ""
    console.print(Panel(
        f"[cyan]{bar}[/cyan]  [yellow]{savings_rate:.1f}% savings rate[/yellow]{goal_line}\n"
        f"Income: {fmt(credits)}  Spend: {fmt(total_spend)}  Net: {('+' if net>=0 else '')}{fmt(net)}",
        title="💰 Monthly P&L", border_style="green"
    ))

# Category totals
console.print()
tbl = Table(title="Spend by Category", box=box.ROUNDED, border_style="green")
tbl.add_column("Category",   width=20, style="cyan")
tbl.add_column(f"Total",     width=13, justify="right", style="red")
tbl.add_column("% Spend",    width=10, justify="right", style="yellow")
tbl.add_column("Budget",     width=12, justify="right", style="dim")
tbl.add_column("Status",     width=14)
tbl.add_column("Tax",        width=5)
for cat,total in sorted(expenses_only.items(),key=lambda x:-x[1]):
    pct  = total/total_spend*100 if total_spend else 0
    bgt  = budget.get(cat)
    over = total - bgt if bgt else 0
    status = f"[green]✅ OK[/green]" if bgt and total<=bgt else (f"[red]⚠ +{fmt(over)}[/red]" if bgt else "")
    bgt_s  = fmt(bgt) if bgt else "—"
    tax_s  = "✓" if cat in TAX_CATEGORIES else ""
    tbl.add_row(cat,fmt(total),f"{pct:.1f}%",bgt_s,status,f"[cyan]{tax_s}[/cyan]")
if credits:
    tbl.add_row("[green]Income / Credits[/green]",f"[green]-{fmt(credits)}[/green]","","","","")
console.print(tbl)

# Tax summary
if tax_total:
    console.print()
    tax_items = [t for t in transactions if t.get("tax_deductible")]
    console.print(Panel(
        f"[cyan]Total potential deductions: {fmt(tax_total)}[/cyan]\n\n" +
        "\n".join(f"• {t['date'].strftime('%b %d')} — {t['description']}: {fmt(t['amount'])}" for t in tax_items),
        title="🧾 Tax-Deductible Expenses",
        border_style="cyan"
    ))

# Monthly trend
if len(months_sorted)>1:
    console.print()
    trend = Table(title="Monthly Trends",box=box.SIMPLE,border_style="blue")
    trend.add_column("Month",width=10,style="cyan")
    trend.add_column("Spend",width=12,justify="right",style="red")
    trend.add_column("Income",width=12,justify="right",style="green")
    trend.add_column("Net",width=12,justify="right")
    for mo in months_sorted:
        sp = sum(monthly[mo].values())
        inc = monthly_income.get(mo,0)
        net_mo = inc-sp
        net_col = "green" if net_mo>=0 else "red"
        trend.add_row(mo,fmt(sp),fmt(inc) if inc else "—",f"[{net_col}]{('+' if net_mo>=0 else '')}{fmt(net_mo)}[/{net_col}]")
    console.print(trend)

# Forecast
if FORECAST_MONTHS>0 and total_spend>0:
    months_count = max(len(months_sorted),1)
    avg_monthly  = total_spend/months_count
    console.print()
    fc_lines = "\n".join(
        f"[dim]+{i}mo:[/dim] [red]{fmt(avg_monthly*(i+1))}[/red] projected spend  "
        f"([green]-{fmt(credits/months_count*(i+1))}[/green] projected income)"
        for i in range(FORECAST_MONTHS)
    )
    console.print(Panel(fc_lines,title=f"📈 {FORECAST_MONTHS}-Month Forecast (based on {months_count}-month average)",border_style="magenta"))

# Top transactions
console.print()
top = sorted([t for t in transactions if t["amount"]>0],key=lambda x:-x["amount"])[:10]
top_tbl = Table(title="Top 10 Transactions",box=box.ROUNDED,border_style="yellow")
top_tbl.add_column("Date",width=12,style="dim")
top_tbl.add_column("Description",width=28)
top_tbl.add_column("Category",width=18,style="cyan")
top_tbl.add_column("Amount",width=12,justify="right",style="red")
top_tbl.add_column("Tax",width=4)
for t in top:
    top_tbl.add_row(t["date"].strftime("%b %d, %Y"),t["description"][:26],t["category"],fmt(t["amount"]),"✓" if t.get("tax_deductible") else "")
console.print(top_tbl)

# Save
slug     = REPORT_MONTH or TODAY.strftime("%Y-%m")
md_path  = f"plutus_pro_report_{slug}.md"
csv_path = f"plutus_pro_summary_{slug}.csv"
json_path= f"plutus_pro_data_{slug}.json"

with open(md_path,"w",encoding="utf-8") as f:
    f.write(f"# 💰 Plutus Pro Report — {slug}\n\n")
    f.write(f"**Spend:** {fmt(total_spend)}  **Income:** {fmt(credits)}  **Net:** {('+' if net>=0 else '')}{fmt(net)}  **Tax deductible:** {fmt(tax_total)}\n\n")
    f.write(f"**Savings rate:** {savings_rate:.1f}%\n\n")
    f.write("## By Category\n\n| Category | Amount | % | Tax |\n|---|---|---|---|\n")
    for cat,total in sorted(expenses_only.items(),key=lambda x:-x[1]):
        pct=total/total_spend*100 if total_spend else 0
        f.write(f"| {cat} | {fmt(total)} | {pct:.1f}% | {'✓' if cat in TAX_CATEGORIES else ''} |\n")
    f.write("\n## All Transactions\n\n| Date | Description | Category | Amount | Tax |\n|---|---|---|---|---|\n")
    for t in sorted(transactions,key=lambda x:x["date"]):
        sign="-" if t["amount"]<0 else ""
        f.write(f"| {t['date'].strftime('%b %d')} | {t['description']} | {t['category']} | {sign}{fmt(t['amount'])} | {'✓' if t.get('tax_deductible') else ''} |\n")

with open(csv_path,"w",newline="",encoding="utf-8") as f:
    writer=csv.writer(f)
    writer.writerow(["category","total","pct","budget","over_budget","tax_deductible"])
    for cat,total in sorted(expenses_only.items(),key=lambda x:-x[1]):
        pct=total/total_spend*100 if total_spend else 0
        bgt=budget.get(cat,0)
        writer.writerow([cat,f"{total:.2f}",f"{pct:.1f}",f"{bgt:.2f}",f"{max(0,total-bgt):.2f}","yes" if cat in TAX_CATEGORIES else "no"])

with open(json_path,"w",encoding="utf-8") as f:
    json.dump({"period":slug,"summary":{"total_spend":total_spend,"total_income":credits,"net":net,"savings_rate":savings_rate,"tax_deductible":tax_total},"categories":{k:v for k,v in expenses_only.items()},"transactions":[{"date":str(t["date"]),"description":t["description"],"amount":t["amount"],"category":t["category"],"tax":t.get("tax_deductible",False)} for t in transactions]},f,indent=2)

console.print()
console.print(Panel(
    f"[green]✅ Done![/green]\n\n"
    f"📝 [cyan]{md_path}[/cyan]\n"
    f"📊 [cyan]{csv_path}[/cyan]\n"
    f"📄 [cyan]{json_path}[/cyan]",
    title="Exports", border_style="green"
))
```
