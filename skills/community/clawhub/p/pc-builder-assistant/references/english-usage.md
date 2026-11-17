# English usage

Read this file when the user's request is primarily in English or explicitly asks for an English answer.

## Activation

- Activate this layer when the user's natural-language request is primarily English or the user explicitly asks for an English answer.
- Do not activate it merely because a Chinese request contains English hardware models, software names, acronyms, or commands.
- For a mixed-language request, follow an explicit output-language instruction. If none is given, use the predominant language of the natural-language clauses and ignore model names when deciding.
- In follow-up turns, honor the user's latest explicit language choice. Stop loading this layer after the user clearly switches back to Chinese.
- Load this file before any Chinese reference required for the task so the translation and output boundary is active first.

## Translation layer

- Treat Chinese references as the single source of selection rules. Read only the references required by the request and use their content as internal evidence; do not copy their headings, sentences, or user-facing labels.
- After querying and checking compatibility, reduce the result to structured facts: exact model, specification, selected price and currency, price date, compatibility finding, trade-off, and verification item. Write the final response from those facts in English.
- Use these user-facing labels: `CPU`, `Motherboard`, `Memory`, `Storage`, `Graphics card`, `CPU cooler`, `Power supply`, `Case`, `Case fans`, `Display`, `Unit price`, `Total`, `Budget difference`, `Compatibility`, and `Local buying note`.
- Before sending, review the answer for Chinese text. Chinese characters are allowed only inside an exact product or model name returned by the catalog. Rewrite Chinese headings, explanations, compatibility messages, dates, and internal status text in English.

## Reference routing

- For a complete build, read `routing.md`, `selection-policy.md`, the relevant part of `scenarios.md`, `hardware-scope.md`, `pricing.md`, and `compatibility.md` after this file. After drafting the first parts list, apply the budget-closure, default-capacity, component-quality, and balance rules from those references before writing the final answer.
- In a complete build, turn every scenario-required item with an available catalog candidate into a priced row. Do not leave a queryable required item as an unpriced budget reserve.
- For an upgrade, configuration completion, or compatibility review, read `workflows.md` plus only the scenario, pricing, selection, and compatibility references needed for that request.
- For a hardware-selection question, read the relevant section of `hardware-faq.md`. Query exact products only when the question requires models or prices.
- For local LLM sizing in either direction (hardware to model, or model parameter count to GPU/RAM), read `local-model-fit.md` and use the same estimator. Translate only its structured result; keep minimum-versus-recommended VRAM, quantization, context, offload, and estimate caveats intact.
- This routing is procedural. Do not restate or maintain a second copy of the Chinese selection rules here.

## Scope

- Reply in English and keep hardware model names unchanged.
- Support desktop PC build planning, upgrades, configuration completion, compatibility reviews, budget allocation, and hardware selection explanations.
- Keep the existing scenario, component-selection, price, and compatibility rules. Run the same query and strict compatibility scripts before recommending a complete build.
- Do not expand into software tutorials, operating-system troubleshooting, or second-hand hardware.
- Do not use this skill for laptops, enterprise or server procurement, ordering or payment, remote control, or security-isolation work.

## Market boundary

