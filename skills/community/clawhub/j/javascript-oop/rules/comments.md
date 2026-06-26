# Comments

- Explain intent, invariants, or tradeoffs.
- Use `//` for local notes and `/** ... */` for API docs.
- Keep `TODO:` and `FIXME:` actionable.
- Delete comments that repeat code.

## Example

```js
/**
 * Keep retry policy here so invoice rules stay independent from transport failures.
 */
const retryLimit = 3;
```

## End Check

- Verify comments explain why, not syntax.
- Verify old comments still match the code.
