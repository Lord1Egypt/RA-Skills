# Access — Integrations, Sharing, and OAuth

Every 404 in this API is an access question until proven otherwise. This file covers getting a token, what the token can reach, and how public integrations differ.

**Contents:** [Two Kinds of Integration](#two-kinds-of-integration) · [Internal Integration, End to End](#internal-integration-end-to-end) · [The Sharing Model Is the Permission Model](#the-sharing-model-is-the-permission-model) · [Capabilities](#capabilities) · [OAuth for a Public Integration](#oauth-for-a-public-integration) · [Token Handling](#token-handling) · [Diagnosing an Access Failure](#diagnosing-an-access-failure) · [Connection Audit](#connection-audit)

**Before answering "can it see X"**, read `## Integrations` in `~/Clawic/data/notion-api-integration/memory.md` — or `integrations.md` if the `## Boxes` index points there. Which parent pages are connected is the answer to most of these questions and is already written down.

## Two Kinds of Integration

| | Internal | Public (OAuth) |
|---|---|---|
| Who uses it | One workspace, the one that created it | Any workspace that installs it |
| Credential | A long-lived token from the integration settings page | An access token per workspace, obtained by authorization code exchange |
| Access granted by | A workspace member connecting pages to it | The user picking pages during the OAuth consent screen |
| Right choice for | Scripts, migrations, internal automation — almost everything | A product other people install |

`integration_type` in `config.yaml` decides which half of this file applies. Default is `internal`, because a one-workspace job that implements OAuth has bought a login screen it will never show anyone.

## Internal Integration, End to End

1. Create the integration in Notion's integration settings, scoped to the workspace, and select its capabilities (below).
2. Copy the internal token. It starts `ntn_` (newer) or `secret_` (older); both are workspace-wide credentials with the capabilities you selected.
3. Export it, never inline it: `export NOTION_API_KEY="…"`. In memory boxes it is written as `env:NOTION_API_KEY` and nothing else.
4. Connect the integration to the topmost page of each area it needs (below), not to individual pages.
5. Verify with the cheapest call in the API — it proves the token and the version header at once:

```bash
curl 'https://api.notion.com/v1/users/me' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

A bot user object comes back (`"type": "bot"`), carrying the integration's own name and owner. A 401 here is the token; a 400 here is the version header; anything else is not an auth problem.

Every subsequent request carries the same two headers, plus `Content-Type: application/json` on writes. `Notion-Version` is required on every call, not just the first (SKILL.md Rule 2).

## The Sharing Model Is the Permission Model

There is no role or scope system that grants access to a workspace. Access is per-object and inherited:

- An integration sees an object only if it, or one of its ancestors, has been connected to that integration (in the UI: the page's `···` menu → connections).
- **Children inherit.** Connect the parent page of a section and every database, page and block under it becomes reachable. This is the only pattern that stays complete as the workspace grows.
- **Moving a page moves its permissions.** Drag a database out of the connected subtree and the integration loses it — the code that worked yesterday returns 404 today and nothing in Notion warns you.
- Duplicating a connected page does not always carry the connection; a template duplicated by a user is a common source of "it works for my copy but not theirs".
- A workspace admin can revoke the integration entirely; that shows up as 401, not 404.
- Private pages of individual members are invisible unless that member connects them.

Record which parent pages are connected in `## Integrations` in `memory.md`. "What can this token reach" is otherwise answerable only by crawling.

## Capabilities

Selected on the integration, independent of which pages it can see. A capability the integration lacks fails at the endpoint even when the object is shared.

| Capability | Unlocks | Withhold when |
|---|---|---|
| Read content | Retrieve and query anything shared | Never — nothing works without it |
| Update content | Property and block updates, archiving | The job only reads; this alone removes most blast radius |
| Insert content | Creating pages and appending blocks | Same |
| Read comments | `GET /v1/comments` | Comments are not part of the job |
| Insert comments | `POST /v1/comments` | Same |
| Read user information (with or without email) | Names and emails on user objects and `people` properties | You only need ids — without this, user objects come back with the id and little else |

Least privilege here is cheap and real: an integration with read-only capabilities cannot be talked into a destructive write, whatever the code does. Note the capability set in `## Integrations`; a "403 or empty field" bug is often a capability that was never granted.

## OAuth for a Public Integration

Standard authorization code flow, with Notion-specific details worth knowing before writing it:

1. Send the user to Notion's authorization URL with `client_id`, `response_type=code`, `owner=user`, and your registered `redirect_uri`.
2. The consent screen is also a **page picker** — the user chooses which pages to grant. You cannot request "the whole workspace"; what they pick is what the token reaches.
3. Exchange the `code` at `POST /v1/oauth/token` with HTTP Basic auth of `client_id:client_secret`, body `grant_type=authorization_code`, the `code`, and the same `redirect_uri`. Codes are single-use and short-lived.
4. The response carries the `access_token`, plus `workspace_id`, `workspace_name`, `bot_id`, and `owner`. Store the token in your app's own secret store, keyed by `workspace_id` — one user can install into several workspaces, and treating the token as per-user is the classic multi-tenant bug.
5. `duplicated_template_id` appears when the install duplicated your template into the user's workspace: it is the id of their copy and the only handle you will get for it. Persist it at install time or lose it.
6. If the response includes a refresh token, implement refresh; if it does not, the access token is long-lived and the failure mode is revocation, which surfaces as 401.

Re-installing over an existing grant issues a new token and can widen or narrow the page selection — always overwrite the stored token and re-resolve ids after a reinstall, never merge.

**Never log the `code`, the `client_secret`, or the token.** In anything written down they are `<1password:Work/Notion/client-secret>` and `<keychain:notion-oauth>`.

## Token Handling

- One token per environment. A single token shared between a cron job and an interactive tool makes the ~3 req/s limit unpredictable and makes an audit meaningless.
- Rotation is manual: create the new token, deploy it, revoke the old one — in that order, since revocation is instant and mid-run 401s corrupt bulk jobs.
- Rotate on personnel change and on the recorded cadence in `## Due`. An internal token has no expiry, which is exactly why it gets forgotten.
- A leaked token is revoked in the integration settings, and revocation invalidates it everywhere immediately. Rotate first, investigate second.

## Diagnosing an Access Failure

| Symptom | Cause | Confirm |
|---|---|---|
| 401 on every call | Bad, revoked or rotated token; or `Bearer` prefix missing | `/v1/users/me` |
| 400 on every call | `Notion-Version` header absent or malformed | `/v1/users/me` with the header |
| 404 on one object, others fine | That object is outside the connected subtree | Open it in the UI and check its connections |
| 404 on everything after a reorganization | The connected parent moved or was replaced | Re-connect the new parent, then re-resolve ids |
| Object retrieves but write returns an error | Capability missing, not access | Capabilities table above |
| User objects have no email | "Read user information without email" was granted instead of the with-email variant | `/v1/users/me` owner field, then the integration settings |
| Works for you, 404 for a teammate's copy | Duplicated page did not inherit the connection | Connect the duplicate's ancestor |

## Connection Audit

Run on the `## Due` cadence, and after any workspace reorganization. There is no endpoint that lists "everything this integration can see", so the audit is: for each entry in `### Data Sources` in `memory.md`, retrieve it and record whether it still resolves.

- Anything that now 404s is either moved or disconnected — resolve which before deleting its row, because a moved data source keeps its id.
- Anything reachable that is *not* in the map is either new or was never recorded; add it.
- Record the audit date in `## Due` and any change in `## Integrations` and `### Data Sources` of `~/Clawic/data/notion-api-integration/memory.md`. An audit whose result is not written down gets re-run from zero next quarter.
