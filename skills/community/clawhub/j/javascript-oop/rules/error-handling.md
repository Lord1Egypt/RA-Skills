# Error Handling

- Throw `Error` objects or subclasses.
- Catch only to recover, convert, or add context.
- Prefer concrete domain errors for business failures.
- Use `cause` when wrapping lower-level errors.

## Example

```js
class PaymentDeclinedError extends Error {
    constructor(invoiceId) {
        super(`Payment for invoice ${invoiceId} was declined`);
        this.name = "PaymentDeclinedError";
    }
}
```

## End Check

- Verify catches add context or recovery.
- Verify domain failures use concrete error types.
- Verify thrown values are always `Error` instances.
