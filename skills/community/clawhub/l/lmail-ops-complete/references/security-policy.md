# Security Policy

## Secret Handling
- Never print full values for API keys, JWTs, permits, or passwords.
- Store credentials in local files with mode `0600`.
- Avoid sending credentials through chat logs.

## Permit and Override Safety
- Treat permits as one-time secrets.
- Use admin override permits only for verified false positives.
- Always include a reason with a ticket or case reference.

## Least Privilege
- Prefer normal agent credentials for worker flows.
- Use admin tokens only for admin endpoints.
- Avoid long-lived terminal exports of secrets.

## Logging
- Keep logs concise and redacted.
- Preserve timestamps and endpoint names for auditability.
- Do not include request bodies containing secrets.
