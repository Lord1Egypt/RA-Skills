---
name: instagram-account-operations
description: Keep an automated Instagram account out of action blocks — Meta Business Suite DMs, comments, quotas. Use when scheduling IG replies from a cron or agent. Trigger on "instagram bot", "action blocked", "instagram dm automation", "reply to instagram comments", "instagram shadowban".
metadata: {"clawdbot":{"emoji":"📸","homepage":"https://openclaw.ai"}}
---

# Instagram Account Operations

**The goal is not to reply fast. The goal is to operate Instagram like a careful, helpful human contributor — through Meta Business Suite, inside quota, and openly, on an account you are authorized to run.**

## Access, Data & Network — read before running anything

| What it needs | Why | Default |
|---|---|---|
| A browser profile already logged into `business.facebook.com` | MBS is the only surface this skill drives | You log in by hand. The skill never handles credentials, never types a password, never launches a login flow. |
| Read access to your IG DMs and comments | It replies to them | Scoped to the one asset ID you configure |
| Local directory `<WORKSPACE_DIR>/memory/` | Quota counting, dedupe, phase state | Created by you (see checklist) |
| Alert webhook (Telegram/Slack/Discord) | Run recaps | **Off by default. Opt-in.** Leave `alerts.webhook` empty and the skill writes recaps to disk only — no network egress beyond Meta's own domains. |

Persisted locally, and nothing else: run recaps, counts of replies sent, IG handles you replied to (for the 7-day dedupe), phase state, follower count, hashtag notes. **Retention: 90 days** — truncate the memory files on that cadence. If you enable a webhook, the recap block in *Recap output* leaves your machine verbatim, including hot-lead handles; redact or keep it off. Instagram's Terms of Use and Community Guidelines, and Meta's Platform Terms, are a hard constraint on everything below, not a footnote: run this only on an account you own or are contractually authorized to operate, and only where automated replies are permitted for your account type.

## When to Use

| Trigger | Action |
|---|---|
| "check my Instagram DMs" / cron DM pass | Session check → MBS `inbox/all` → qualify → reply within quota |
| "reply to instagram comments" | MBS `inbox/instagram` → `@username` flow |
| "action blocked" / "try again later" toast | **Stop the run.** Flip to Phase A, alert, human reviews |
| "am I shadowbanned" / followers dropped overnight | Flip to Phase A, alert, no automated recovery attempt |
| "set up my instagram bot" | Configure → first-run checklist → 14 days manual first |
| Any challenge, CAPTCHA, or "verify it's you" screen | **Stop. Hand to a human.** Never solve, never retry, never reshape behavior to get past it |

## Configure

| Placeholder | Example | Your value |
|---|---|---|
| `<BRAND_NAME>` | "Acme Studio" | — |
| `<IG_HANDLE>` | "@acmestudio" | — |
| `<META_BUSINESS_ID>` | numeric ID from business.facebook.com → Settings | — |
| `<META_ASSET_ID>` | numeric ID of the IG asset in MBS | — |
| `<BROWSER_PROFILE>` | "instagram-live" | — |
| `<BROWSER_PORT>` | "18802" | — |
| `<PRIMARY_CTA>` | "WhatsApp / form / app — pick ONE" | — |
| `<WORKSPACE_DIR>` | "~/.openclaw/workspace/instagram-acme" | — |

```yaml
# <WORKSPACE_DIR>/config.yaml
instagram: { handle: <IG_HANDLE>, account_type: business, browser_profile: <BROWSER_PROFILE>, browser_port: <BROWSER_PORT> }
meta_business_suite: { business_id: <META_BUSINESS_ID>, asset_id: <META_ASSET_ID> }
cta: { primary: <PRIMARY_CTA> }        # one channel only
alerts: { channel: telegram, webhook: "" }   # empty = no egress, recaps to disk only
schedule:
  timezone: Europe/Paris
  windows: { dm_check: "*/15 9-22 * * *", comment_check: "10,25,40,55 9-22 * * *", daily_recap: "21:00" }
```

