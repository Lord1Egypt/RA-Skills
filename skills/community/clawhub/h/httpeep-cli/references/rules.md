<!-- GENERATED FILE: DO NOT EDIT DIRECTLY. -->
<!-- Source of truth: docs.httpeep.com/content/docs/cli/rules.mdx -->
<!-- Generate with: node scripts/generate-httpeep-cli-skill-reference.mjs <references-dir> -->

# Rules

The `rules` command manages HTTPeep traffic manipulation rules from the terminal. Use it to create mock APIs, redirect traffic to staging, inject headers, simulate latency, block tracking requests, export a ruleset, or test whether a request would match a rule.

```bash
# `hp` is the short alias for `httpeep-cli`
hp rules list
httpeep-cli rules list
```

> **Note:**
> The new `create` and `update` flags are a CLI-friendly input layer. HTTPeep still stores rules in the existing `ForwardRuleConfig` format under `~/.httpeep/rules/rule.yaml`, so rules created from the CLI remain compatible with the desktop app and the runtime engine.

## Command overview

| Command | Purpose |
|---|---|
| `rules create` | Create one persistent rule from flags or `--from-file` |
| `rules list` | List rules, optionally filtered by group or enabled state |
| `rules show` | Show one rule by ID or unique name |
| `rules update` | Patch one existing rule by ID or unique name |
| `rules delete` | Delete one rule |
| `rules enable` / `rules disable` | Toggle one rule, or every rule in a group |
| `rules reorder` | Move a rule before/after another rule or to top/bottom |
| `rules export` / `rules import` | Back up or restore rules |
| `rules validate` | Validate a rule payload before applying it |
| `rules test` | Test whether a request matches current rules |
| `rules run` | Run a command with temporary rules and automatic rollback |

## Mental model

`rules create` and `rules update` organize flags in the same order as HTTPeep's rule pipeline:

1. **Matcher** — choose which requests the rule applies to.
2. **Resolve action** — pass through, map remote, map local, or block.
3. **Request pipeline** — modify the request before it reaches the target.
4. **Response pipeline** — modify the response before it returns to the client.

Rules are evaluated top-to-bottom. Use `rules reorder` when one rule should take priority over another.

## Create rules

At least one matcher is required. If `--action` is omitted, HTTPeep creates a pass-through rule that can still run request or response pipeline actions.

### Map a production host to staging

```bash
hp rules create "staging API" \
  --match-host "api.example.com" \
  --action map-remote \
  --map-remote-url "https://staging.example.com" \
  --req-remove-header "Authorization" \
  --req-set-header "Authorization:Bearer staging-token" \
  --req-set-query "env=staging" \
  --group "staging" \
  --comment "Route production API calls to staging during local testing"
```

### Serve a local mock file

```bash
hp rules create "mock users API" \
  --match-url "https://api.example.com/v1/users/*" \
  --match-method "GET,POST" \
  --action map-local \
  --map-local-file ./mocks/users.json \
  --map-local-status 200 \
  --map-local-content-type application/json \
  --res-set-header "X-Mock:true" \
  --group "mock"
```

### Return an inline error body

```bash
hp rules create "simulate login failure" \
  --match-path "/auth/login" \
  --match-method POST \
  --res-status 401 \
  --res-set-header "Content-Type:application/json" \
  --res-set-body '{"error":"invalid credentials"}'
```

### Simulate slow or unreliable network

```bash
hp rules create "slow checkout" \
  --match-host "api.example.com" \
  --match-path "/checkout*" \
  --req-delay 1500 \
  --res-delay 1000 \
  --res-throttle 40
```

### Block tracking requests

Return a normal HTTP response:

```bash
hp rules create "silent block analytics" \
  --match-host "*.analytics.com,*.tracking.io,gtm.example.com" \
  --action block \
  --block-mode reject \
  --block-status 200 \
  --block-body '{}'
```

Simulate a network-layer failure:

```bash
hp rules create "analytics network error" \
  --match-host "*.analytics.com,*.tracking.io" \
  --action block \
  --block-mode network-error
```

### Add request and response breakpoints

```bash
hp rules create "break checkout" \
  --match-path "/api/checkout" \
  --match-method POST \
  --req-breakpoint \
  --res-breakpoint \
  --group "debug"
```

### Apply rule-level DNS and upstream proxy

```bash
hp rules create "local dev DNS" \
  --match-host "api.myapp.com" \
  --req-dns-override "api.myapp.com:127.0.0.1" \
  --req-proxy "http://127.0.0.1:3001"
```

