# nutanix-aiops setup & security guide

> Currently validated against mocked v4 REST responses; see `docs/VERIFICATION.md`
> in the repo for the live-verification checklist.

## 1. Install

```bash
uv tool install nutanix-aiops          # or: pipx install nutanix-aiops
```

## 2. Prepare a Prism Central account (with REST API rights)

nutanix-aiops connects to **Prism Central** on HTTPS port **9440** and
authenticates the v4 REST APIs with **HTTP Basic auth** (username + password).

> **Important gotcha:** the account needs **REST API** rights, not just Web UI
> access. A user that can log into the Prism Central console may still be denied
> at the API. Give the account a role with the v4 API permissions it needs
> (read for the estate; the relevant lifecycle/VM/storage/DR permissions for any
> writes). `nutanix-aiops doctor` runs a REST-RBAC preflight to catch this early.

## 3. Onboard

```bash
nutanix-aiops init
```

The wizard collects the (non-secret) connection details into
`~/.nutanix-aiops/config.yaml` and stores the **password encrypted** into
`~/.nutanix-aiops/secrets.enc`. Example config:

```yaml
targets:
  - name: pc1
    host: 10.0.0.20        # Prism Central IP / FQDN
    port: 9440
    username: admin        # PC account with REST API rights
    verify_ssl: false      # self-signed lab / CE certs only
```

The `username` is not a secret and lives in the config file; the password lives
only in the encrypted store.

## 4. Non-interactive use (MCP server / CI / cron)

Export the master password so the encrypted store unlocks without a prompt:

```bash
export NUTANIX_AIOPS_MASTER_PASSWORD='your-master-password'
```

## Credential security

- The Prism Central password is **never** written to disk in plaintext. It lives
  only in `~/.nutanix-aiops/secrets.enc`, encrypted with Fernet (AES-128-CBC +
  HMAC), the key derived from your master password via scrypt. Only a per-store
  random salt and the ciphertext are on disk (chmod 600); the master password
  itself is never stored.
- A legacy plaintext env var `NUTANIX_<TARGET_NAME_UPPER>_PASSWORD` is still
  honoured as a fallback with a deprecation warning — migrate with
  `nutanix-aiops secret migrate`.
- The password is held only in memory during a session and is never logged or
  echoed; exception text and tracebacks are scrubbed of secret-shaped strings
  before being written to the audit log.

## Optional audit annotations

The skill does not decide whether a write is permitted — that is the agent's
judgement, or the permission of the account you connect it with (connect with
a Prism Central account holding only a read-only (Viewer) role, and writes
fail at the server). `NUTANIX_AUDIT_APPROVED_BY` / `NUTANIX_AUDIT_RATIONALE`
optionally annotate the audit row with who authorized a high-risk operation
and why — they are never required and never block a call:

```bash
export NUTANIX_AUDIT_APPROVED_BY='alice@example.com'
export NUTANIX_AUDIT_RATIONALE='Decommissioning migrated ESXi guest per CHG-1234'
```

## Governance harness state

State lives under `~/.nutanix-aiops/` (relocate with `NUTANIX_AIOPS_HOME`):

- `audit.db` — every tool call (SQLite), with risk tier and any approver/rationale supplied
- `undo.db` — inverse descriptors for reversible writes (e.g. `vm_update` prior
  CPU/memory, `vm_migrate` prior host)
- budget / runaway guard — caps cumulative tool calls and wall-time; trips on
  tight poll/retry loops

## Self-test for free (Community Edition)

You can validate end-to-end at no cost with **Nutanix Community Edition (CE)**:
a single-node CE cluster plus an **X-Small Prism Central** VM. Point a `pc1`
target at that PC on `:9440` and run the read tools; exercise the writes against
throwaway VMs / snapshots.

## Verify

```bash
nutanix-aiops doctor
```

`doctor` is the fastest live check — config, encrypted store + permissions, a
password per target, connectivity to Prism Central `:9440`, and the REST-RBAC
preflight.
</content>
