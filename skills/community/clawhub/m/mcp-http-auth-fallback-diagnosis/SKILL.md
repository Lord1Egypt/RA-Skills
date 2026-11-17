---
name: "mcp-http-auth-fallback-diagnosis"
description: "Diagnose MCP HTTP 401/405 fallback errors by isolating credentials, transport, and runtime interpolation."
---

# MCP HTTP authentication fallback diagnosis

## When to use

Use when an HTTP MCP client reports 401, 405, or a fallback/SSE error and the endpoint previously worked or credentials may rotate.

## Procedure

1. Record the configured endpoint, transport, auth mode, and header shape. Never print credential values.
2. Test the primary MCP endpoint directly with the configured credential and an MCP initialize request. Capture only HTTP status and protocol response.
3. Repeat with the current trusted runtime credential, keeping endpoint and request identical.
4. Interpret the split:
   - configured credential fails, runtime credential succeeds: credential drift; do not blame transport.
   - both fail identically: continue endpoint, protocol, and transport diagnosis.
   - primary request returns 401 before a later 405: treat the 405 as possible fallback noise until authentication is resolved.
5. Inspect the installed client's documentation or source to confirm whether HTTP headers support environment interpolation. Do not assume config interpolation matches command-argument interpolation.
6. If supported, replace the static secret with the documented runtime environment placeholder. Keep the secret out of persisted config and logs.
7. Ensure the launching process actually receives the environment variable; a correct placeholder with a missing variable is not a fix.
8. Re-run the client's schema/list operation against the named server. For mcporter, the evidenced check is `mcporter list <server> --schema --output json`.

## Pitfalls

- Diagnosing the final fallback status instead of the first primary-endpoint failure.
- Rotating the external token while leaving a copied Bearer token in client config.
- Claiming interpolation support from general docs without checking header materialization.
- Comparing or logging full tokens; compare presence or equality without exposing values.
- Declaring recovery from a raw HTTP 200 alone; verify through the actual MCP client.

## Verification

Require both:

1. Primary MCP initialize succeeds with the runtime-backed header and returns a protocol response.
2. The actual client lists the server schema successfully without exposing the credential.