Shell snippets use the OpenClaw browser CLI over CDP; any CDP-capable stack works (Playwright, Puppeteer, Chrome MCP) — swap the calls. Multi-account: one workspace dir, one browser profile and one port per account; each account carries its own `<META_ASSET_ID>`.

## Meta Business Suite is the only surface

**Everything goes through `business.facebook.com`. Never automate against `instagram.com`.** No iframes; one UI for IG DMs, FB DMs, IG comments, FB comments; `click + type + Enter` works; link previews auto-generate. Append `?business_id=<META_BUSINESS_ID>&asset_id=<META_ASSET_ID>` to each URL fragment below.

| Tab | URL fragment |
|---|---|
| All messages | `/latest/inbox/all` |
| Instagram DMs only | `/latest/inbox/instagram_direct` |
| Instagram comments | `/latest/inbox/instagram` |
| Messenger (FB DMs) | `/latest/inbox/messenger` |

Roles are a mental separation on one physical profile: `ig-post` acts as the brand inside MBS · `ig-engage` reads and qualifies, and **never acts outside MBS** · `ig-observe` checks hashtag reach in a logged-out window, so results reflect what the public sees rather than what your own account history personalizes — nothing is posted, liked, or followed from there. Return to `inbox/all` at the end of every run. Approved Graph API app available (`instagram_basic` / `instagram_manage_messages` / `instagram_manage_comments`)? Use it — this playbook is the fallback for accounts without one, and for the MBS UI features the API lacks (labels, prospect stages, link previews).

## Session check — run first, every cron

```bash
openclaw browser --browser-profile <BROWSER_PROFILE> status
# Output: profile=instagram-live state=running cdp=http://127.0.0.1:18802
openclaw browser --browser-profile <BROWSER_PROFILE> navigate \
  "https://business.facebook.com/latest/inbox/all/?business_id=<META_BUSINESS_ID>&asset_id=<META_ASSET_ID>"
openclaw browser --browser-profile <BROWSER_PROFILE> snapshot --limit 60
# Output: … [textbox "Search messages"] … [list] Conversations (12)   → OK, continue
# Output: … [form] Log into Facebook …                                → exit 3, stop
```

`status: stopped`, a login form, or a "Reauthenticate to manage this asset" banner all mean **stop and report**. Never relaunch Chrome from inside a cron. Never re-login programmatically.

## Phase gating

Instagram has no karma. It has **action blocks** — 24 h (warning), 7 d (second), permanent (third+).

| Phase | Condition | Authorized |
|---|---|---|
| **A** | account < 30 d, OR an action block in the last 30 d, OR < 500 followers | Inbound DM/comment replies inside MBS only. **Zero outbound.** |
| **B** | ≥ 30 d, no block in 30 d, ≥ 500 followers, no guideline flag | All crons |

Read `<WORKSPACE_DIR>/memory/ig-state.md` at start; last line is the current phase. A→B is **never automatic**: on threshold, alert `🎉 IG account ready for Phase B — review and flip manually`, and a human flips it. First week of B: cap at 3 replies/run. Observed block thresholds (not officially published, treat as ceilings you stay far under — they are limits that protect the account, not a budget to spend; if you are anywhere near one, the run is doing too much): follow/unfollow > 50/day or > 200/week · comments on others' posts > 30/hr or > 200/day · proactive DMs to non-followers > 10/day on a young account · likes > 60/hr · posts > 5/24h · > 6 actions in 10 min on one role · follow + like of the same account's last 5 posts inside 1 min → immediate block · the same DM body to > 3 accounts in 24 h → "Action blocked" toast within minutes.

## Quotas — hard limits

