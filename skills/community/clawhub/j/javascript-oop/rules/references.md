# References

- Use `const` by default.
- Use `let` only for real reassignment.
- Do not use `var`.
- Keep scope narrow.

## Example

```js
const invoiceId = request.invoiceId;
let retryCount = 0;
retryCount += 1;
```

## End Check

- Verify `let` signals actual reassignment.
- Verify scopes stay as small as possible.
