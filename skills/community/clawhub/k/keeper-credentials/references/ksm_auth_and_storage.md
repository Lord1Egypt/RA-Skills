# KSM authentication & cross-session persistence

How `keeper_creds.py` authenticates to the user's Keeper vault via **Keeper
Secrets Manager (KSM)** and keeps the agent logged in across sessions.

## Why KSM (and not OAuth / Commander)

Keeper has several developer surfaces with very different auth and blast radius:

| Surface | Auth | Access |
| --- | --- | --- |
| **Keeper Secrets Manager (KSM)** | One-Time Access Token → device config | Only records in shared folders granted to the KSM Application |
| Keeper Commander (CLI/SDK, REST Service Mode) | Authentication Flow V3: device approval / **SSO (SAML/OIDC)** + 2FA | The user's **entire vault** |
| Admin API / SCIM | Enterprise admin auth | Event logs, provisioning, compliance |

This skill uses **KSM** on purpose: it is the smallest-privilege way to let an
agent read *specific* stored credentials. The trade-off is that KSM is **not**
an OAuth/SSO flow — its "user completion" is the one-time token bootstrap, and
it cannot mint One-Time Shares (see `delivery_modes.md`). If you truly need an
OAuth/SSO browser login and full-vault access, that's a Commander integration,
a deliberately different and broader-access design.

## The bootstrap (token → config)

1. In the **Web Vault**: *Secrets Manager → create Application → share the
   folder(s) → Add Device → generate a One-Time Access Token* (e.g.
   `US:BASE64...`, where the prefix is the region/host).
2. `init` passes the token to the SDK:

   ```python
   from keeper_secrets_manager_core import SecretsManager
   from keeper_secrets_manager_core.storage import FileKeyValueStorage

   sm = SecretsManager(token="US:ONE_TIME_TOKEN",
                       config=FileKeyValueStorage("ksm-config.json"))
   sm.get_secrets([])   # first call binds the device + rewrites config
   ```
3. The SDK locally generates an EC key pair, registers the device, and writes
   `ksm-config.json` (hostname, client id, app key, private key). The **token
   is now spent** — one-time only.
4. Every later command loads the config and authenticates silently:

   ```python
   sm = SecretsManager(config=FileKeyValueStorage("ksm-config.json"))
   ```

`init` is the single step that needs a human, and only because the user must
choose what to share and generate the token in their vault.

## Storage

- The config lives in `KEEPER_SKILL_HOME` (default
  `~/.config/keeper-credentials`), written `0600` in a `0700` dir.
- **It must persist across sessions.** The skill can't make storage durable
  by itself — the host must. On containerized/remote agents, point
  `KEEPER_SKILL_HOME` at a mounted volume / synced secret dir that outlives the
  ephemeral container, and run `init` once. Subsequent sessions mounting the
  same path are silent.

| File | Sensitivity |
| --- | --- |
| `ksm-config.json` | **High** — the bound device key; grants scoped read/write to the shared folders. `0600`. |

## Reading records

- `sm.get_secrets([])` → all accessible records; `sm.get_secrets([uid])` → one.
- `sm.get_secret_by_title("title")` → first exact-title match.
- `record.field("password", single=True)` → a standard field value.
- `record.custom_field("name")` → a custom field.
- `sm.get_notation("keeper://UID/field/password")` → value via Keeper Notation.
- `record.dict` → the raw record; the skill reads only field **labels** from it
  for `list`, never values.

## Re-auth

If the user removes the Application or unshares the folder, calls fail. `status`
surfaces this as `reauth_required` (exit code 2). The fix is to re-run the
bootstrap with a fresh token — there is no silent workaround, by design.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Success. |
| 2 | Needs the human bootstrap (`not_authenticated` / `reauth_required` / `missing_token`). |
| 1 | Other error (not found, SDK missing, field/notation/share error). |
