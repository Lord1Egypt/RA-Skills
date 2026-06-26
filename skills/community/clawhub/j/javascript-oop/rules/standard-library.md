# Standard Library

- Prefer standard helpers over custom utilities.
- Use `Number.isNaN()`, `Number.isFinite()`, and `Object.hasOwn()`.
- Use `RegExp.escape()` for user-provided regex fragments.
- Use `Error.isError()` when normalizing unknown thrown values.
- Prefer `Temporal` for new date/time domain logic when the runtime supports it.
- Use `Uint8Array.fromBase64()` and `.toBase64()` for binary-text conversion when the
  runtime supports them.

## Example

```js
const invoiceSearchPattern = new RegExp(RegExp.escape(searchTerm), "i");
const attachmentBytes = Uint8Array.fromBase64(base64Attachment);
const auditTimestamp = Temporal.Instant.from(submittedAtIsoText);
```

## End Check

- Verify standard helpers replace hand-rolled utilities.
- Verify standard helpers are used inside repositories, services, or value-object
  workflows.
- Verify newer binary helpers are gated by runtime support.
