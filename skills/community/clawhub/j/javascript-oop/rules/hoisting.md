# Hoisting

- Use `const` and `let`, never `var`.
- Declare values before use.
- Treat TDZ failures as design feedback.
- Do not rely on hoisting for control flow.

## Example

```js
const total = calculateInvoiceTotal(lineItems);

function calculateInvoiceTotal(items) {
    return items.reduce((sum, item) => sum + item.amount, 0);
}
```

## End Check

- Verify declarations appear before reads.
- Verify `var` is not introduced.
