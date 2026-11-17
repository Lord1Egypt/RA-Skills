---
name: outlook-mailbox
description: App-only Graph access to a few Exchange Online mailboxes, not the whole tenant. RBAC scope, 403 test, call list. Use when an agent reads Outlook mail. Trigger on "outlook mailbox".
metadata: {"clawdbot":{"emoji":"📬","requires":{"bins":["pwsh","python3","curl"]},"homepage":"https://learn.microsoft.com/en-us/exchange/permissions-exo/application-rbac"}}
---

# Outlook Mailbox Access (app-only, scoped)

A scoped mailbox grant is an Exchange object, not an Entra consent. Consent `Mail.*` in Entra and the scope stops scoping anything, with no error and no warning.

## Personal Data: Settle This Before Any Setup

Mailbox content is personal data about the mailbox owner **and** about every correspondent. Nothing below runs until each line has an answer the data controller signed off on.

| Item | Minimum required | Stop if |
|---|---|---|
| Lawful basis | Written basis per purpose (e.g. GDPR Art. 6(1)(b) contract or 6(1)(f) legitimate interest with a balancing test). Employee mailboxes usually need a DPIA (Art. 35) and, depending on the country, staff-representative consultation | No named controller, or purpose is "general monitoring" |
| Minimization: mailboxes | Explicit list of addresses, one purpose each. One shared relay/test mailbox inside, one mailbox deliberately **outside** for the negative test | List is "everyone", or a dynamic rule |
| Minimization: folders | Only the folders the purpose needs (usually `inbox`). Delta is per folder, so this is enforced by which folders you poll | Recursive crawl of all folders |
| Minimization: fields | Smallest role that works: `Mail.ReadBasic` (no body, no attachments) < `Mail.Read` < `Mail.ReadWrite` (drafts). Fixed `$select` list | Body or attachment bytes pulled "to see" |
| Retention | Store Graph ids + metadata, re-read on demand. No mail body persisted. Local attachment copies purged when the task closes. Numbers live in config, e.g. working notes 30 days | No purge job exists |
| Logging | Audit line per action: timestamp, mailbox, message id, action, result. Never subject, body, or names | Log contains content |
| Information | Mailbox owners told in writing what the agent reads, drafts, keeps, and for how long; privacy notice updated for correspondents | Owners not informed |
| Special categories / secrecy | Art. 9 data (health, union…), Art. 10 data, or mail under professional secrecy: pseudonymize before any model prompt, human review on every output | No pseudonymization step |

The agent itself should hold **no Graph credential**. Deterministic scripts hold the certificate, run the calls through the allowlist below, and hand the agent pre-filtered files.

## When to Use

| Trigger | Action |
|---|---|
| "let the agent read these 5 mailboxes" | Full sequence: data table, Setup, Prove, Allowlist |
| "graph app-only mail access", "restrict app to some mailboxes" | Setup → Prove |
| "the app can still read the CEO's mailbox" | Union trap: remove Entra consent, re-test |
| "ApplicationAccessPolicy", "New-ApplicationAccessPolicy" | Do not create one. Migrate to RBAC for Applications |
| "delta stopped returning mail", `syncStateNotFound`, `410` | Delta rules → full resync + alert |
| "429 from Graph on one mailbox" | Throttling table |
| "agent should draft replies" | `createReply` + PATCH rules, never send |

## Placeholders

| Placeholder | Meaning | Example (fictional) |
|---|---|---|
| `<APP_ID>` | Application (client) ID, from **Enterprise applications** | `11111111-2222-4333-8444-555555555555` |
| `<APP_OBJECT_ID>` | Object ID of the **enterprise application** (service principal) | `66666666-7777-4888-9999-000000000000` |
| `<GROUP>` | Alias of a new mail-enabled security group | `sg-agent-mailboxes` |
| `<SCOPE>` | Management scope name | `Agent-Mailboxes` |
| `<IN_MAILBOX>` | A mailbox that must be reachable | `relay@contoso.com` |
| `<OUT_MAILBOX>` | A mailbox that must be refused | `ceo@contoso.com` |
| `<ADMIN_UPN>` | Exchange admin (Organization Management) | `admin@contoso.com` |

