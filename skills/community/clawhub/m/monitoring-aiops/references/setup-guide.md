# monitoring-aiops setup & security guide

> Not yet validated against a live NOC (see `docs/VERIFICATION.md`). **PRTG's free
> perpetual 100-sensor Freeware edition (with the API) and an open-source
> Zabbix appliance (Docker compose) are the easiest live checks; SolarWinds is
> a 30-day trial only — mock-only past that, the largest verification debt.**

## 1. Install

```bash
uv tool install monitoring-aiops
```

## 2. Get a credential

- **SolarWinds Orion** — an Orion account (username + password) with the Orion
  API enabled. monitoring-aiops talks to SWIS REST + SWQL with **HTTP Basic
  auth** on port **17774** — the SWIS port since Orion 2023.1, which deprecated
  the old **17778** and slated it for removal. Leave `port` unset and a
  pre-2023.1 server is still reached: the first connection failure triggers one
  retry on 17778, and the port that answered is reused for that session. Set
  `port:` yourself and it is used verbatim, with no fallback probing.
- **PRTG** — an **API token** (Setup → Account Settings → API Keys, or a
  passhash). PRTG's web API is on port **443/8080**. A free Freeware edition
  (100 sensors, perpetual) exposes the same API — the easiest way to self-test.
- **Zabbix (6.x/7.x)** — an **API token** (Administration → API tokens; user
  tokens under User settings → API tokens). monitoring-aiops talks JSON-RPC 2.0
  to `/api_jsonrpc.php` on the frontend port (default **443**), sending the
  token as a `Bearer` header (6.4+/7.x) with an automatic legacy `auth`-field
  fallback for 6.0. Zabbix is fully open source — a Docker-compose appliance
  is a 10-minute self-test.

## 3. Onboard

```bash
monitoring-aiops init
```

The wizard asks, per target, for the **platform** (`solarwinds` / `prtg` /
`zabbix`), the **host**, the **port** (defaults 17774 for SolarWinds, 443 for
PRTG and Zabbix — accept the default and no `port:` key is written, so the
default keeps tracking the platform), the **Orion username** (SolarWinds only),
and the **secret**
— the Orion account password, the PRTG API token, or the Zabbix API token.
Non-secret connection details go to `~/.monitoring-aiops/config.yaml`; the
secret is stored **encrypted** into `~/.monitoring-aiops/secrets.enc`. Example
config (one config can span all NOCs):

```yaml
targets:
  - name: orion1
    platform: solarwinds
    host: 10.0.0.20
    # port omitted -> 17774 (Orion 2023.1+), falling back to 17778 once if
    # nothing answers. Set it here only to pin a non-standard SWIS port.
    username: admin
    verify_ssl: false          # self-signed lab certs only
  - name: prtg1
    platform: prtg
    host: 10.0.0.40
    port: 443
    verify_ssl: true
  - name: zbx1
    platform: zabbix
    host: 10.0.0.60
    port: 443
    verify_ssl: true
```

## 4. Non-interactive use (MCP server / CI / cron)

Export the master password so the encrypted store can be unlocked without a
prompt:

```bash
export MONITORING_AIOPS_MASTER_PASSWORD='your-master-password'
```

## Credential security

- The secret (Orion password / PRTG API token / Zabbix API token) is **never**
  written to disk in
  plaintext. It lives only in `~/.monitoring-aiops/secrets.enc`, encrypted with
  Fernet (AES-128-CBC + HMAC), the key derived from your master password via
  scrypt. Only a per-store random salt and the ciphertext are on disk (chmod
  600); the master password itself is never stored.
- A legacy plaintext env var `MONITORING_<TARGET_NAME_UPPER>_SECRET` is still
  honoured as a fallback with a deprecation warning — migrate with
  `monitoring-aiops secret migrate` (it imports then renames the old `.env`).
- The secret is used for HTTP Basic auth (SolarWinds) or as the PRTG / Zabbix
  API token at request time and held only in memory; it is never logged or
  echoed. Exception
  text and tracebacks are scrubbed of secret-shaped strings before being written
  to the audit log.

## Governance harness state

State lives under `~/.monitoring-aiops/` (relocate with `MONITORING_AIOPS_HOME`):

- `audit.db` — every tool call (SQLite), with risk tier, approver, rationale
- `undo.db` — inverse descriptors for reversible writes (mute→unmute,
  unmanage→remanage, pause→resume, zabbix create-maintenance→delete)
- budget / runaway guard — caps cumulative tool calls and wall-time; trips on
  tight poll/retry loops

## Governed writes

- **High-risk** ops (`unmanage_node`, `remove_node`,
  `zabbix_delete_maintenance`) use `dry_run` + double confirmation;
  `MONITORING_AUDIT_APPROVED_BY` / `MONITORING_AUDIT_RATIONALE` are optional
  audit annotations, recorded when set but never required.
- **Time-boxed** ops require an end time / duration: `mute_alerts`,
  `schedule_maintenance` (SolarWinds), `schedule_maintenance_prtg` (PRTG, in
  minutes), and `zabbix_create_maintenance` (Zabbix, in minutes). This prevents
  forgotten, indefinite suppression windows.

## Verify

```bash
monitoring-aiops doctor
```

`doctor` is platform-aware: it checks the config file, the encrypted store and
its permissions, that a secret is present per target, and (unless `--skip-auth`)
connectivity — a SWQL query for SolarWinds targets, `/api/status.json` for PRTG
targets, and for Zabbix targets the unauthenticated `apiinfo.version`
(reachability) followed by a cheap authed host count (token validity).
