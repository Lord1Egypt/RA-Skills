# Keeping Notion in Sync — Webhooks, Polling, Conflicts

Reacting to changes made by humans in the UI. Two mechanisms, one hard problem (deciding who wins), and a set of loops that are easy to create by accident.

**Contents:** [Decide the Direction of Truth First](#decide-the-direction-of-truth-first) · [Polling](#polling) · [Webhooks](#webhooks) · [Avoiding Echo Loops](#avoiding-echo-loops) · [Conflict Resolution](#conflict-resolution) · [Deletions](#deletions) · [Schema Drift](#schema-drift)

**Before changing anything about a sync**, read `## Integrations` (webhook subscriptions and their targets) and `sync_posture` in `config.yaml`. Which side is the source of truth is a declaration, not something to re-derive.

## Decide the Direction of Truth First

| Posture | Meaning | Consequence |
|---|---|---|
| Notion is the record | Humans edit Notion, your system mirrors it | Your writes to Notion are rare and always user-initiated; sync is mostly reads |
| Notion is the mirror | Your system owns the data, Notion is the human-facing view | Notion edits are advisory; you may overwrite them, and you must say so to the humans who make them |
| Field-level split | Some properties owned each way | The only honest option for most workspaces, and the one that needs the ownership map written down |

Record it in `sync_posture.source_of_truth` in `config.yaml`, and record the per-property ownership in the `schemas/<data-source>.md` box. Two-way sync without a written ownership map produces edits that silently vanish, and no log will explain them.

## Polling

The mechanism that always works:

```json
{
  "filter": {"timestamp": "last_edited_time",
             "last_edited_time": {"on_or_after": "2026-07-26T10:00:00Z"}},
  "sorts": [{"timestamp": "last_edited_time", "direction": "ascending"}],
  "page_size": 100
}
```

- Store the watermark — the highest `last_edited_time` you processed — not the cursor (`pagination.md`).
- Use `on_or_after`, not `after`, and make processing idempotent: two rows with the same timestamp would otherwise straddle the boundary and one would be skipped.
- Overlap the window by a minute on restart. Reprocessing is cheap when writes are idempotent; a missed edit is invisible forever.
- **Cost**: one request per source per interval, plus one per 100 changed rows. Polling four data sources every 15 minutes is ~384 requests/day — negligible against the rate limit, and the honest default.
- Polling detects *that* a page changed, never *what* changed. Diffing against your own stored copy is the only way to know which property moved.

## Webhooks

Notion supports webhook subscriptions configured on the integration, delivering events to an HTTPS endpoint you host. Recorded 2026-07; verify the current event list and payload shape before building against a specific event.

The parts that matter regardless of the event list:

- **Verification handshake.** On subscription, Notion sends a verification token to the endpoint, which must be echoed or entered to activate the subscription. That token is a secret: `<keychain:notion-webhook>` in anything written down, never in a memory box.
- **Verify every delivery** before acting on it. An unauthenticated webhook endpoint is an open write path into your system.
- **Events are notifications, not data.** Retrieve the object by the id in the payload before doing anything with it; the payload is a pointer and can arrive after further edits.
- **Delivery is at-least-once and unordered.** Two events for one page can arrive out of order — always re-read, never apply a diff carried in the event.
- **Endpoint failures unsubscribe you eventually.** Return 2xx fast, queue the work, and monitor for silence: a webhook that stops delivering looks exactly like a workspace where nobody is editing.
- Keep a low-frequency poll as a backstop even with webhooks. It costs a few requests a day and turns a silent outage into a delay.

Record every subscription — event, target, endpoint, verification date — in `## Integrations` in `memory.md`.

## Avoiding Echo Loops

Your own writes bump `last_edited_time` and fire webhooks. Without a guard, every sync becomes a loop that also burns the rate limit.

- **Ignore edits whose `last_edited_by` is your bot id.** Get it once from `/v1/users/me` (`users.md`). This is the simplest and most reliable guard.
- Suppress the watermark advance for writes you made yourself, or raise the watermark past your own batch after writing.
- **Write nothing when nothing changed.** Compare against the stored copy before the PATCH — a no-op write is a real event to every other consumer, and at volume it is the difference between a quiet sync and a self-inflicted 429 storm.
- After a bulk backfill, expect the whole target to look changed; pause the sync or advance the watermark deliberately (`bulk.md`).

## Conflict Resolution

Both sides changed the same row since the last sync. Pick one policy and write it down:

| Policy | When it is right | What it costs |
|---|---|---|
| Source of truth wins | Notion is a mirror | Human edits disappear without a trace — tell the humans |
| Last write wins by timestamp | Both sides are casual | Clock skew and the 1-minute granularity of human editing make it arbitrary |
| Field-level ownership | The realistic default | Needs the ownership map in the schema box |
| Flag and stop | Financial or contractual data | Needs a human queue, and a comment on the row is the cheapest one (`comments.md`) |

## Deletions

The asymmetry nobody plans for: a row deleted in Notion goes to the trash and **stops appearing in queries**, which is indistinguishable from "not matching the filter any more".

- A page that vanished from a filtered query may be archived, edited out of the filter, or moved out of the connected subtree. Retrieve it by id and read `archived`/`in_trash` before propagating a delete (`search.md`).
- Do not propagate deletes from a filtered poll. Reconcile deletions on a slower full scan comparing id sets, which is the only reliable signal.
- Restoring from the trash is a user action and produces a normal edit event afterwards.

## Schema Drift

A property renamed or an option removed in the UI breaks a sync silently: filters stop matching, writes 400.

- Re-read the schema on the `## Due` cadence and compare to `schemas/<data-source>.md`. Property ids make the diff unambiguous (`databases.md`).
- On drift, update the schema box in the same turn and note it in `## Gotchas`.
- A sync that has been quiet for a suspiciously long time is a drift check, not good news.

**After configuring or changing a sync**, write the subscription, its endpoint and its verification date to `## Integrations` in `~/Clawic/data/notion-api-integration/memory.md`, the polling interval and conflict policy to `sync_posture` in `config.yaml`, the recurring reconciliation to `## Due`, and the ownership map into the affected `schemas/<data-source>.md` box.