## The Union Trap (verified 2026-09)

- Entra consent and Exchange RBAC for Applications are **added together**. An unscoped `Mail.Read` in Entra plus a scoped `Mail.Read` in Exchange = tenant-wide `Mail.Read`. Microsoft's own FAQ: "results in no effective resource scoping".
- So in Entra, the app registration gets **no** `Mail.*`, `MailboxItem.*`, `Mail-Advanced.*` or `Calendars.*` application permission. Mail rights come only from `New-ManagementRoleAssignment`.
- `Test-ServicePrincipalAuthorization` **ignores Entra grants**. It will show a perfect scope while Entra leaks the whole tenant. Check Entra separately (step 0 below) and check the token's `roles` claim.
- `New-ApplicationAccessPolicy` doc (updated 2026-05): "Don't create new App Access Policies". RBAC for Applications replaces it. An old policy only constrains Entra grants, never RBAC ones.
- **Exclusive** management scopes do not restrict app access. Use a normal scope.
- `MemberOfGroup` counts **direct** members only; nested groups are out of scope. Mail-enabled security groups, M365 groups and distribution lists work as the filter target.

## Setup: Exchange RBAC for Applications

Run as `<ADMIN_UPN>` in a **fresh** `pwsh` process. A role change in Entra (e.g. you were just made Exchange Administrator) is not seen by an already-open session: `Disconnect-ExchangeOnline`, exit the process, reconnect (observed 2026-09).

```powershell
$AppId       = '<APP_ID>'
$AppObjectId = '<APP_OBJECT_ID>'
$Group       = '<GROUP>'
$Scope       = '<SCOPE>'
$InMailbox   = '<IN_MAILBOX>'
$OutMailbox  = '<OUT_MAILBOX>'
$Mailboxes   = @('<IN_MAILBOX>', '<MAILBOX_2>', '<MAILBOX_3>')
$ErrorActionPreference = 'Stop'

# 0. Entra must hold NO mail application permission (union trap).
Connect-MgGraph -Scopes 'Application.Read.All' -NoWelcome
$graphSp = Get-MgServicePrincipal -Filter "appId eq '00000003-0000-0000-c000-000000000000'"
$leaks = Get-MgServicePrincipalAppRoleAssignment -ServicePrincipalId $AppObjectId |
  Where-Object { $_.ResourceId -eq $graphSp.Id } |
  ForEach-Object { $id = $_.AppRoleId; ($graphSp.AppRoles | Where-Object Id -eq $id).Value } |
  Where-Object { $_ -match '^(Mail|MailboxItem|MailboxFolder|Mail-Advanced|Calendars|Contacts)' }
if ($leaks) { throw "Entra grants make the scope useless: $($leaks -join ', ')" }

# 1. Group: direct members only, created with its members, closed to self-join.
Connect-ExchangeOnline -UserPrincipalName '<ADMIN_UPN>' -ShowBanner:$false
if ($Mailboxes -contains $OutMailbox) { throw 'Negative-test mailbox must stay outside the list.' }
$g = New-DistributionGroup -Name $Group -Alias $Group -Type Security -Members $Mailboxes `
  -MemberJoinRestriction Closed -MemberDepartRestriction Closed
$dn = $g.DistinguishedName.Replace("'", "''")
$filter = "MemberOfGroup -eq '$dn'"
Get-Recipient -RecipientPreviewFilter $filter -ResultSize Unlimited |
  Select-Object PrimarySmtpAddress, RecipientTypeDetails      # must list exactly $Mailboxes

# 2. Pointer to the Entra service principal (IDs from Enterprise applications, not App registrations).
New-ServicePrincipal -AppId $AppId -ObjectId $AppObjectId -DisplayName 'agent-mailboxes'

# 3. Scope + role assignment. Pick the smallest role: Mail.ReadBasic < Mail.Read < Mail.ReadWrite.
New-ManagementScope -Name $Scope -RecipientRestrictionFilter $filter
New-ManagementRoleAssignment -Name "agent-mail-$Scope" -App $AppObjectId `
  -Role 'Application Mail.ReadWrite' -CustomResourceScope $Scope
```

