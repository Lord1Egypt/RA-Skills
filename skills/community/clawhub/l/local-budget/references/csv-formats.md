# CSV Format Reference

Documentation of supported bank CSV formats and how to add new ones.

## Supported Formats

### Chase (credit cards & checking)

Auto-detected when headers include both `Transaction Date` and `Post Date`.

**Headers:** `Transaction Date, Post Date, Description, Category, Type, Amount, Memo`

**Key details:**
- Amounts: negative = debit (spending), positive = credit (payment/refund)
  - Note: `parse_csv.py` normalizes all amounts to positive; type is stored in the `type` field
- Date format: `MM/DD/YYYY`
- Category column present (Chase's own categories)
- `Type` column: `Sale`, `Payment`, `Return`, `Adjustment`

**Example rows:**
```
Transaction Date,Post Date,Description,Category,Type,Amount,Memo
01/15/2024,01/16/2024,WHOLE FOODS #365,Groceries,Sale,-87.42,
01/18/2024,01/19/2024,STARBUCKS #12345,Food & Drink,Sale,-6.75,
01/20/2024,01/21/2024,AUTOPAY PAYMENT,,Payment,500.00,
```

**Export path:** Chase.com → Accounts → Download → CSV

---

### Bank of America (checking & credit)

Auto-detected when headers include `Date` + `Running Bal.` (checking) or `Posted Date` + `Reference Number` (credit).

**Checking headers:** `Date, Description, Amount, Running Bal.`

**Credit card headers:** `Posted Date, Reference Number, Payee, Address, Amount`

**Key details:**
- Checking: negative = withdrawal (debit), positive = deposit (credit)
- Credit: negative = charge (debit), positive = payment (credit)
- Date format: `MM/DD/YYYY`
- No category column in most BoA exports

**Example rows (checking):**
```
Date,Description,Amount,Running Bal.
01/15/2024,WHOLE FOODS MARKET,-87.42,1234.56
01/16/2024,DIRECT DEPOSIT EMPLOYER,2500.00,3734.56
```

**Export path:** BofA Online Banking → Accounts → Download → CSV

---

### Generic (fallback)

Used when auto-detection fails or for any other bank.

**Column detection (tries in order):**
- Date: `Date`, `Transaction Date`, `Posted Date`, `Posting Date`
- Description: `Description`, `Merchant`, `Name`, `Payee`, `Transaction Description`
- Amount: `Amount`, `Debit`, `Credit`, `Transaction Amount`
- Category: `Category`, `Type` (optional)

Also handles split debit/credit columns (some banks use separate `Debit` and `Credit` columns with one left blank).

---

## Adding a New Bank Format

### Option 1: Use `--format generic`

Most banks work with `generic` format. Try it first:
```bash
python3 parse_csv.py mybank_export.csv --format generic --output tx.json
```

Check stderr output for warnings about undetected columns.

### Option 2: Add a Named Format

Edit `parse_csv.py` and add an entry to the `FORMATS` dict:

```python
"mybank": {
    "date": "Transaction Date",          # exact column header name
    "description": "Description",
    "amount": "Amount",
    "category": "Category",              # None if no category column
    "amount_sign": "native",             # "native" = positive is debit
},
```

Then add a detection rule in `detect_format()`:

```python
# MyBank: has "Account Number" and "Transaction ID"
if "account number" in headers_set and "transaction id" in headers_set:
    return "mybank"
```

### Option 3: Split Debit/Credit Columns

Some banks (Ally, Discover) use separate Debit and Credit columns:

```
Date,Description,Debit,Credit
01/15/2024,WHOLE FOODS,87.42,
01/20/2024,DIRECT DEPOSIT,,2500.00
```

`parse_csv.py` auto-detects this pattern when `Debit` and `Credit` headers are present without an `Amount` column. No changes needed.

---

## Date Format Handling

Supported date formats (auto-tried in order):
- `MM/DD/YYYY` — Most US banks (Chase, BoA, Citi)
- `YYYY-MM-DD` — ISO format (some exports)
- `MM/DD/YY` — Short year format
- `MM-DD-YYYY` — Hyphen-separated
- `YYYY/MM/DD` — ISO with slashes
- `DD/MM/YYYY` — European format (non-US banks)

If a date fails to parse, it's kept as-is and logged to stderr. Unparseable dates won't break the pipeline but may appear in "unknown" month in the report.

---

## Common Issues

**"Could not find date column"**  
→ Print the first few rows: `head -3 export.csv`. Check for leading/trailing spaces in header names. Some banks add BOM characters (handled by `encoding="utf-8-sig"`).

**"Skipped N rows"**  
→ Normal for banks that add summary/balance rows at the top or bottom. Check the count matches expectations.

**Wrong amounts (all zeros or massive numbers)**  
→ Check if amounts include currency symbols or commas. `parse_csv.py` strips `$` and `,` automatically.

**All transactions showing as debits**  
→ Check if your bank uses negative numbers for debits or for credits. Some banks invert the convention. If needed, flip logic by editing the `tx_type` detection in `parse_csv.py`.

---

## Tested Banks

| Bank | Format | Notes |
|---|---|---|
| Chase (credit) | `chase` | Full support incl. categories |
| Chase (checking) | `chase` | Works, categories may be blank |
| Bank of America (checking) | `boa` | Full support |
| Bank of America (credit) | `boa` | Full support |
| Citi | `generic` | Works well |
| Wells Fargo | `generic` | Works well |
| Ally Bank | `generic` | Split debit/credit auto-detected |
| Capital One | `generic` | Works with standard export |
| Discover | `generic` | Split columns auto-detected |
| American Express | `generic` | Works well |
