Audit pasted HTTP response headers for missing security headers — HSTS, CSP, XFO, XCTO, Referrer-Policy, Permissions-Policy, cookie flags. Offline, zero deps.

`curl -sI https://example.com | node scripts/headers.js -`

Free lite version of `http-header-audit` — the full skill ($9) adds live fetch, CORS, redirect chains. See SKILL.md for agent workflow.
