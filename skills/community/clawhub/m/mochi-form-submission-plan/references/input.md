# Input contract

fields: list of name, optional required/type/sensitive. values: name-to-value map. finalAction: optional action label. Reports field names, never values.

## Operational scope

Use observed browser fields rather than guessed selectors. The helper never fills or submits a form. Apply the host approval rules to the final browser action, especially purchases, agreements and account permissions.

## Fictional example

```json
{
  "fields": [
    {
      "name": "email",
      "required": true
    },
    {
      "name": "message",
      "required": true
    }
  ],
  "values": {
    "email": "demo@example.com",
    "message": "Fictional inquiry"
  }
}
```

## Results

The helper returns `ok`, a task-specific `result`, a report path and an artifact list with byte counts and SHA-256. `ok=true` means this local transformation completed; use the explicit result fields for remaining work. Source files are not overwritten. Python3.10+ is required; IANA timezone support needs timezone data on the operating system or the Python tzdata package.