- If `New-ManagementScope` asks for it: `Enable-OrganizationCustomization`, then wait. Usually 15-30 min, observed up to 24 h.
- `-App` accepts ObjectId, AppId or display name (doc, 2026-08). Pass the **enterprise application** ObjectId: the Object ID on the App registrations page is a different object and matches nothing.
- Group membership of a mail-enabled security group is edited in Exchange (EAC or `Add-DistributionGroupMember`), not in Entra, where "Add members" is greyed out (observed).
- Never re-run blindly after a partial failure. Inspect `Get-ManagementScope`, `Get-ServicePrincipal`, `Get-ManagementRoleAssignment -RoleAssignee $AppObjectId` first.

## Prove the Scope: Positive and Negative, Twice

Layer 1 (RBAC only, bypasses the cache, so valid immediately):

```powershell
Test-ServicePrincipalAuthorization -Identity $AppObjectId -Resource $InMailbox  | Format-Table RoleName, AllowedResourceScope, InScope
# Output: Application Mail.ReadWrite  Agent-Mailboxes  True
Test-ServicePrincipalAuthorization -Identity $AppObjectId -Resource $OutMailbox | Format-Table RoleName, AllowedResourceScope, InScope
# Output: Application Mail.ReadWrite  Agent-Mailboxes  False
```

Layer 2 (real Graph call). Wait: the app cache holds old permissions **30 min (idle app) to 2 h (active app)** (doc, verified 2026-09). Then, with an app-only token (client credentials + certificate, scope `https://graph.microsoft.com/.default`) read from stdin, never argv:

```bash
# token must carry NO mail role; a Mail.* entry here proves an Entra grant (union trap)
python3 -c 'import sys,json,base64;p=sys.stdin.read().split(".")[1];p+="="*(-len(p)%4);print(json.loads(base64.urlsafe_b64decode(p)).get("roles",[]))' <<<"$TOKEN"
# Output: []
printf 'header = "Authorization: Bearer %s"\n' "$TOKEN" | curl -s -o /dev/null -w '%{http_code}\n' -K - \
  "https://graph.microsoft.com/v1.0/users/relay@contoso.com/mailFolders/inbox/messages?\$top=1&\$select=id"
# Output: 200
printf 'header = "Authorization: Bearer %s"\n' "$TOKEN" | curl -s -o /dev/null -w '%{http_code}\n' -K - \
  "https://graph.microsoft.com/v1.0/users/ceo@contoso.com/mailFolders/inbox/messages?\$top=1&\$select=id"
# Output: 403
```

These two `curl` calls are a one-off admin probe, run by hand outside the agent; the runtime gate below would refuse a folder listing. A `200` on `<OUT_MAILBOX>` is a leak: stop, go back to step 0. A `403` on `<IN_MAILBOX>` within 2 h is the cache; after 2 h it is a wrong ObjectId or a nested member.

## Closed Call List

`Mail.ReadWrite` does not send (doc: "Doesn't include permission to send mail"), but it does PATCH and DELETE any message in every scoped mailbox. The permission does not protect the mailboxes; the call list does.

| Call | Allowed when |
|---|---|
| `GET /users/{mb}/mailFolders/{folder}/messages/delta?$select=…` | folder in policy, `$select` **required** and inside policy, only `changeType` besides |
| `GET` a Graph-issued `@odata.nextLink` / `@odata.deltaLink` | URL byte-identical to the one Graph returned **and** its stored origin is an initial delta call that passes the gate today (see below) |
| `GET /users/{mb}/messages/{id}?$select=…` | `$select` **required** and inside policy, nothing else. Re-read before any write |
| `GET /users/{mb}/messages/{id}/attachments?$select=id,name,contentType,size,isInline` | `$select` required, metadata fields only |
| `GET …/attachments/{aid}/$value` | documented exception: bytes, only if `allow_attachment_content: true` |
| `POST /users/{mb}/messages/{id}/createReply` | reply text goes in the `comment` parameter |
| `PATCH /users/{mb}/messages/{draftId}` | `draftId` returned by `createReply` **this cycle**, re-read shows `isDraft: true` and same mailbox |
| everything else | denied, including every read without a compliant `$select`: `…/messages/{id}` bare, `…/messages/{id}/$value` (raw MIME), `$expand`, `$top`, dollar-less `select=`, `…/messages` and `…/mailFolders/{id}/messages` lists, `…/attachments/{aid}` object; and `DELETE`, `send`, `sendMail`, `reply`, `replyAll`, `forward`, `move`, `copy`, `$batch`, `subscriptions`, `/me`, `/beta` |

