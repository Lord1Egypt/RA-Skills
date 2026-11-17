# Expense Tracker and Budgets input contract

add: kind expense|income|refund, date, amount (decimal string, max 2 places), currency (3 uppercase letters), category, optional description. void: id, reason. budget: month YYYY-MM, amount, currency, category. list/summary: from and to inclusive dates. Amounts in outputs are minor units (100 = 1 major unit). Mutations require requestId.

## Added in 1.1.0

New: import-csv {file} uses kind,date,amount,currency,category,description?,sourceId? headers; export {from,to} writes ledger.csv and budget-report.md. Amounts are positive two-decimal values; refunds use kind refund. Import is batch-atomic and repeated identical file/IDs are counted; changed values under an existing sourceId raise a conflict. Writes/exports require requestId.

## Output files

ledger.csv / budget-report.md

Exports create a new unique directory and return files [{path,bytes,sha256}]. Repeating the same requestId returns the same files; altered or missing saved exports raise an error. CSV output quotes fields and neutralizes spreadsheet formula prefixes. Keep other operations' active lock files in place. All files and records are scoped to the supplied active workspace.

Supported currencies: CNY, USD, EUR, GBP, HKD, SGD, AUD, CAD, CHF, NZD; two decimal places. Budget spend values cover the whole month.
