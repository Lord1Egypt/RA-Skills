# Collections

- Prefer array literals and change-by-copy methods like `toSorted()` and `toSpliced()`.
- Prefer iterator helpers for lazy pipelines inside services and repositories; call
  `toArray()` at the boundary.
- Prefer Set algebra methods like `intersection()` and `union()` over manual loops when
  they clarify domain intent.
- Use `for...of` when control flow or `await` matters.
- Be explicit about shallow copies versus `structuredClone()`.

## Example

```js
const visibleInvoiceIds = Iterator.from(invoiceRepository.findVisible())
    .map((invoiceSummaryDto) => invoiceSummaryDto.invoiceId)
    .take(50)
    .toArray();
const eligibleInvoiceIds = submittedInvoiceIds.intersection(reviewableInvoiceIds);
```

## End Check

- Verify lazy pipelines stay lazy until `toArray()` or another terminal step.
- Verify Set algebra replaces manual membership loops where it clarifies intent.
- Verify collection helpers support service or repository workflows instead of replacing
  object boundaries.
- Verify copy depth matches the data being handled.
