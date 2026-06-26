# Destructuring

- Destructure when names stay obvious.
- Prefer parameter objects and object returns for multi-field APIs.
- Defaults apply only to `undefined`.
- Guard nullable intermediates before nested destructuring.

## Example

```js
function buildInvoiceSummary({ invoiceId, customerName = "Unknown", tags = [] }) {
    const [primaryTag] = tags;
    return { invoiceId, customerName, primaryTag };
}
```

## End Check

- Verify destructuring improves names instead of hiding them.
- Verify nullable inputs are guarded before deep access.