## Matcher flags

| Flag | Description |
|---|---|
| `--match-url <pattern>` | Match a full URL. A single value can contain comma-separated alternatives. |
| `--match-host <pattern>` | Match the request host. Comma-separated values are OR alternatives. |
| `--match-path <pattern>` | Match the path without query string. Comma-separated values are OR alternatives. |
| `--match-method <method>` | Match one or more HTTP methods, for example `GET,POST`. |
| `--match-header <key:value>` | Match request headers. Repeatable; comma-separated pairs are also accepted. |
| `--match-header-op <and\|or>` | Combine multiple header matchers. Default: `and`. |
| `--match-query <key=value>` | Match query parameters. Repeatable; comma-separated pairs are also accepted. |
| `--match-query-op <and\|or>` | Combine multiple query matchers. Default: `and`. |
| `--match-body <pattern>` | Reserved for future body matching. The current runtime schema rejects it instead of silently creating an over-broad rule. |

Pattern type is inferred automatically:

| Pattern | Inferred type |
|---|---|
| Contains `*` or `?` | Wildcard |
| Contains regex markers like `(`, `)`, `[`, `]`, `^`, `$`, `+` | Regex |
| Otherwise | Exact |

Examples:

```bash
# Wildcard host and path
hp rules create "mock v1 or v2 users" \
  --match-host "*.example.com" \
  --match-path "/api/v*/users*" \
  --res-set-header "X-Matched:true"

# Header OR logic
hp rules create "any debug header" \
  --match-host "api.example.com" \
  --match-header "X-Debug:true,X-Test:1" \
  --match-header-op or \
  --res-set-header "X-Debug-Rule:hit"

# Query AND logic, the default
hp rules create "staging debug query" \
  --match-host "api.example.com" \
  --match-query "debug=true,env=staging" \
  --res-set-header "X-Query-Rule:hit"
```

## Resolve actions

| Flag | Description |
|---|---|
| `--action pass-through` | Do not replace the upstream target; still allows pipeline actions. |
| `--action map-remote` | Forward matching requests to another remote URL. Requires `--map-remote-url`. |
| `--action map-local` | Serve a local file. Requires `--map-local-file`. |
| `--action block` | Reject the request or simulate a network error. |

Map remote:

```bash
hp rules create "redirect API to staging" \
  --match-host "api.example.com" \
  --action map-remote \
  --map-remote-url "https://staging.example.com"
```

Map local:

```bash
hp rules create "mock payment" \
  --match-path "/api/payment/*" \
  --action map-local \
  --map-local-file ./mocks/payment.json \
  --map-local-status 200
```

Block:

```bash
hp rules create "rate limit users endpoint" \
  --match-path "/api/users" \
  --action block \
  --block-mode reject \
  --block-status 429 \
  --block-body '{"error":"too many requests"}'
```

## Pipeline flags

### Request pipeline

| Flag | Description |
|---|---|
| `--req-dns-override <domain:ip>` | Use a rule-level DNS override. Repeatable. |
| `--req-proxy <url>` | Use a rule-level upstream proxy, for example `http://host:8080` or `socks5://127.0.0.1:1080`. |
| `--req-delay <ms>` | Delay before sending the upstream request. |
| `--req-throttle <kbps>` | Throttle request upload speed. |
| `--req-set-header <key:value>` | Set request headers. Repeatable; comma-separated pairs are accepted. |
| `--req-remove-header <key>` | Remove request headers. Repeatable. |
| `--req-set-query <key=value>` | Set query parameters. Repeatable; comma-separated pairs are accepted. |
| `--req-remove-query <key>` | Remove query parameters. Repeatable. |
| `--req-set-body <body\|@file>` | Replace the request body with a literal string or file content. |
| `--req-breakpoint` | Pause matching requests before upstream delivery. |

Examples:

```bash
# Inject auth and remove cookies
hp rules create "inject test auth" \
  --match-host "api.example.com" \
  --req-remove-header "Cookie" \
  --req-set-header "Authorization:Bearer test-token" \
  --req-set-header "X-Debug:true"

# Rewrite query parameters
hp rules create "force mock query" \
  --match-path "/api/search" \
  --req-set-query "mock=true,env=dev" \
  --req-remove-query "utm_source"

# Replace request body from a file
hp rules create "replace checkout body" \
  --match-path "/api/checkout" \
  --match-method POST \
  --req-set-body @./payloads/checkout.json
```

### Response pipeline