- **Continuation links cannot carry `$select`**: they inherit the fields of the initial call. So the state file stores each Graph-issued link **with the initial delta URL that started its chain** (`{"link": …, "origin": …}`), and the gate re-checks that origin against the current policy. A link born from a call without `$select`, with a field outside policy, on another folder, or under an older wider policy is refused: narrowing `select` forces a full resync, which is the point.
- `createReply` and `PATCH` responses contain the whole draft, quoted thread included (`$select` does not apply to these writes). Keep the returned `id` and discard the rest before anything reaches the agent.

- Put the reply in `createReply`'s `comment`: Graph inserts it above the quoted thread. A PATCH of `body.content` replaces the whole body and drops the thread.
- From 2026-12-31, `Mail.ReadWrite` can no longer change sensitive properties (subject, body, recipients…) of **non-draft** messages; that needs `Mail-Advanced.ReadWrite.All`. Drafts stay editable. Do not request the advanced permission for a drafting agent.
- Success is the id Graph returns. Exit 0 without an id = `uncertain`, never `applied`.

Gate every call through `scripts/graph_allowlist.py` (stdlib, fail-closed: missing, empty, malformed or unknown input is a denial):

```bash
cat > policy.json <<'EOF'
{"mailboxes": ["relay@contoso.com", "00000000-0000-4000-8000-000000000001"],
 "folders": ["inbox"], "select": ["id","subject","from","receivedDateTime","isDraft","conversationId"],
 "allow_attachment_content": false}
EOF
cat > cycle.json <<'EOF'
{"draft_ids": {"relay@contoso.com": []},
 "issued_links": [{"link": "<@odata.deltaLink exactly as returned>",
                   "origin": "https://graph.microsoft.com/v1.0/users/relay@contoso.com/mailFolders/inbox/messages/delta?$select=id,subject"}]}
EOF
# written only by your script, from Graph responses to gate-approved calls; nextLinks inherit the chain's origin
python3 scripts/graph_allowlist.py --policy policy.json --cycle cycle.json \
  DELETE "https://graph.microsoft.com/v1.0/users/relay@contoso.com/messages/AAMkAGI2TG93AAA="
# Output: DENY DELETE on a message is never allowed   (exit 2; 0 = allow, 3 = unusable input)
```

List both the address and the user object id in `mailboxes`: links returned by Graph can carry either form.

## Delta Polling

- Delta is **per folder**. One cursor per mailbox per folder.
- Follow `@odata.nextLink` immediately in the same cycle. It is pagination, not a cursor: never persist it.
- Persist only `@odata.deltaLink`, with the initial delta URL it descends from, atomically (temp file, validate, rename), in the same transaction as the queue items it produced.
- Put `$select`, `changeType`, `Prefer: odata.maxpagesize` on the **initial** call only. Graph encodes them into the token; re-adding them to a `nextLink`/`deltaLink` is unsupported (doc: "don't modify subsequent delta query requests to repeat these query parameters").
- `@removed` with `"reason": "deleted"` is also emitted when a message is **moved out of the folder** (doc, 2026-06). A user filing mail into a subfolder is not a deletion: drop it from the work queue, conclude nothing, alert nobody.
- Outlook delta tokens have **no fixed lifetime**: they die when Microsoft's token cache overflows, with a 40X and `syncStateNotFound`. `410 Gone` with a `Location` holding an empty `$deltatoken` means tenant maintenance or migration. Both: full resync of that mailbox **and** an alert. Without the alert the cron exits 0 forever and detects nothing.
- One failing mailbox must not stop the sweep: `try` per mailbox, keep its cursor, mark it `degraded`, exit non-zero at the end.
- Webhooks need a public HTTPS endpoint and a subscription renewed within days. Behind NAT, poll delta.

## Throttling and Errors (verified 2026-09)