| Action | Phase A | Phase B |
|---|---|---|
| DMs handled per 24 h | 20 | 60 |
| DMs handled per run | 4 | 8 |
| Comment replies per 24 h | 30 | 100 |
| Comment replies per run | 5 | 10 |
| Outbound DMs / day | 0 | 5 |
| Follows / day · Unfollows / day | 5 | 20 |
| Likes / hour | 30 | 60 |
| Gap, same conversation | ≥ 60 s | ≥ 30 s |
| Gap, globally | ≥ 30 s | ≥ 15 s |

Count entries in `ig-reply-log.md` for the last 24 h at start of every run. Quota met → abort early with `status: skipped`.

## Posting cadence and hashtags

Out of scope for the reactive crons; the rhythm the rest of the doctrine assumes, logged in `ig-post-log.md`.

| Surface | Phase B rhythm |
|---|---|
| Reels | 3-5/week · hook in the first 1.5 s · vertical 9:16 · native or licensed sound |
| Carousels | 2-3/week · educational — saves are the strongest ranking signal |
| Stories | 3-7/day · polls and stickers carry reach |
| Lives | ≤ 1/week, planned |
| Hashtags | 3-5 per post — 1 broad + 2-3 niche + 1 micro (< 50k posts). The "30 hashtags" advice is dead: IG cut the cap and over-tagging reads as spam. Re-check `ig-hashtag-state.md` monthly for tags gone dead. |

## Qualify before replying

Repliable only if **all** hold: the thread has a user-authored message (not a bare Reel forward — skip those silently) · the user isn't sitting on an unacknowledged auto-reply · it's a real question in your domain · Phase B if the reply mentions the brand · no brand-mentioning reply to that handle in the last 7 days (`ig-reply-log.md`). Any check fails → skip, and say why in the recap. If the handle is in `ig-clients-known.md`: reply with empathy, **paste no link**, redirect to the support channel — `<PRIMARY_CTA>` is for prospects only.

## Reply templates

Phase A: 1-3 sentences, match the tone, no links, no expert-grade advice. Phase B DM (≤ 700 chars — past that nobody reads it):
```
[Acknowledge the situation in 1 sentence, neutral tone.]

[General framework in 2-3 short paragraphs.]

[Concrete next step — point to <PRIMARY_CTA>. ONE channel only.]
```
Filled:
```
Sorry you're dealing with that — a suspended licence is stressful and the clock matters.

Broadly, two things decide the outcome: the notice date on the decision, and whether the procedural steps were followed. Both are checkable from the paperwork you already have.

If you want it looked at properly, the intake form on our profile is the fastest route.
```
Phase B comment (≤ 200 chars):
```
@username [contextual acknowledgement]. [Indirect signal — "DM us" or "form on profile"].
```

Never paste: anything with `[brackets]` left in · the same opening phrase more than twice in 7 days · a URL in a comment body, ever · more than one URL in a DM · a URL in the *first* message of a conversation — Meta's link-preview takes 1-2 s to generate and IG classes the bare link as spam; the `<PRIMARY_CTA>` link goes in the second message · any shortener (bit.ly, tinyurl — IG treats them as spam).

## MBS flow — DMs

1. Session check (above), then navigate `inbox/all`. Wait 5 s for the list to render.
2. Click the "Unread" filter chip, or read the list for unread badges.
3. Per conversation, top-to-bottom: click the tile → **read the whole thread** (IG threads often span auto-template + the real reply) → qualify → click `[contenteditable='true']` → `type` the message → **press Enter** → verify the textbox emptied and the message landed before moving on.
4. Sweep the `Messenger` and `Instagram` tabs after `all` — some conversations surface only there.

**Press Enter, do not click "Send".** MBS renders visual duplicates of the send button and a Playwright `click` lands on the wrong one roughly one time in ten — silently, with no error. Enter is unambiguous.

## MBS flow — comments

