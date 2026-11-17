# olvm-aiops — Setup & security guide

## Prerequisites

- An Oracle Linux Virtualization Manager 4.5 or oVirt 4.5 engine, reachable over HTTPS.
- Python 3.11+ with [uv](https://docs.astral.sh/uv/) (`uv tool install olvm-aiops`), or `uvx`
  for the MCP server.
- An engine account. For read-only use, a user holding a read-only role such as
  `ReadOnlyAdmin` on the system or data center is enough, and keeps any change refused by the
  engine itself.

## 1. Know your username form

The username includes its authorization profile:

| Engine | Admin username |
|---|---|
| Keycloak enabled by engine-setup (the default since 4.5.1) | `admin@ovirt@internalsso` |
| Keycloak disabled, or an engine upgraded from before 4.5.1 | `admin@internal` |
| Directory users | `user@<profile>` as shown on the Administration Portal login page |

A wrong profile answers "Cannot authenticate user" from the engine's SSO service.

## 2. Get the engine CA

```bash
curl -o olvm-engine-ca.pem \
  'https://<engine-fqdn>/ovirt-engine/services/pki-resource?resource=ca-certificate&format=X509-PEM-CA'
```

Connect by the engine's FQDN. Its certificate is issued to that name; connecting by IP fails
verification with "IP address mismatch", which this tool reports as a TLS problem, not as an
unreachable engine.

## 3. Onboard

```bash
olvm-aiops init
```

The wizard asks for a master password (encrypts `secrets.enc`), then per target: name, engine
URL, username, CA file, whether to verify TLS, and the account password (hidden). It writes:

```yaml
targets:
  - name: engine1
    url: https://olvm-engine.example.com
    username: admin@ovirt@internalsso
    ca_file: /etc/pki/olvm-engine-ca.pem
    verify_ssl: true
```

Optional per target: `timeout` (seconds per request, default 30).

## 4. Verify

```bash
olvm-aiops doctor
```

Expect the engine product and version, e.g. "Connected to 'engine1' (…) as
admin@ovirt@internalsso — Oracle Linux Virtualization Manager 4.5.5-1.73.el9".

## Files & permissions

| Path | Content | Mode |
|---|---|---|
| `~/.olvm-aiops/config.yaml` | Non-secret connection details | 600 recommended |
| `~/.olvm-aiops/secrets.enc` | Encrypted passwords (Fernet + scrypt) | 600 (doctor warns otherwise) |
| `~/.olvm-aiops/audit.db` | Audit log of every call | user-only |
| `~/.olvm-aiops/undo.db` | Undo log (unused in this read-only release) | user-only |

Relocate everything with `OLVM_AIOPS_HOME`.

## Security notes

- The password is exchanged once per connection for an SSO token held only in memory; the token
  is revoked (`/ovirt-engine/services/sso-logout`) when the connection closes. The engine issues
  no refresh token, so an expired token is renewed by logging in again, once, on a 401.
- Neither the password nor the token is logged. SSO session ids that the engine prints in its
  login events are redacted before event text is returned.
- Only `https://` URLs are accepted: login sends the password in the request body.
- A login the engine refuses is not retried for 60 s, so a wrong password cannot lock the account
  through repeated calls.
- `verify_ssl: false` disables certificate checks entirely; use it only on a throwaway lab engine.
- The tool makes no outbound calls other than to the configured engine URL.
- This release has no write tools. Least privilege is still set on the engine account, which is
  the boundary that will keep holding once writes are added.

## MCP client setup

```bash
uvx --from olvm-aiops olvm-aiops-mcp
```

Put `OLVM_AIOPS_MASTER_PASSWORD` (and `OLVM_AIOPS_HOME` / `OLVM_AIOPS_CONFIG` if used) in the
client's `env` block: MCP clients do not inherit your shell profile.
