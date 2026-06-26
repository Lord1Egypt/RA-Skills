---
name: myipchecker-ip-info
description: Query the public MyIPChecker IP information API and explain or return the geolocation and network fields it provides. Use when Codex needs to look up metadata for a specific IPv4 address, fetch the caller IP information when no `ip` query parameter is provided, troubleshoot live responses from MyIPChecker, or make a real request to the deployed endpoint from a helper script.
---

# MyIPChecker IP Info

Treat the deployed MyIPChecker IP information endpoint as the only source of truth for this skill.

Read [references/myipchecker-api.md](references/myipchecker-api.md) before describing parameters, response fields, or observed failure behavior.

Use [scripts/get_myipchecker_ip_info.sh](scripts/get_myipchecker_ip_info.sh) for live requests. The script is a pure shell helper that uses `curl` and already sends a browser-style `User-Agent`, because the deployed site blocks simple non-browser request signatures.

Do not describe this API as the repo's local ping route. The public endpoint currently returns IP metadata such as country, city, coordinates, timezone, ISP, and AS information.

## Workflow

1. Decide whether the user wants a live lookup, the caller IP info, an explanation of response fields, or troubleshooting for a failed request.
2. Read `references/myipchecker-api.md` for the current contract and observed edge cases.
3. Prefer a real request through `scripts/get_myipchecker_ip_info.sh`.
4. Pass `--ip <ipv4>` when the user gives a target IP.
5. Omit `--ip` when the user wants the caller IP information from the deployed service.
6. Treat non-200 responses, empty bodies, or invalid JSON as upstream/API failures rather than successful lookups.
7. Summarize the returned fields in plain language unless the user explicitly asks for raw JSON.

## Request Rules

- Use `ip` as the only supported lookup parameter.
- Do not rely on `target`; observed requests with `target` fall back to caller-IP behavior.
- Use a browser-style `User-Agent` for live calls.
- Expect JSON on success.
- Handle empty error bodies gracefully.

## Response Rules

- Successful responses are plain JSON objects, not the repo's `code/message/data` wrapper.
- Common fields include `ip`, `country`, `countryCode`, `region`, `city`, `zip`, `lat`, `lon`, `timezone`, `isp`, `org`, and `as`.
- Some fields may be absent depending on the looked-up IP.
- For invalid or unsupported inputs, the deployed API may return an HTTP error with no JSON body.

## Examples

- Input: `Look up 8.8.8.8 in MyIPChecker`
  Output: Run `sh skill/myipchecker-ip-info/scripts/get_myipchecker_ip_info.sh --ip 8.8.8.8`, then summarize the country, city, coordinates, timezone, and network owner.

- Input: `What does the deployed IP info endpoint return with no parameters?`
  Output: Explain that the deployed endpoint returns metadata for the caller IP when `ip` is omitted, then use the helper script without `--ip` if a live call is required.

- Input: `Why did my lookup fail with a 500 response?`
  Output: Explain that the upstream API can fail before returning a successful lookup payload, and that the error body may be empty or may contain a separate error JSON object.

## Live Call Commands

```bash
sh skill/myipchecker-ip-info/scripts/get_myipchecker_ip_info.sh
sh skill/myipchecker-ip-info/scripts/get_myipchecker_ip_info.sh --ip 8.8.8.8
sh skill/myipchecker-ip-info/scripts/get_myipchecker_ip_info.sh --ip 1.1.1.1
sh skill/myipchecker-ip-info/scripts/get_myipchecker_ip_info.sh --base-url <service-base-url> --ip 103.224.172.246
```

If a live request fails with Cloudflare 1010 or another non-JSON response, say so plainly and include the HTTP status plus any response body that is available.
