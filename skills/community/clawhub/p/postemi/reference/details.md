# Postemi CLI: details

The main skill ([../SKILL.md](../SKILL.md)) links here for the things an agent
needs only now and then: making an account, what a key can do, billing, rate
limits and the analytics repair.

## Creating an account

Only when the user asks you to make them a Postemi account and they have none.

```bash
postemi auth:signup --email anna@example.com
# → {codeSent:true, terms, privacy, timezone, language, next}
postemi auth:signup --email anna@example.com --code 123456 --accept-terms [--workspace-name "Anna's Cafe"] [--timezone Europe/London]
# → {created:true, workspaceId, workspaceName, trial:false, credentials, next}
```

1. Run it with `--email` only. Postemi e-mails the user a six digit code (valid
   10 minutes). Ask the user to read the code to you. Off a terminal, `next`
   is the exact second command with every option kept.
2. Show the user the terms (https://postemi.com/terms) and the privacy notice
   (https://postemi.com/privacy) and ask whether they agree. Pass
   `--accept-terms` ONLY after they said yes; never decide it for them.
3. Run it again with `--code` and `--accept-terms`. The CLI keeps the sign-in
   the same way `auth:login` does and never prints it.
4. **There is no free trial on an account made this way.** Until the user
   pays, only the `billing:*` commands work. Next: `billing:plans`, confirm a
   plan with the user, `billing:subscribe`, give them the link. The user
   connects channels in the web app after paying.
5. **You keep working for the user only on a plan with API access**
   (`limits.apiAndMcpAccess: true` in `billing:plans`). Basic has none: if the
   user picks it, tell them BEFORE they pay that you will not be able to
   schedule for them afterwards. `billing:subscribe` answers with
   `apiAndMcpAccess: false` and a warning on stderr for such a plan.

Exit 1 with "already has a Postemi account" (HTTP 409): the address is taken, so
the user signs in with `postemi auth:login`. A wrong or expired code: run step 1
again for a new one.

## What a key can do

`postemi auth:login` is a device login: the CLI asks Postemi for a short code,
opens the approval page, and waits until the signed in human approves it and
chooses which workspace and which channels the new key may reach. Keys can
also be made in the web app under Settings, Developers. A key is shown once;
a lost key cannot be recovered, only rotated.

Two limits apply to every request, and both explain a 403 that looks like a
bug:

1. **Scopes.** A key carries some of `posts:read`, `posts:draft`,
   `posts:publish`, `channels:read`, `channels:write`, `media:write`,
   `analytics:read`. A route refuses a key without its scope.
2. **The owner's current role, checked on every request.** A key never does
   more than the person who made it can do right now. If that person loses a
   role, their keys narrow on the next request. A key that worked yesterday
   can return 403 today with no change to the key.

A key can also be limited to some workspaces and some channels; a request that
names a channel outside the grant is refused even with the right scope.

On a 403, read the message: it names what is missing. Do not retry, do not
try another route around it, and do not run `auth:login`. Ask the user for a
key with that access, or to have someone with the right role make one.

## Subscription (only when the user asks)

The only commands that name a plan. Use them only when the user asks about
plans, asks to subscribe, or asks to manage the subscription; never suggest a
plan or an upgrade otherwise.

```bash
postemi billing:plans                                  # → {current, plans:[{plan, slug, monthly, yearly, limits}], trial, trialDays}
postemi billing:subscribe --tier pro --period yearly   # → {status:"requires_payment", checkoutUrl, ..., apiAndMcpAccess}
postemi billing:status                                 # → {state, plan, period, currentPeriodEnd, payerIsCaller, pendingCheckout, apiAndMcpAccess}
postemi billing:manage                                 # → {portalUrl}
```

1. Confirm the plan (Basic, Pro, Creator or Team: `--tier basic`, `pro`,
   `creator` or `team`, or the `slug` that `billing:plans` prints) and the
   period (monthly or yearly) with the user. Basic has no API access: if the
   user picks it, tell them BEFORE they pay that you will not be able to
   schedule for them afterwards.
2. Run `billing:subscribe` once and give the user `checkoutUrl`. **The user
   opens it and pays with their OWN Link wallet or card.** Never pay with a
   one time or agent issued card, a virtual card number or any credential of
   your own: the subscription renews, and a one time credential fails at the
   first renewal, which ends the plan. `--open` opens the link in this
   machine's browser; use it only when this machine is the user's own.
3. After the user says they paid, run `billing:status` and check that `state`
   is `trialing` or `active`. If it shows a `pendingCheckout`, give that link
   back instead of running `billing:subscribe` again.
4. Plan changes, cancelling and invoices are in the Stripe portal:
   `billing:manage` prints the link.

These commands work before the workspace has a plan (they are how it gets
one). `billing:subscribe` and `billing:manage` need a full workspace key or a
sign-in held by the person who pays (or a workspace owner when nobody pays
yet); a scoped key is refused with a message that says so.

## Rate limits

Per key, per route, per hour. Each route has its own allowance, so polling
`posts:list` cannot use up `posts:create`.

| Routes | Limit per hour |
|---|---|
| Reads: `posts:list`, `posts:get`, `integrations:list`, `integrations:groups`, `integrations:settings`, `posts:missing`, `posts:find-slot`, `notifications:list` | 600 |
| Writes: `posts:create`, `posts:update`, `posts:reschedule`, `posts:retry`, `posts:delete`, `posts:delete-group`, `posts:status`, `integrations:trigger` | 60 |
| Analytics: `analytics:platform` (`analytics:channel`), `analytics:post` | 30 |
| Uploads: `upload`, `upload:url` | 30 |
| Upload links: `upload:link` 60, `upload:files` 600 | |

Rotating a key starts a fresh allowance. Over the limit the answer is `429`:
wait, and do not retry in a tight loop, which only uses up the next hour too.

## When analytics says missing

If `analytics:post` returns `{"missing": true}`, the post was published but the
platform did not give back a usable post id (TikTok often does this). Connect
the post to its content once, then analytics work:

```bash
postemi posts:missing <post-id>
# → [{"id": "7321456789012345678", "url": "https://...cover.jpg"}, ...]
postemi posts:connect <post-id> --release-id "7321456789012345678"
postemi analytics:post <post-id>
```

Show the user the candidates (the `url` is a cover picture) and let them pick
when it is not clear which one is theirs. `posts:missing` returns an empty list
when the platform does not support this or the post is not missing its id.