| Flag | Description |
|---|---|
| `--res-delay <ms>` | Delay before returning the response. |
| `--res-throttle <kbps>` | Throttle response download speed. |
| `--res-status <code>` | Rewrite the response status code. |
| `--res-set-header <key:value>` | Set response headers. Repeatable; comma-separated pairs are accepted. |
| `--res-remove-header <key>` | Remove response headers. Repeatable. |
| `--res-set-body <body\|@file>` | Replace the response body with a literal string or file content. |
| `--res-breakpoint` | Pause matching responses before returning them to the client. |

Examples:

```bash
# Force a 500 response
hp rules create "simulate 500" \
  --match-host "api.example.com" \
  --res-status 500 \
  --res-set-header "Content-Type:application/json" \
  --res-set-body '{"error":"internal server error"}'

# Remove cache headers
hp rules create "disable cache" \
  --match-host "cdn.example.com" \
  --res-set-header "Cache-Control:no-store" \
  --res-remove-header "ETag"

# Replace response body from a file
hp rules create "mock 404 response" \
  --match-path "/api/not-found" \
  --res-status 404 \
  --res-set-body @./responses/404.json
```

## Create from file

Use `--from-file` when a rule is too complex for one command. This file format is only a CLI input format; after creation, HTTPeep stores the compiled rule in the normal `ForwardRuleConfig` rules file.

```bash
hp rules create --from-file ./payment-rule.yaml
```

```yaml title="payment-rule.yaml"
name: "mock payment API"
enabled: true
group: "mock"
comment: "Used for local payment integration tests"

matcher:
  url: "https://api.example.com/payment/*"
  method: ["POST", "GET"]
  header:
    X-Client-Version: "2.*"
    X-Env: "staging"
  header_op: AND
  query:
    debug: "true"

resolve:
  action: map-local
  map_local:
    file: ./mocks/payment.json
    status: 200
    content_type: application/json

request_pipeline:
  delay_ms: 500
  set_headers:
    X-Debug: "true"
  remove_headers:
    - Cookie

response_pipeline:
  delay_ms: 200
  set_headers:
    X-Mock: "true"
```

JSON works too:

```json title="payment-rule.json"
{
  "name": "mock payment API",
  "enabled": true,
  "group": "mock",
  "matcher": {
    "path": "/payment/*",
    "method": ["POST"]
  },
  "resolve": {
    "action": "map-local",
    "map_local": {
      "file": "./mocks/payment.json",
      "status": 200
    }
  }
}
```

## List and show rules

```bash
# Human-readable list
hp rules list

# JSON list for scripts
hp --format json rules list

# Only enabled rules
hp rules list --enabled

# Rules tagged with group:mock
hp rules list --group "mock"
```

Show one rule by ID or by unique name:

```bash
hp rules show cli-rule-mock-users-api
hp rules show "mock users API"
hp --format json rules show "mock users API"
```

If more than one rule has the same name, use the rule ID.

## Update rules

`rules update` patches only the fields you provide. Existing matchers, resolve action, and pipeline actions remain unchanged unless you provide flags for that section.

```bash
# Change only the response status and body
hp rules update "simulate 500" \
  --res-status 200 \
  --res-set-body '{"ok":true}'

# Rename and regroup a rule
hp rules update cli-rule-mock-users-api \
  --name "mock users API v2" \
  --group "mock-v2" \
  --comment "Updated for the v2 contract"

# Replace the matcher and request pipeline
hp rules update "inject test auth" \
  --match-host "api-v2.example.com" \
  --req-set-header "Authorization:Bearer new-token"
```

You can also patch from a file:

```bash
hp rules update cli-rule-mock-payment-api --from-file ./payment-rule.yaml
```

## Enable, disable, delete

Toggle one rule:

```bash
hp rules disable "mock users API"
hp rules enable cli-rule-mock-users-api
```

Toggle a whole group:

```bash
hp rules disable --group "debug"
hp rules enable --group "mock"
```

Delete a rule:

```bash
hp rules delete "mock users API"
hp rules delete --id cli-rule-mock-users-api --force
```

## Reorder rules

Rules are matched in list order. Move a rule when priority matters:

```bash
# Evaluate first
hp rules reorder "silent block analytics" --to-top

# Evaluate last
hp rules reorder "slow checkout" --to-bottom

# Place one rule before another
hp rules reorder "mock users API" --before "staging API"

# Place one rule after another
hp rules reorder "inject test auth" --after "staging API"
```

Exactly one of `--before`, `--after`, `--to-top`, or `--to-bottom` is required.

