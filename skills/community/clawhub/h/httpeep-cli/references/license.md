<!-- GENERATED FILE: DO NOT EDIT DIRECTLY. -->
<!-- Source of truth: docs.httpeep.com/content/docs/cli/license.mdx -->
<!-- Generate with: node scripts/generate-httpeep-cli-skill-reference.mjs <references-dir> -->

# License

`hp license` manages license activation and status checks from the terminal.

`hp` is the short alias for `httpeep-cli`; both command names work the same way.

## license activate

Activate a license key on the current machine.

```bash
hp license activate --key <license-key>
```

The command validates the key, stores the local license state, and refreshes CLI entitlements used by gated features.

Use JSON output when automating activation in setup scripts:

```bash
hp --format json license activate --key <license-key>
```

The JSON response includes whether activation produced a Pro runtime, the evaluated license runtime, and the synced entitlement state.

## license status

Show the current license runtime state.

```bash
hp license status
```

Human output includes the plan, reason, local blob state, signature status, machine match status, hash match status, and relevant expiry timestamps.

Use JSON output for automation:

```bash
hp --format json license status
```

The JSON response includes:

| Field | Description |
|---|---|
| `runtime` | Current license runtime evaluation |
| `entitlements` | CLI entitlement state synced from the runtime |

Example CI check:

```bash
hp --format json license status | jq -e '.runtime.plan == "Pro"'
```

> **Note:**
> The frontend does not decide feature access by itself. License and entitlement checks are evaluated by the Rust runtime and reused by the CLI.