Less stable than DMs. Navigate to `inbox/instagram`, wait 5 s, click a post tile, comments render in the right pane. Per qualified comment: find the page-level "Add a comment…" / "Ajoutez un commentaire…" textarea **at the bottom** of the right pane, type `@username your reply`, then **click the send-arrow** — Enter does not submit here. **Do not click "Reply" under a comment.** Meta's SPA navigates the right pane to a *different post* (bug present 2025-2026). You'll think it worked; you replied somewhere else. The `@username` prefix targets the parent comment without it. If you truly need a nested reply, a human does it on `instagram.com` and logs it in `ig-reply-log.md` — do not script the `instagram.com` reply path.

| Element | Selector |
|---|---|
| DM textbox | `[contenteditable='true']`, `[aria-label*='Reply'], [aria-label*='Répondre']` |
| DM send | `press Enter` |
| Comment textarea | `textarea[placeholder*='comment'], textarea[placeholder*='commentaire']` |
| Comment send | `[aria-label*='Send'], [aria-label*='Envoyer']` (SVG arrow) |
| Unread filter chip | `text=Unread, text=Non lu` |

| Exit | Meaning | Recap |
|---|---|---|
| 0 | Replies sent and verified | `status: ok` |
| 1 | Fatal (selector missing, MBS error toast) | `status: error` + screenshot |
| 2 | "Action blocked" / "Try again later" | `status: blocked`, flip to Phase A pause |
| 3 | Session expired / reauth banner | `status: blocked`, alert human |
| 4 | Comment "Reply" navigated away (known bug) | `status: partial`, log for manual review |

## Content rules

| Avoid | Use instead |
|---|---|
| "Check link in bio" repeated | Mention bio once per conversation, max |
| `<BRAND_NAME>` twice in one reply | One mention |
| "DM me" + "WhatsApp me" + "click here" stacked | One CTA, one channel |
| Phone numbers, emails in comments | Never in a comment; DM tail only if asked |
| Emojis in regulated/sober niches | Drop them |
| Same opening phrase across replies | Vary it — identical openers *are* spam, that's why they get flagged |
| Replying < 30 s after a comment lands | Wait ≥ 2 min. You haven't read it yet in 30 s |

## Identity and conduct

- **If anyone asks whether they are talking to a bot, an AI, or a human: say so, plainly and immediately.** "Yes — this account's replies are handled by an automated assistant. Want me to get a person on it?" Then offer the human.
- If the person asks for a human, **stop automated replies in that thread**, escalate, and log it in the recap.
- Never give expert-grade advice on a specific case — redirect to `<PRIMARY_CTA>`. Never share private client details, names, or numbers. Never promise an outcome. Never solicit payment in DM.
- Handle and bio: brand-aligned, not aggressive (`@drsmithlegal` > `@bestlawyerinparis`). One line + one `<PRIMARY_CTA>` link.

## Stop conditions — the agent halts, a human takes over

| Signal | Action |
|---|---|
| "Please verify it's you" / CAPTCHA / any challenge | **Stop.** Never solve it, never retry, never change timing or behavior to get past it. Alert for manual login. A challenge is Instagram telling you a human should be here — believe it. |
| "Action blocked — try again later" | Stop the run. Phase A pause 24 h. Alert. |
| MBS → Settings → Account Status shows any "warning" | Revert to Phase A immediately, alert. Check this daily, not just at first run. |
| Login form or reauth banner | Session expired. Alert, stop. |
| `status: stopped` | Report, stop. |
| "Something went wrong" (generic) | Refresh once. Persists → stop and alert. |
| Followers drop > 5 % overnight | Suspected shadowban → Phase A, alert. No automated recovery. |
| 2 comments removed within 10 min of posting | Freeze the comment cron 6 h. |
| Account suspended (not just blocked) | Stop everything. **Do not appeal automatically** — the appeal flow is sensitive to repeated automated submissions. Human, manually, once. Log the last 20 actions in `ig-learnings.md`. |

## Recap output

