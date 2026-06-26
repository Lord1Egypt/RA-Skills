# Objects

- Prefer object literals, shorthand, and dot notation.
- Use computed keys only for truly dynamic names.
- Prefer object spread for shallow copies.
- Prefer `**` over `Math.pow()`.
- Treat DTOs as transport carriers, not business objects.
- Treat value objects as validated domain concepts with explicit construction boundaries.
- Avoid anonymous shape drift across layers.

## Example

```js
const invoiceSummaryDto = {
    invoiceId,
    customerName,
    riskScore: baseRiskScore ** 2,
};
```

## End Check

- Verify dynamic keys are genuinely dynamic.
- Verify DTOs and value objects are not blurred together.
- Verify value-object boundaries stay explicit and predictable.
- Verify spread copies are shallow by design.
