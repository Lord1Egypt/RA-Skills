# Events

- Emit objects, not primitives.
- Name payload fields explicitly.
- Prefer stable domain event names.
- Publish ids and DTO fields, not mutable object graphs.

## Example

```js
publish("invoice.submitted", {
    invoiceId,
    customerId,
    submittedAt,
});
```

## End Check

- Verify payload fields are explicit.
- Verify event payloads act as stable DTO contracts.
- Verify event names stay stable and domain-oriented.