| Signal | Meaning | Do |
|---|---|---|
| 10,000 requests / 10 min | Limit per **app + mailbox** pair | Budget per mailbox, not globally |
| 4 concurrent requests | Per app + mailbox; one mailbox over the limit does not affect others | Semaphore of 4 **per mailbox**. A global cap of 4 is slow and still wrong |
| 150 MB upload / 5 min | PATCH/POST/PUT per app + mailbox | Large drafts count |
| `429` / `503` | Throttled | Honor `Retry-After`; if absent, exponential backoff with jitter. Retry next cycle, never in a tight loop |
| `401` / `403` on an in-scope mailbox | Rights changed or cache | Mark `degraded`, keep cursor, alert a human. Retrying does not fix rights |
| `syncStateNotFound`, `410 Gone` | Cursor dead | Full resync + alert |
| Known mailbox unreachable after its owner left | Mailbox turned **inactive** | App-only access cannot read an inactive mailbox (observed): recover or restore it to an active or shared mailbox, or use a compliance export |
| `400 SearchWithSkip` | `$search` + `$skip` | Follow `@odata.nextLink` instead |

## Output Format

Write this record after every setup or scope change. It is the proof the data controller files.

```
MAILBOX-SCOPE RECORD — <date>
app: <APP_ID> / enterprise object <APP_OBJECT_ID>
entra mail permissions: none (checked <time>) | token roles: []
role: Application Mail.ReadWrite | scope: <SCOPE> | filter: MemberOfGroup (direct members)
mailboxes (n=<N>): <list>
rbac test: <IN_MAILBOX> InScope=True | <OUT_MAILBOX> InScope=False
graph test (+<minutes> min): <IN_MAILBOX> 200 | <OUT_MAILBOX> 403
call gate: graph_allowlist.py, policy sha256 <hash>
basis: <ref> | retention: <days> | owners informed: <date>
STATUS: SCOPED | LEAK | PENDING-CACHE
```

```
MAILBOX-SCOPE RECORD — 2026-09-30
app: 11111111-2222-4333-8444-555555555555 / enterprise object 66666666-7777-4888-9999-000000000000
entra mail permissions: none (checked 09:12) | token roles: []
role: Application Mail.ReadWrite | scope: Agent-Mailboxes | filter: MemberOfGroup (direct members)
mailboxes (n=3): relay@contoso.com, sales@contoso.com, support@contoso.com
rbac test: relay@contoso.com InScope=True | ceo@contoso.com InScope=False
graph test (+95 min): relay@contoso.com 200 | ceo@contoso.com 403
call gate: graph_allowlist.py, policy sha256 3f9a…
basis: DPIA-2026-07 | retention: 30 | owners informed: 2026-09-15
STATUS: SCOPED
```

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| App reads a mailbox outside the group | Entra `Mail.*` consent still present (union) | Remove the Entra permission and admin consent; re-run step 0 and the negative Graph test |
| RBAC test `True`, Graph `403` | Permission cache | Wait up to 2 h; the test bypasses the cache, Graph does not |
| Member of a sub-group refused | Nested groups ignored | Add the mailbox directly to `<GROUP>` |
| `New-ServicePrincipal` or assignment "not found" | IDs copied from App registrations | Use Application ID + Object ID from **Enterprise applications** |
| New admin role has no effect | Open PowerShell session caches the old token | Disconnect, exit the process, reconnect |
| Draft lost the quoted thread | Body set with PATCH | Use `createReply` with `comment` |
| Delta returns nothing for days, exit 0 | Dead cursor swallowed | Treat `syncStateNotFound`/`410` as resync + alert |
| Exclusive scope did not restrict | Exclusive scopes do not apply to apps | Use a regular management scope |

## Scope

This skill ONLY:
- scopes an app to a named list of mailboxes through Exchange RBAC for Applications and proves it both ways;
- reads, and at most creates reply drafts, through a closed call list;
- keeps ids and metadata, not content, and logs actions without content.

This skill NEVER:
- grants `Mail.*` in Entra, creates an Application Access Policy, or uses an exclusive scope as a restriction;
- sends, forwards, moves, deletes, or marks mail as read;
- runs before the lawful basis, retention and owner information above are settled;
- gives the agent the certificate or a token.
