# Account provisioning

Reach is **explicitly authorized** to register accounts at any source listed in `scripts/sources.yml` whose `account` field is `required` or `optional`. Use the persona below for every registration; do not reuse the user's personal accounts.

## Authorized identity

| Field | Value |
|---|---|
| Name | <agent-name> |
| Email | `<agent-email>` |
| Organization | OpenClaw Agent Suite (OCAS) |
| Stated use case | "Personal AI assistant queries; non-commercial; rate-respectful" |

For sources that require a website / project URL, use `https://github.com/<agent-handle>`.

## Registration playbook (when an action returns `auth_required`)

1. **Confirm the source's `account_url`** in `sources.yml` (or the index).
2. **Open the registration form** in the agent's browser session (claude-in-chrome MCP, NEVER computer-use clicks on a tier-`read` browser).
3. **Submit** with the authorized identity above. If a usage / project description is requested, use the canonical wording in `account_url` rows of the index, or write one or two sentences describing OCAS as a personal AI assistant.
4. **Verify the account email** if the source sends a confirmation message — check Gmail via the `dispatch` skill or a direct read.
5. **Capture the issued credential.** Most sources show the API key once on success. Some email it.
6. **Store the key in `~/.hermes/.env`** under the env var declared in `sources.yml` for that source. One key per line, no quotes:

   ```
   FRED_KEY=abcdef0123456789abcdef0123456789
   ```
7. **Append a ledger entry** to `{agent_root}/commons/data/ocas-reach/accounts.json` (see schema below).
8. **Write an Action Journal** at `{agent_root}/commons/journals/ocas-reach/YYYY-MM-DD/{run_id}.json` describing the registration. Set `kind: action` (not `observation`) — registration is a side effect.
9. **Notify the user once** by including a single line in the next briefing or status response: "Registered Reach account at <source> (key stored in `~/.hermes/.env`)."
10. **Verify the credential works** by issuing one cheap query (`reach.py query <source> <action>` for the lowest-cost action). If the call fails with auth-related status, re-check the env var name + value.

## Ledger schema

`{agent_root}/commons/data/ocas-reach/accounts.json`:

```json
{
  "accounts": [
    {
      "source": "fred",
      "account_email": "<agent-email>",
      "registered_at": "2026-04-26T18:00:00Z",
      "env_var": "FRED_KEY",
      "key_set_at": "2026-04-26T18:01:30Z",
      "plan_tier": "free",
      "verified_call": "2026-04-26T18:02:15Z",
      "notes": "120 req/min; no monthly cap"
    }
  ]
}
```

Rules:

- **One entry per source.** If a key is rotated, update `key_set_at` and add a `rotated_from` field with the previous timestamp; do not create a duplicate row.
- **Never put the key value in the ledger.** The ledger records existence and metadata; the secret lives only in `~/.hermes/.env`.
- **`verified_call`** must be set after the post-registration smoke call succeeds. If the smoke call fails, leave it null and surface an error to the user — do not pretend the account is live.

## What Reach is NOT authorized to do

- Pay for a paid tier or upgrade plan, even if a free trial is offered. If a feature requires payment, surface it to the user and stop.
- Use the user's personal email or any other identity besides `<agent-email>`.
- Register at sources outside `sources.yml`. New sources go through the "Adding a new source" workflow first (registry update + reference doc + version bump), THEN registration.
- Solve billing-related captchas (most registration captchas are fine; billing flows are a hard stop).
- Accept ToS that include arbitration waivers, exclusivity clauses, or anything beyond standard non-commercial API usage. If unclear, defer to the user.

## What to do if the registration is blocked

If a source requires phone verification, ID upload, or a captcha that fails repeatedly:

1. Stop. Do not retry more than twice.
2. Write a journal entry with `outcome: registration_blocked` describing the block.
3. Surface to the user with: source name, what blocked it, and a link to the registration page so they can complete it themselves.

## Audit

To list all currently registered accounts:

```bash
python3 scripts/reach.py source <name>      # shows quota + auth state for one
python3 scripts/reach.py sources            # full registry overview
cat {agent_root}/commons/data/ocas-reach/accounts.json
```

To check which env vars are missing on the host:

```bash
for src in $(jq -r '.sources[].name' < <(python3 scripts/reach.py sources)); do
  env=$(python3 -c "import yaml; print((yaml.safe_load(open('scripts/sources.yml'))['sources'].get('$src') or {}).get('env_var', ''))")
  [ -n "$env" ] && [ -z "${!env}" ] && echo "$src: missing $env"
done
```
