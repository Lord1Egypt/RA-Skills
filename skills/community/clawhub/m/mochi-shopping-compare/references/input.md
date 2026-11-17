# Shopping Comparison input contract

compare: asOf YYYY-MM-DD, criteria [], items [{name,url,observedOn,currency,evidence, optional price,shipping,discount,quantity,specs}]. Decimal strings have up to two places. Shipping omitted means unknown, not free. Costs rank separately by currency; each result includes quantity and unitTotalMinor. show: id. Compare requires requestId.

## Added in 1.1.0

New: changes {fromId,toId} matches exact URL/currency/quantity across stored comparisons; export {id} writes Markdown and CSV. Changed pack sizes and incomplete prices are flagged. Original referral URLs are retained. Exports require requestId. No scraping, purchase or background watch is performed.

## Output files

comparison.md / comparison.csv

Exports create a new unique directory and return files [{path,bytes,sha256}]. Repeating the same requestId returns the same files; altered or missing saved exports raise an error. CSV output quotes fields and neutralizes spreadsheet formula prefixes. Keep other operations' active lock files in place. All files and records are scoped to the supplied active workspace.
