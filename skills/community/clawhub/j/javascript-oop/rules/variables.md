# Variables

- Declare one variable per statement.
- Group `const` declarations before `let` declarations.
- Declare values close to use.
- Prefer `+= 1` and `-= 1` over `++` and `--`.
- Avoid chain assignments.

## Example

```js
const invoiceId = request.invoiceId;
const customerId = request.customerId;
let retryCount = 0;
retryCount += 1;
```

## End Check

- Verify declarations stay close to their usage.
- Verify mutation is visible through `let`.