Every run ends with this block — to `<WORKSPACE_DIR>/memory/ig-recaps.md` always, to the webhook only if you opted in. **Never fake a successful reply:** better silence than spam, better a blockage report than a false success.
```
## YYYY-MM-DD HH:MM TZ — <job-id> — status: ok|partial|blocked|skipped
- Phase: A|B
- DMs handled: <N or "—">
- Comments handled: <N or "—">
- Hot leads: <list or "—">
- Escalated to human: <N or "—">
- Blockers: <text or "—">
- Next useful action: <1 line>
```
Filled:
```
## 2026-07-16 21:00 Europe/Paris — ig-dm-check — status: partial
- Phase: A
- DMs handled: 3
- Comments handled: —
- Hot leads: @marc_r (licence suspension, asked for a callback)
- Escalated to human: 1 (@sofia.k asked to speak to a person)
- Blockers: comment tab hit the Reply-navigation bug once (exit 4)
- Next useful action: reply to @sofia.k manually before 10:00
```

## Memory files

`<WORKSPACE_DIR>/memory/` — `ig-recaps.md` (per run) · `ig-reply-log.md` (replies sent, quota + dedupe source) · `ig-state.md` (daily phase, followers, flags) · `ig-post-log.md` · `ig-hashtag-state.md` (weekly) · `ig-clients-known.md` (never pitch these) · `ig-ideas.md` · `ig-learnings.md` · `ig-alerts-sent.md` (alert dedupe). Plain markdown, local, yours to delete. 90-day retention.

## First-run checklist

- [ ] Placeholders filled; you own or are authorized to operate `<IG_HANDLE>`.
- [ ] Account is Business or Creator, linked to an MBS asset.
- [ ] `<META_BUSINESS_ID>` / `<META_ASSET_ID>` copied from the MBS URL.
- [ ] Browser profile at `http://127.0.0.1:<BROWSER_PORT>`, **logged in by hand**, `inbox/all` renders the conversation list.
- [ ] Memory dir created.
- [ ] Webhook decided: empty (no egress) or tested, knowing recaps carry handles.
- [ ] Phase A confirmed: inbound DM cron only.
- [ ] ≥ 14 days of manual posting and manual replies before any cron.
- [ ] Account Status (MBS → Settings) green, no warning.

```bash
mkdir -p "<WORKSPACE_DIR>/memory" && cd "$_" && for f in recaps post-log reply-log state hashtag-state clients-known ideas learnings alerts-sent; do [ -f "ig-$f.md" ] || touch "ig-$f.md"; done
# Output: (silent, idempotent — re-running never truncates an existing log)
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Reply "sent" but the thread is unchanged | `click` landed on a duplicate Send button | Press Enter instead; verify the textbox emptied |
| Right pane jumped to another post | The MBS comment-Reply SPA bug | `@username` prefix + page-level textarea + send-arrow; exit 4 |
| Selector matches nothing | UI is localized | Try both labels — `Reply`/`Répondre`, `Send`/`Envoyer` |
| Clicks land on stale tiles after a tab switch | MBS re-fetches the list on switch | Wait ≥ 3 s after switching tabs |
| Unread chip click does nothing | Transparent overlay on the chip | Snapshot before clicking |
| Reauth prompt out of nowhere | MBS soft-logs-out after ~48 h idle | Treat as session expired (exit 3), human logs in |
| Cron dies mid-run | MBS pages take 4-6 s to render | Timeout ≥ 1200 s |

## Scope

**This skill ONLY:** drives Meta Business Suite in a browser profile *you* logged into · replies to inbound DMs and comments within stated quotas · counts, dedupes, and reports what it did · stops and escalates when the platform pushes back · states plainly that it is automated when asked.

**This skill NEVER:** handles your password or performs a login · solves, retries, or works around a CAPTCHA, challenge, or any anti-abuse control · shapes timing or behavior to avoid being detected as automation · denies or obscures being automated · scripts `instagram.com` directly · exceeds the quota table · sends outbound DMs in Phase A · appeals a suspension automatically · touches an account you are not authorized to operate · sends anything off your machine unless you set a webhook.

Anti-abuse controls protect accounts, including yours. When a defense fires, the run ends and a human takes over.
