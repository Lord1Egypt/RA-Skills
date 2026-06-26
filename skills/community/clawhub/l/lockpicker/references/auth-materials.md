# Auth materials

## Typical items
Depending on the site, replay may require some or all of:
- raw `Cookie` header
- csrf token header
- Authorization header
- client headers such as language, active-user flags, origin, or referer

## Safe handling rules
- Extract the minimum needed.
- Keep auth local.
- Prefer plain text runtime files in `workspace/tmp/`.
- Do not paste secrets into chat unless the user explicitly chooses to.
- Refresh expired values from the browser instead of trying bypasses.

## Common local file layout
- `tmp/site-cookie-header.txt`
- `tmp/site-csrf-token.txt`
- `tmp/site-authorization.txt`

## Common sources
- DevTools request headers
- browser storage/cookies for the same logged-in session
- a user-provided exported header string

## Warnings
- These values often grant live account access.
- Reusing them may violate the service's terms.
- The service may revoke, rotate, or challenge them without warning.
