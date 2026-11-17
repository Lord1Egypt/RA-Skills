---
name: oo-kingdee
description: "Kingdee (kingdee.com). Use this skill for ANY Kingdee request — reading, creating, updating, and deleting data. Whenever a task involves Kingdee, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Kingdee"
  author: "OOMOL"
  version: "1.1.3"
  services: ["kingdee"]
  icon: "https://static.oomol.com/logo/third-party/kingdee.svg"
---

# Kingdee

Operate **Kingdee** through your OOMOL-connected account. This skill calls the `kingdee` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Kingdee. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "kingdee" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "kingdee" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

### Choose the route

- Use a foundation action from the action index below whenever it covers the requested operation. These actions work across business objects through `formId`; a different object alone is not a reason to use proxy.
- If the object's FormId or business fields are unknown, search the bundled index and inspect the official operation contract, then return to the matching action.
- Use proxy only for a documented operation that no foundation action covers, such as a form-specific general operation or custom business service. Never invent an endpoint from a Chinese operation name.
- This skill covers Kingdee Galaxy Enterprise (金蝶星空企业版). State the scope mismatch before trying these endpoints for another Kingdee product family.

Foundation actions accept `{ "formId": "...", "data": { ... } }`. Preserve official business-field casing inside `data`; Connector serializes it internally. `Model` fields and object-specific keys come from the selected object's documentation, not its Chinese display name.

```bash
oo connector schema "kingdee" --action "query_records"
oo connector run "kingdee" \
  --action "query_records" \
  --data '{"formId":"SAL_SaleOrder","data":{"FieldKeys":"FID,FBillNo","StartRow":0,"Limit":20}}' \
  --json
```

Queries return `rows` and `fieldKeys`; views return `record` and `result`; reports return `result`. Mutations return `success`, `partialSuccess`, `errors`, `successfulEntities`, and `result`. Inspect these fields before reporting completion. Never repeat an entire partially successful batch without identifying which items failed.

### Find an object or long-tail operation

1. Search [references/api-index.jsonl](references/api-index.jsonl) by the user's business-object name. Resolve the path relative to this installed skill directory, not the user's project:

   ```bash
   rg -n -F '"object":"应收调汇单"' references/api-index.jsonl
   ```

   If an exact search misses, use a shorter Chinese keyword and compare the returned `domain`, `module`, and `object`. Do not read the entire index into context or select the first ambiguous match.

2. Select an operation present in the chosen row's `operations`. Preserve `apiInfoId` and `catalogNodeId` as strings; neither is a FormId. If the operation is absent, report the gap.
3. Read [references/proxy-reference.md](references/proxy-reference.md). Fetch the selected operation's official detail first, then only the request fields, response fields, or examples needed for the task. Verify object identity, operation code, and version.
4. Return to a foundation action when it covers the operation. Otherwise follow the reference's standard, special, or general-operation request rule and separately verify any custom service URL.
5. Write the complete proxy request to `proxy-request.json`, then execute only the authorized operation:

   ```bash
   oo connector proxy "kingdee" --data @proxy-request.json --json
   ```

   The file contains `endpoint`, `method`, and the upstream `body`; it is not an action input. In the named-parameter format, serialize inner `body.data` exactly once.

6. For proxy results, inspect `response.data.status` and then `response.data.data`. CLI success or HTTP 200 alone does not prove business success.

The bundled index is a 2026-09-15 snapshot with 1,076 object rows and 7,881 unique operation IDs. It helps discovery but does not prove that an operation is enabled in the user's instance. Stop and resolve any identity or version conflict with current official documentation.

## Available actions

- `allocate_records` — Allocate master data to target organizations. [write]
- `audit_records` — Approve records through the audit operation. [write]
- `batch_save_records` — Save multiple records, including updates, and preserve partial results. [destructive]
- `delete_records` — Delete records by internal IDs or numbers. [destructive]
- `draft_record` — Save a draft, including changes to an existing draft. [destructive]
- `get_record` — View a record by its internal ID or number.
- `push_records` — Convert source records or entries into target records using a conversion rule. [write]
- `query_records` — Query business records by fields, filters and row offset.
- `query_report` — Query a report using its form-specific filters.
- `save_record` — Save a record, including updates to existing records. [destructive]
- `submit_records` — Submit records for approval. [write]
- `unaudit_records` — Reverse the audit status of records. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Kingdee state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**
- Classify proxy calls by the documented business effect, not the HTTP method. A POST can query, approve, or delete; resolve an unclear effect before execution.
- Each action or proxy call gets a fresh login session. `SwitchOrg` does not affect a later call; use documented per-operation organization fields. Organization IDs are distinct from data-center IDs.
- A timed-out or interrupted write may already have completed. Do not retry automatically; reconcile state with known record identifiers first.
- Keep documentation requests anonymous. Never send enterprise credentials to the documentation host or use proxy to call login endpoints.
- Real enterprise end-to-end behavior has not been validated by the skill's authoring checks. Claim success only from the current tenant's result.

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Kingdee is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/kingdee
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

- **Ambiguous HTTP 401/403 or business error** — preserve the upstream error as reported; do not conclude that the application secret expired unless the response contains a documented credential signal.
- **Official operation documentation unavailable** — report the missing contract. Do not guess fields, enumerate documentation IDs, or fetch every operation.

## Resources

- Kingdee homepage: https://www.kingdee.com/cn
- API documentation: https://open.kingdee.com/K3Cloud/Open/ApiCenterReportDetail.aspx
- [Business operation index](references/api-index.jsonl) — search this when identifying an object or operation.
- [Documentation lookup, proxy formatting, and result handling](references/proxy-reference.md) — read this before proxy execution.
- [Official third-party authorization setup](https://open.kingdee.com/K3Cloud/Open/ApiCenterReportDetail.aspx)
