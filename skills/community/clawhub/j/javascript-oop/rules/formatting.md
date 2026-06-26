# Formatting

- Use spaces and 4-space indentation unless the project formatter differs.
- Use one space after keywords and around operators.
- Use trailing commas in multiline literals.
- End files with one newline.
- Always use semicolons.

## Example

```js
const invoiceConfig = {
    retries: 3,
    region: "eu",
};
```

## End Check

- Verify formatter output matches local project defaults.
- Verify multiline literals keep trailing commas when supported.
