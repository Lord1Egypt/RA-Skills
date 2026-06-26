# Arrow Functions

- Use arrows for callbacks and short local functions.
- Keep parentheses around parameters.
- Use implicit returns only for one expression.
- Do not use arrows for methods that need dynamic `this`.

## Example

```js
const invoiceIds = invoices
    .map((invoice) => invoice.id)
    .filter((invoiceId) => invoiceId !== null);
```

## End Check

- Verify arrows stay local, not stateful methods.
- Verify long bodies use explicit `return`.
