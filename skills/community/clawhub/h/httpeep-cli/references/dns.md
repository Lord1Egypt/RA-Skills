<!-- GENERATED FILE: DO NOT EDIT DIRECTLY. -->
<!-- Source of truth: docs.httpeep.com/content/docs/cli/dns.mdx -->
<!-- Generate with: node scripts/generate-httpeep-cli-skill-reference.mjs <references-dir> -->

# DNS

The `dns` command manages HTTPeep DNS Override settings from the terminal. Use it to redirect a production hostname to a local or staging IP, switch between DNS environments, or export the current DNS configuration for automation.

```bash
# `hp` is the short alias for `httpeep-cli`
hp dns list
httpeep-cli dns list
```

DNS Override only affects traffic routed through HTTPeep. It does not edit `/etc/hosts`, does not require system-wide DNS changes, and can be toggled without restarting the proxy.

> **Note:**
> Global DNS host entries are available to all users. Environment-scoped DNS groups and active environment switching require Pro entitlement.

## Command overview

| Command | Purpose |
|---|---|
| `dns list` | Show the full DNS Override configuration |
| `dns enable` / `dns disable` | Toggle DNS Override resolution globally |
| `dns replace` | Replace the full DNS configuration from JSON or YAML |
| `dns upsert` | Create or update a host mapping (global or environment-scoped) |
| `dns global-host list` | List global host mappings |
| `dns global-host delete` | Delete one global host mapping |
| `dns env list` | List environment groups |
| `dns env upsert` | Create or replace one environment group |
| `dns env delete` | Delete one environment group |
| `dns env-host list` | List host mappings in an environment |
| `dns env-host delete` | Delete one environment-scoped mapping |
| `dns active-env set` | Select the active environment |

## Mental model

DNS Override has three layers:

1. **Global switch** — `enabled` turns DNS Override on or off.
2. **Environment hosts** — mappings under the selected `activeEnv`.
3. **Global hosts** — fallback mappings that apply regardless of environment.

When a host exists in both the active environment and `globalHosts`, the environment mapping wins. Exact host matches are evaluated before wildcard matches.

## Add host mappings

`dns upsert` creates or updates a host mapping. Omit `--env` for global mappings; pass `--env <name>` for environment-scoped mappings.

```bash
# Global mapping — applies regardless of active environment
hp dns upsert \
  --domain api.example.com \
  --ip 127.0.0.1

# Wildcard global mapping
hp dns upsert \
  --domain "*.internal.example.com" \
  --ip 10.0.0.5

# Environment-scoped mapping
hp dns upsert \
  --env dev \
  --domain api.example.com \
  --ip 127.0.0.1

# Disable a mapping without deleting it
hp dns upsert \
  --domain api.example.com \
  --ip 127.0.0.1 \
  --enabled false
```

List or delete mappings:

```bash
hp dns global-host list
hp dns global-host delete --pattern api.example.com
hp dns env-host list --env dev
hp dns env-host delete --env dev --pattern api.example.com
```

> **Note:**
> `global-host` and `env-host` subcommands remain available for listing and deleting. Prefer `dns upsert` for creating and updating entries.

## Toggle DNS Override

Use `enable` and `disable` to control whether DNS Override participates in resolution.

```bash
hp dns disable
hp dns enable
```

This only changes the global switch. Existing host mappings remain stored and can be re-enabled later.

## Use environment groups

Environment groups let you switch between dev, staging, and production mappings without editing each host one by one.

Create an empty environment:

```bash
hp dns env upsert --name dev
```

Add host entries to it:

```bash
hp dns upsert \
  --env dev \
  --domain api.example.com \
  --ip 127.0.0.1

hp dns upsert \
  --env staging \
  --domain api.example.com \
  --ip 10.0.1.50
```

Activate an environment:

```bash
hp dns active-env set --name dev
```

List and delete environment entries:

```bash
hp dns env list
hp dns env-host list --env dev
hp dns env-host delete --env dev --pattern api.example.com
hp dns env delete --name staging
```

> **Tip:**
> `dns active-env set --name <env>` creates the environment if it does not already exist. This makes environment switching convenient in scripts.

## Replace the full config

Use `dns replace` when you want to apply a complete DNS configuration from a checked-in file.

```yaml title="dns.yaml"
enabled: true
activeEnv: dev
globalHosts:
  internal-tool.example.com:
    ip: 10.0.0.5
    enabled: true
environments:
  dev:
    hosts:
      api.example.com:
        ip: 127.0.0.1
        enabled: true
      "*.dev.example.com":
        ip: 127.0.0.1
        enabled: true
  staging:
    hosts:
      api.example.com:
        ip: 10.0.1.50
        enabled: true
```

Apply it:

```bash
hp dns replace --file ./dns.yaml
```

`dns replace` accepts JSON or YAML. Pass `-` to read from stdin:

```bash
cat ./dns.yaml | hp dns replace --file -
```

You can also replace a single environment with `dns env upsert --file`:

```yaml title="dev-dns.yaml"
hosts:
  api.example.com:
    ip: 127.0.0.1
    enabled: true
  auth.example.com:
    ip: 127.0.0.1
    enabled: true
```

```bash
hp dns env upsert --name dev --file ./dev-dns.yaml
```

## JSON output

Use `--format json` for scripts and `jq` pipelines:

```bash
hp --format json dns list
hp --format json dns global-host list
hp --format json dns env-host list --env dev
```

Example: list only enabled global host mappings.

```bash
hp --format json dns global-host list | \
  jq 'to_entries[] | select(.value.enabled) | "\(.key) -> \(.value.ip)"'
```

## Common workflows

### Route a production API to localhost

```bash
hp dns upsert \
  --domain api.myapp.com \
  --ip 127.0.0.1

hp dns enable
```

### Switch a test run to staging DNS

```bash
hp dns env upsert --name staging
hp dns upsert \
  --env staging \
  --domain api.myapp.com \
  --ip 10.0.1.50
hp dns active-env set --name staging
```

### Keep team DNS mappings in source control

```bash
hp --format json dns list > httpeep-dns.json
hp dns replace --file ./httpeep-dns.json
```

> **Warning:**
> DNS Override is applied by HTTPeep's proxy runtime. Applications that bypass the proxy or use their own resolver will not be affected by these mappings.
