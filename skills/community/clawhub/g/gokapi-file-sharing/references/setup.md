# First-use setup

OpenClaw skill installation does not ask custom setup questions. On first invocation, obtain the base URL from the owner unless a valid local binding is already present. The URL may be supplied in the conversation; the API key must not be.

For a new URL, validate HTTPS with no userinfo, query, or fragment. Save it as an `env`-kind store entry using `openclaw secrets store set GOKAPI_BASE_URL --kind env --value-file -` and bind that entry to `skills.entries.gokapi-file-sharing.apiKey` with `openclaw config set skills.entries.gokapi-file-sharing.apiKey --ref-source store --ref-provider <local-store-provider-alias> --ref-id GOKAPI_BASE_URL`. Use the actual store-provider alias from the local configuration; do not assume an alias from another OpenClaw installation. `apiKey` here is OpenClaw's generic skill-injection field, not the Gokapi API key.

Prefer OpenClaw's masked secret prompt for `GOKAPI_API_KEY` with `--allow-host` set to the exact hostname from the validated URL. If that prompt cannot connect to a Control UI, use a local shell with masked input; do not copy the key into chat, command arguments, environment variables, or a file. This Python standard-library snippet sends it only over stdin to the store CLI:

```python
import getpass
import subprocess

host = input("Gokapi hostname (without scheme): ").strip().lower()
if not host or "/" in host or "@" in host or ":" in host:
    raise SystemExit("Enter only the exact hostname of the configured HTTPS URL")
key = getpass.getpass("Gokapi API key: ")
if not key:
    raise SystemExit("API key is required")
subprocess.run(
    ["openclaw", "secrets", "store", "set", "GOKAPI_API_KEY", "--kind", "secret", "--allow-host", host, "--value-file", "-"],
    input=key,
    text=True,
    check=True,
)
```

Verify the store entries and URL binding by metadata, then perform a read-only authenticated API check through Gateway secret egress. Do not print the key or a populated secret field. If the CLI store is not available on that host, ask the owner to make the Control UI reachable and retry the protected prompt; do not fall back to chat.
