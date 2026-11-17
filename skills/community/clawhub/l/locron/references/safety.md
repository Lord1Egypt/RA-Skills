# Locron 0.5–0.8 safety model

Use this reference for operations whose consequences depend on mutation support, policy, or durable state. Confirm the installed help before using any command. The mutation boundaries below are verified through Locron 0.8.0; `explain` is available from 0.6.0 and the local dashboard from 0.8.0.

## Mutation boundary

The following mutations support a non-mutating `--dry-run` in Locron 0.5.0 through 0.8.0:

- `add`, `update`, and `run`
- `import` and `prune`
- `config set` and `config unset`

Run the complete proposed command with `--dry-run --format json` first. A successful dry-run validates or simulates; it does not authorize or apply the change.

The following operational mutations have no dry-run:

- `enable`, `disable`, and `remove`
- `cancel`
- `service install` and `service uninstall`
- `dashboard enable`, `dashboard disable`, and token rotation through `dashboard enable --reset`

For these, read the exact target immediately before acting and require authorization in the current request. `cancel --acknowledge-unconfirmed` is a separate risk acceptance, not a routine retry flag.

Dashboard token display is read-only but sensitive. Prefer `dashboard status` for ordinary inspection because it reports token presence and permission posture without the secret. Use `dashboard token` only when the user needs to authenticate locally, never put the token in a URL, and treat `dashboard enable --reset` as deliberate credential rotation that invalidates existing sessions. The dashboard is loopback-only by contract; proxying or tunnelling it changes the exposure boundary and is not an ordinary dashboard operation.

## Schedule and policy facts

- A job has exactly one cron, interval, or one-time schedule.
- Cron uses a `local` or IANA timezone. An interval uses a durable anchor. A one-time timestamp contains its own explicit offset.
- A manual run does not move the schedule or its next occurrence.
- Overlap policies are `skip`, `replace`, and `allow`. None bypasses global or per-job concurrency admission.
- Missed-run policies are `skip`, `latest`, and bounded `all`. A start deadline may exclude old occurrences.
- The daemon records durable occurrence and reconciliation facts but does not directly detect machine sleep.
- Queued, started, succeeded, failed, skipped, cancelled, interrupted, and termination-unconfirmed states are materially different. Use `why --run` rather than inferring the outcome from a queue acknowledgement or log fragment.

## Target and value safety

- Direct process targets pass argv without shell evaluation and are the default choice.
- Shell targets enable shell parsing and should reflect an explicit need for shell semantics.
- Process, shell, and HTTP targets can all produce external side effects when a real run executes.
- Inline environment values, HTTP headers, and bodies can contain secrets. Locron redacts configured values in ordinary observation, but explicit plaintext export/import flags cross that protection boundary.
- An imported definition can schedule arbitrary commands or HTTP requests. Inspect its dry-run plan, target, enabled state, policy, and plaintext-value requirements before application.

## Diagnostic evidence order

Use service state and `doctor` for availability, `why <job>` for job eligibility, `history` to find a canonical run, `why --run` for durable run decisions, and `logs` for target output. Preserve Locron warnings and keep a distinction between stored evidence, target output, and your own inference.
