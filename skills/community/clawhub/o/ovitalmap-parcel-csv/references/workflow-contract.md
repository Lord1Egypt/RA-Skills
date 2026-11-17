# Workflow Contract

Every pipeline response contains:

```text
status: needs_input | ready | completed | blocked
next_action: machine-readable next step
required_input: exact missing confirmations or values
message: concise user-facing summary
result: structured evidence and file paths
```

## Agent behavior

- `needs_input`: show the message and relevant coordinate or code preview, ask only for `required_input`, and stop.
- `ready`: report the result and perform `next_action` when it requires no new user decision.
- `completed`: deliver every item in `result.exports` in order and give the appropriate OvitalMap import instruction.
- `blocked`: explain the message, make no success claim, and wait for corrected input or retry safely.

Respond in the user's language. Do not expose run state or raw JSON unless the user asks for technical details.

## Confirmation gates

The pipeline must not pass these gates implicitly:

- `confirmed_coordinates`: the user verified the displayed WGS84 vertices.
- `country_code`: the country or region is known rather than guessed.
- `provider_resolutions.{parcel_ref}`: a missing or ambiguous provider is resolved per parcel.
- `duplicate_resolutions.{parcel_ref}`: identical submitted boundaries are confirmed as `same` or `different`.
- `official_id_resolutions.{parcel_ref}`: duplicate official identifiers are corrected or cleared.
- `confirmed_codes`: the user approved generated parcel codes before Step 3.
- `auto_accept_codes`: explicit permission for non-interactive `--step all`.

`export_mode` is not a confirmation gate. It defaults to `boundary` and must remain unchanged throughout a run unless the user explicitly requests another mode.

Use stable parcel references in decisions:

```json
{"provider_resolutions":{"P01":"Survey Team"},"duplicate_resolutions":{"P02":"different"}}
```

Use `parcel_ref` keys for every per-parcel decision.
