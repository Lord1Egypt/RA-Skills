---
name: hashicorp-vault
description: Work with HashiCorp Vault using the `vault` CLI for authentication checks, KV secret reads and writes, listing paths, enabling and tuning secrets engines, policy inspection, token lookup, and operational troubleshooting. Use when tasks mention HashiCorp Vault, Vault KV, secret paths like `secret/` or `kv/`, `VAULT_ADDR`, `VAULT_TOKEN`, AppRole, policies, mounts, or the `vault` command.
metadata:
  {
    "openclaw":
      {
        "emoji": "🏦",
        "requires": { "bins": ["vault"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "hashicorp/tap/vault",
              "bins": ["vault"],
              "label": "Install HashiCorp Vault CLI (brew)",
            },
            {
              "id": "apt",
              "kind": "apt",
              "package": "vault",
              "bins": ["vault"],
              "label": "Install HashiCorp Vault CLI (apt)",
            },
            {
              "id": "manual-download",
              "kind": "manual",
              "url": "https://releases.hashicorp.com/vault/",
              "label": "Download Vault CLI from HashiCorp releases",
            },
          ],
      },
  }
---

# HashiCorp Vault CLI

Use the `vault` CLI for Vault work. Prefer read-only inspection first, then confirm before writing secrets, changing auth methods, enabling engines, or editing policies.

## Quick checks

```bash
vault version
vault status
vault auth list
vault secrets list
vault token lookup
```

If `VAULT_ADDR` is missing, set it first:

```bash
export VAULT_ADDR='https://vault.example.com'
```

For a local lab Vault, an example endpoint is:

```bash
export VAULT_ADDR='http://192.168.1.101:8200'
vault status
curl -s "$VAULT_ADDR/v1/sys/health"
```

Notes:
- Replace the example address with your actual Vault endpoint.
- Some local test deployments use plain HTTP instead of HTTPS.
- Prefer reading tokens from a local file or environment variable instead of echoing them in chat.

Verify auth before assuming a path is missing:

```bash
vault token lookup
vault kv get secret/my-app
```

## Read secrets

For KV v2 paths, use `vault kv` commands instead of raw API-style paths.

```bash
vault kv get secret/my-app
vault kv get -field=password secret/my-app
vault kv list secret/
```

If output is unclear, use JSON:

```bash
vault kv get -format=json secret/my-app
vault secrets list -format=json
```

## Helper scripts

This skill includes simple wrappers that auto-load local settings:

```bash
{baseDir}/scripts/vault-list.sh secret/openclaw
{baseDir}/scripts/vault-get.sh secret/openclaw/openclaw-test
{baseDir}/scripts/vault-put.sh secret/openclaw/demo status=ok source=openclaw
```

Behavior:
- Defaults `VAULT_ADDR` to `http://192.168.1.101:8200`
- Loads `VAULT_TOKEN` from `~/.vault-token` if not already exported
- Uses `vault kv` commands for the common KV v2 workflow

## Write secrets

Confirm before overwriting or deleting anything.

```bash
vault kv put secret/my-app username=app password='s3cr3t'
vault kv patch secret/my-app password='rotated'
```

Prefer `patch` when updating a subset of keys on KV v2.

## Policies and mounts

Inspect first:

```bash
vault policy list
vault policy read my-policy
vault secrets list -detailed
```

Change only with explicit user intent:

```bash
vault policy write my-policy ./policy.hcl
vault secrets enable -path=secret kv-v2
vault secrets tune -max-versions=10 secret/
```

## Authentication helpers

Common login flows:

```bash
vault login
vault login -method=userpass username=<user>
vault write auth/approle/login role_id=<role_id> secret_id=<secret_id>
```

When troubleshooting auth, inspect enabled auth backends and token details first:

```bash
vault auth list -detailed
vault token lookup
```

## Troubleshooting workflow

1. Check `vault status` and `VAULT_ADDR`.
2. Check auth with `vault token lookup` or the intended login flow.
3. Confirm mount names with `vault secrets list`.
4. For KV access, verify whether the engine is KV v1 or KV v2 before choosing commands.
5. Prefer `-format=json` when output will be parsed or compared.
6. Read `references/kv-and-troubleshooting.md` for command patterns and common errors when the task is non-trivial.
