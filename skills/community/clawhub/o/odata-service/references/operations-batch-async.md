# Functions, actions, batch, and asynchronous requests

## Functions and actions

Functions are side-effect-free and invoked with GET. Actions may change state and are invoked with POST. Resolve overloads, binding type, namespace-qualified name, parameters, and return type from CSDL.

```text
GET Products/Namespace.TopSelling(count=10)
GET Products(1)/Namespace.GetTax(rate=@r)?@r=0.2
POST Orders(1)/Namespace.Submit
{"note":"approved"}
```

Treat actions with the same authorization, ETag, ambiguity, and no-automatic-retry rules as other mutations. A function result may still be paged.

## Batch

POST to `{service-root}/$batch`. OData supports multipart batch; OData 4.01 also defines JSON batch. Use the format advertised/accepted by the service.

A JSON batch document contains a `requests` array. Each request has a unique string `id`, `method`, relative `url`, optional `headers` and `body`; `dependsOn` expresses dependencies, and a shared `atomicityGroup` groups requests atomically. Multipart batch uses `multipart/mixed` boundaries and change sets for atomic modifications.

Example 4.01 JSON batch with an atomic create/update group:

```json
{
  "requests": [
    {
      "id": "1",
      "atomicityGroup": "g1",
      "method": "POST",
      "url": "Products",
      "headers": {"content-type": "application/json"},
      "body": {"Id": 7, "Name": "Road Bike"}
    },
    {
      "id": "2",
      "atomicityGroup": "g1",
      "dependsOn": ["1"],
      "method": "PATCH",
      "url": "Products(7)",
      "headers": {"content-type": "application/json", "if-match": "*"},
      "body": {"Price": 1200}
    }
  ]
}
```

Replace every URL, key, property, ETag, and payload from the target metadata and current state. The `If-Match: *` above is illustrative; prefer the actual ETag when updating an existing resource. Send this through the helper with `request --path '$batch' --method POST --body-file batch.json --content-type application/json --allow-write`. For OData 4.0 or services without JSON batch, construct an exact `multipart/mixed;boundary=...` body and pass its complete content type; do not hand-edit boundary values after calculating the body.

Before sending:

- Validate every relative URL, method, payload, content ID/request ID, dependency, and ETag.
- Use an atomic group only when all grouped changes must commit or roll back together.
- Do not assume ordering without dependencies.
- Estimate payload and operation counts against service limits.
- Treat the batch as one mutation for retry ambiguity; a transport failure may occur after some non-atomic operations committed.

After receiving a response, parse every subresponse. Independent requests can have mixed results even when the outer HTTP status is successful. Within an atomic group, identify the failing request and verify rollback rather than assuming it.

## Preferences

Useful `Prefer` tokens include `return=representation`, `return=minimal`, `odata.maxpagesize=N`, `odata.include-annotations="..."`, `continue-on-error`, and `respond-async`. Support is optional; inspect `Preference-Applied` rather than assuming the service honored a preference.

`continue-on-error` changes independent batch processing, not atomic group guarantees.

## Asynchronous processing

Send `Prefer: respond-async` only when supported and appropriate. A service may reply `202 Accepted` with a status-monitor URL in `Location` and possibly `Retry-After`.

Poll the monitor with bounded GET requests, honoring `Retry-After`. Follow updated monitor locations safely. Do not resend the original operation merely because processing is still pending. Stop on completion, failure, expiry (`404`/`410`), user cancellation, or the declared poll/time limit. The completed response may itself contain a normal OData response or a batch result that still requires per-item parsing.