- The bundled catalog and channel quotes describe the Chinese market and use CNY.
- If the user supplies local prices in text or an image, read `user-catalog.md`. Convert the evidence into the documented JSON only after checking the exact SKU and currency, validate it, and pass the same explicit overlay to both query and compatibility commands. The scripts never question the user, inspect images, browse, or discover local files; the Agent owns those steps.
- Prefer an exact base `target_id` when the bundled catalog already has the SKU: a quote patch inherits its specifications without overwriting them. For a genuinely new SKU, use a `user-<category>-...` ID. Search an official product page only for compatibility-critical fields absent from both the base catalog and the user's evidence; otherwise ask the user to supplement them and keep the result review-required.
- A selected user overlay currency is a local user quote, not a converted China-market quote. Keep currencies separate and never add, compare, budget-filter, or sort CNY and non-CNY prices together. Preserve the bundled CNY value only as a separate reference field.
- Do not present a currency conversion as a local retail quote. Do not claim that a listed model, suffix, color, warranty, stock level, or price is available in the user's country.
- If the user asks what to buy locally, provide hardware criteria and a China-market reference build, then ask them to verify equivalent local SKUs, retailers, warranty terms, stock, and prices.
- Do not convert currencies by default. A budget stated in USD or another non-CNY currency counts as a request for conversion only when no matching user-price overlay exists: verify a current exchange rate before querying, translate the budget into a CNY target, retain the CNY total, and show an approximate total in the user's currency. State the exchange-rate date and make clear that the conversion is not a local retail quote.
- For every non-CNY budget, the final market note must name the checked exchange-rate date; a conversion statement without that date is incomplete.
- Keep the CNY component total separate from local tax, shipping, rebates, and checkout-only discounts. Show those separately only when the user asks.
- Exclude RTX 5090D and RTX 5090D V2 from default English recommendations. Compare them only when the user explicitly asks about China-region GPU variants.
- Cases, CPU coolers, case fans, and power supplies vary strongly by region. Give each selected row a short, concrete local buying note such as `Check for a local 650W ATX 3.1 equivalent`.
- Put that note directly in each selected case, cooler, fan, and power-supply row. Do not replace the row notes with one generic verification list.
- Leave the local-verification field blank for CPU, motherboard, memory, storage, and graphics-card rows unless that exact SKU has a documented regional restriction. Do not add generic stock, warranty, or availability notes to those rows.

## User-facing output

- For a complete build, use the columns `Component | Exact model | Unit price | Local buying note`. Keep exact product model names.
- Leave `Local buying note` blank for CPU, motherboard, memory, storage, and graphics-card rows. Fill it only for each selected CPU cooler, power supply, case, and case-fan row, unless a standard row has a documented regional restriction.
- Give one primary build. Add one compact alternative only when the request has a genuine decision fork.
- Use one price currency per total. Without a matching user overlay, show every selected component and the total in CNY. With an explicit overlay, total only rows carrying the selected matching currency; never add uncovered CNY rows to a USD/EUR/GBP/JPY/TWD subtotal. If the overlay does not price every required row, state that local-price coverage is partial and do not claim a complete local-currency total.
- Take the reference date only from the current query result rows selected for the quote. Treat a quote older than 14 days as stale for current-budget closure, follow the search fallback when available, and never reuse a date from an example, an older report, or memory.
- Keep the report compact: eight core component rows, optional fan or display rows when requested, total, compatibility result, two to four useful trade-offs, and one market note. Do not expose command names, exit codes, internal status labels, test markers, raw templates, or Chinese column labels.
- Never expose words such as `strict`, `complete`, pass/check counts, skipped checks, or script status. Distinguish the three outcomes in natural English: a hard conflict; no hard conflict found with specific checks still open; or no hard conflict found with the required fields verified. When checks remain open, say `The available specifications show no hard incompatibility, but these items still need verification:` and name the concrete items.
- A separate verification list is only for concrete compatibility uncertainties such as QVL, physical clearance, connector availability, or an unknown catalog field. Do not use it for generic SKU, stock, warranty, or availability reminders.
- Use one natural market note that fits the request instead of repeating a fixed disclaimer:
  - Full quote: `CNY prices are China-market references dated YYYY-MM-DD; local price and stock can differ.`
  - Local buying request: `Treat these as China-market equivalents and verify local SKUs, warranty, stock, and store pricing.`
  - User-price overlay: `The CUR prices are user-supplied observations dated YYYY-MM-DD; verify the exact SKU and checkout price.`
  - Currency request: `Using the exchange rate checked on YYYY-MM-DD, the CNY total is about USD X. This is a currency conversion; local prices and stock can differ.`
- Do not stack these notes or repeat them after every component.

## Final check

- Every queryable item required by the loaded Chinese scenario is a priced row in the selected currency and is included in that currency's total; otherwise the answer explicitly says coverage is partial and omits a mixed-currency total. Do not show a budget difference until all required rows are priced in the same currency with usable dates.
- Exact catalog product names remain unchanged; Chinese text appears nowhere else.
- Each selected cooler, power supply, case, and case-fan row has its own short local buying note.
- Every displayed price date comes from the selected query result rows.
