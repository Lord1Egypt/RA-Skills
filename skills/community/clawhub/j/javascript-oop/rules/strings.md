# Strings

- Use double quotes for string literals.
- Use template literals for interpolation and multiline text.
- Avoid unnecessary escaping.
- Do not use `eval()`.

## Example

```js
const serviceName = "billing";
const statusMessage = `${serviceName} service is ready`;
const sql = `select id from invoices where status = "OPEN"`;
```

## End Check

- Verify template literals improve readability.
- Verify string handling does not depend on `eval()`.
