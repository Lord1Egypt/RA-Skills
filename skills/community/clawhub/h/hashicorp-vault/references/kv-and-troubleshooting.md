# KV and troubleshooting

## KV v1 vs KV v2

Use `vault kv` commands whenever possible. They hide path differences between KV versions.

- KV v1 often behaves like direct paths under a mount.
- KV v2 adds versioned data and metadata under the hood.
- `vault kv get secret/foo` is safer than manually guessing `/v1/secret/data/foo`.

Detect mounts:

```bash
vault secrets list -detailed
```

Look for the mount type and options to confirm KV version.

## Safe inspection commands

```bash
vault status
vault token lookup
vault auth list -detailed
vault secrets list -detailed
vault kv metadata get secret/my-app
vault kv get -format=json secret/my-app
```

## Local endpoint example

For a local lab Vault, a generic example is:

```bash
export VAULT_ADDR='http://192.168.1.101:8200'
```

Notes:
- Replace the example address with your actual Vault endpoint.
- If HTTPS fails with a TLS version or certificate error, verify whether the server is actually serving plain HTTP.
- If a hostname does not resolve, use a working IP or fix local DNS/mDNS.

## Useful write commands

```bash
vault kv put secret/my-app username=app password='s3cr3t'
vault kv patch secret/my-app password='rotated'
vault kv delete secret/my-app
vault kv undelete -versions=2 secret/my-app
```

## Common errors

### permission denied

Usually means the token or login method lacks policy access.

Check:

```bash
vault token lookup
vault policy read <policy-name>
```

### no value found / unsupported path

Usually means one of these:

- wrong mount name
- wrong KV version assumption
- wrong namespace
- secret does not exist

Check mounts and retry with `vault kv` commands.

### connection refused / x509 / tls errors

Usually means `VAULT_ADDR` is wrong, the server is down, or trust settings are incomplete.

Check:

```bash
echo "$VAULT_ADDR"
vault status
```

## Good habits

- Do read-only discovery first.
- Do prefer JSON output for automation.
- Do ask before writing secrets or policy changes.
- Do redact tokens and secret values from shared output.
- Do store policy files as `.hcl` when editing them locally.
