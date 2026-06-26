# Functions

- Keep one business responsibility per function.
- Prefer parameter objects over long positional lists.
- Do not mutate inputs.
- Restrict free functions to tiny pure transforms, validators, mappers, and calculators.
- Keep workflows and orchestration on named services or use cases.
- Inject dependencies through parameters, not module globals.

## Example

```js
function buildInvoiceTotal({ lineItems, taxRate }) {
    const subtotal = lineItems.reduce((sum, lineItem) => sum + lineItem.amount, 0);
    return subtotal + subtotal * taxRate;
}
```

## End Check

- Verify multi-field APIs use parameter objects.
- Verify workflows are not hidden inside utility functions.
- Verify helper functions stay free of hidden dependencies.
