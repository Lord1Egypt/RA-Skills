# US inventory, tax and shipping rules

Reference for the Inventory Tracker skill. Every limit and rule below is a US-facing constraint the workflow has to respect.

## Inventory accounting the IRS expects

- A business using the physical method counts the goods on hand at the close of the tax year and keeps the count details with the books.
- Form 970 and Form 970-T are the US business income tax forms, and the cost of goods sold line depends on the inventory method.
- LIFO is capped by the $25 million gross receipts test in 26 USC 472(c) and was repealed for tax years beginning after 2024.
- A tracker that shows the count and the adjustment gives the accountant the trail the return needs.

## Sales tax and where the state matters

- Sales tax is a state and local tax, and after South Dakota v. Wayfair a remote seller with economic nexus in a state has to collect it there.
- Thresholds and rates differ by state, so the tracker carries a state column instead of a rate column.
- A marketplace seller may handle the state collection for some items, which changes what the seller of record has to report.
- Record the state the item was shipped to, not the state the warehouse sits in.

## Shipping promises and the mail order rule

- 16 CFR part 435 requires a reasonable basis to expect to ship within the promised time, or within 30 days when no time is stated.
- When the shipment will be late, the seller has to offer the buyer a delay or a prompt refund, generally within 7 working days.
- A backorder line on the tracker carries the revised date and the buyer's answer.
- A late-shipment notice goes out before the promise is broken and not after.

## Origin, returns and the records to keep

- 19 USC 1304 and the Customs and Border Protection rules require country-of-origin marking on imported goods.
- Record the returns window and the restocking terms the business published, not a generic 30-day assumption.
- Keep the count sheet, the adjustment log and the order records together for the tax year.
- Flag an item whose origin or tax treatment is unconfirmed instead of guessing.