## Import and export

Export writes the current compiled rules as JSON. Use it for backup or scripts:

```bash
# Export to stdout
hp rules export

# Export to a file
hp rules export --output ./rules-backup.json
```

Import accepts both the existing `ForwardRuleConfig` JSON/YAML format and the structured CLI input format shown above.

```bash
# Replace all non-builtin rules (default)
hp rules import ./rules-backup.json

# Merge with existing rules
hp rules import ./rules-backup.json --mode merge

# Import a structured CLI rule file
hp rules import ./payment-rule.yaml --mode merge
```

| Flag | Description | Default |
|---|---|---|
| `--mode replace` | Replace all non-builtin rules with imported rules | `replace` |
| `--mode merge` | Upsert imported rules into the current ruleset | — |

## Validate and test

Validate before writing:

```bash
# Validate an upsert payload
hp rules validate --rule-file ./rule.yaml

# Validate as a full replacement
hp rules validate --replace --rule-file ./rules-full.json
```

Test whether a request would match:

```bash
hp rules test \
  --url "https://api.example.com/v1/users?debug=true" \
  --method GET \
  -H "X-Debug: true"
```

JSON output includes whether anything matched, matched rule details, terminal action, and request/response step counts:

```bash
hp --format json rules test \
  --url "https://api.example.com/v1/users" \
  --method POST
```

## Temporary rules

`rules run`, `request`, and `replay` still support shortcut rule flags. These rules are temporary and roll back automatically after the command exits.

```bash
hp rules run \
  --map-remote "api.example.com=http://127.0.0.1:3000" \
  -- hp request --method GET --url "https://api.example.com/users"
```

Agent-friendly JSON output:

```bash
hp rules run \
  --json \
  --reject "api.example.com/orders=503" \
  -- hp replay --id s1
```

Exit code convention:

- If rule parsing or validation fails, `rules run` exits non-zero.
- If the executed command fails, `rules run` exits with the command's exit code.
- With `--json`, the output includes `exit_code` and `success` fields.

## Legacy shortcut parameters

These shortcut flags remain available for `rules upsert`, `rules replace`, `rules validate`, `rules run`, `request`, and `replay`.

| Flag | Format | Description |
|---|---|---|
| `--rule` | Inline JSON string | Full compiled rule JSON. Repeatable. |
| `--rule-file` | File path | Compiled rule file, JSON or YAML. Repeatable. |
| `--map-remote` | `<match>=<target>` | Redirect matching requests to another host. |
| `--map-local-file` | `<match>=<file_path>` | Serve a local file for matching requests. |
| `--inline-response` | `<match>=<status>:<mime>:<content>` | Return an inline response. |
| `--reject` | `<match>=<status>` | Reject matching requests with a status code. |
| `--delay` | `<match>=<ms>` | Add a request delay in milliseconds. |
| `--throttle` | `<match>=<spec>` | Throttle bandwidth, for example `100` or `req=100,res=200`. |

`<match>` supports host, `host/path`, `/path`, full URL, and wildcards.

Examples:

```bash
# Persistent upsert with a shortcut
hp rules upsert --map-remote "api.example.com=http://127.0.0.1:3000"

# Temporary local file mapping for one request
hp request --method GET --url "https://example.com/banner" \
  --map-local-file "example.com/banner=./fixtures/banner.json"

# Temporary inline response
hp request --method GET --url "https://api.example.com/health" \
  --inline-response "/health=503:text/plain:maintenance"

# Temporary delay and throttle
hp request --method GET --url "https://api.example.com/feed" \
  --delay "api.example.com/feed=300" \
  --throttle "api.example.com/feed=req=100/200,res=150"
```

`--inline-response` supports `@file` for the content segment. If the literal content must start with `@`, write `@@...`.

## Plan-gated response modification

Before creating rules that modify an upstream response body, status, or headers, check the current entitlement:

```bash
hp --format json license status
```

Response modification actions are a Pro capability. On a plan without that entitlement, a rule using response modification may fail with:

```text
Response modification actions are a Pro feature.
```

When you only need to mock an endpoint, use a resolve-based response such as `--inline-response` or `--map-local-file` instead of modifying an upstream response:

```bash
hp request --method GET --url "https://httpeep.com/api/welcome" \
  --inline-response "https://httpeep.com/api/welcome=200:application/json:{\"message\":\"Hello HTTPeep\"}"
```

> **Note:**
> If an attempted rule requires a plan-gated feature, report that limitation to the user before switching to an available alternative.
