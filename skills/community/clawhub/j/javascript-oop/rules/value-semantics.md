# Value Semantics

- Use `===` and `!==`, never loose equality.
- Convert at the boundary with `String()`, `Number()`, `Boolean()`, or
  `parseInt(value, 10)`.
- Use `??` for missing values; use `||` only when any falsy value should fall back.
- Optional chaining returns `undefined` and only short-circuits the touched segment.
- Parenthesize mixes of `??` with `&&` or `||`.
- Remember coercion surprises like `"5" + 1` and `Number("")`.

## Example

```js
const page = parseInt(searchParams.get("page") ?? "1", 10);
const retryDelayMs = config.retryDelayMs ?? 1000;
const city = customer?.address?.city ?? "Unknown";
const isConfigured = settings.enabled === true;
```

## End Check

- Verify strict equality is used intentionally.
- Verify defaults do not hide valid falsy inputs.
- Verify conversions happen at input boundaries.
