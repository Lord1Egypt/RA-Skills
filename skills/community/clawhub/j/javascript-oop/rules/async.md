# Async

- Prefer `async` and `await` for readable flows.
- Use `Promise.try()` at sync-or-async boundaries when a call may throw or return a
  promise.
- Use `Array.fromAsync()` for async iterables inside service or repository flows; use
  `Promise.all()` for known parallel tasks.
- Await, return, or intentionally detach every promise.
- Avoid `new Promise(async () => {})` and `forEach(async () => {})`.
- Treat top-level `await` as module-load coordination, not a default.

## Example

```js
async function loadInvoiceSummaries(invoiceRepository) {
    const invoiceIds = await Array.fromAsync(
        invoiceRepository.streamPendingInvoices(),
        (invoiceSummaryDto) => invoiceSummaryDto.invoiceId,
    );

    return Promise.try(() => invoiceRepository.loadMany(invoiceIds));
}
```

## End Check

- Verify `Promise.try()` wraps boundary calls, not ordinary async code.
- Verify `Array.fromAsync()` is used for async iteration, not parallel batching.
- Verify async helpers live inside service or repository workflows.
- Verify every promise is awaited, returned, or intentionally detached.
