---
name: instagram-account-operations
description: Operating doctrine for Instagram account automation — careful creator + business pattern via Meta Business Suite, role separation, action-block awareness (24h/7d/permanent), comment + DM ops (Playwright click + type + Enter), reply qualification, hashtag-shadowban discipline, and recovery. Use this for any scheduled IG activity (cron, agent, recurring task) where account safety and Reels reach matter more than raw output.
---

# Instagram Account Operations

This skill is the operating doctrine for every Instagram automation run on a brand, professional or personal account.

**The goal is not to comment fast. The goal is to operate Instagram like a careful, helpful human contributor: stable browser, correct context (Meta Business Suite), useful action, no action block, no shadowban risk.**

Drop-in for any niche (legal, medical, software, finance, creator, ecommerce). Replace the placeholders in section 0 with your own values.

---

## 0. Configure for your brand

Before running anything, fill these placeholders in your local copy or your agent's memory:

| Placeholder | Example | Your value |
|---|---|---|
| `<BRAND_NAME>` | "Acme Studio" | — |
| `<BRAND_DOMAIN>` | "acme.studio" | — |
| `<IG_HANDLE>` | "@acmestudio" | — |
| `<META_BUSINESS_ID>` | numeric ID from business.facebook.com → Settings | — |
| `<META_ASSET_ID>` | numeric ID of the IG account asset in MBS | — |
| `<BROWSER_PROFILE>` | "instagram-live" | — |
| `<BROWSER_PORT>` | "18802" | — |
| `<NICHE_KEYWORDS>` | "lost license OR speeding ticket" | — |
| `<PRIMARY_CTA>` | "WhatsApp / form / app — pick ONE" | — |
| `<WORKSPACE_DIR>` | "~/.openclaw/workspace/instagram-<brand>" | — |

All shell snippets below assume an [OpenClaw](https://openclaw.ai) browser CLI bound by CDP, but the doctrine works with any browser-automation stack (Playwright, Puppeteer, Chrome MCP). Swap the CLI calls for your own.

### Quick config (copy-paste YAML)

If your agent reads config from YAML, drop this in `<WORKSPACE_DIR>/config.yaml`:

```yaml
brand:
  name: <BRAND_NAME>
  domain: <BRAND_DOMAIN>

instagram:
  handle: <IG_HANDLE>
  account_type: business | creator    # business strongly recommended for MBS access
  browser_profile: <BROWSER_PROFILE>  # e.g. "instagram-live"
  browser_port: <BROWSER_PORT>        # e.g. 18802

meta_business_suite:
  business_id: <META_BUSINESS_ID>
  asset_id: <META_ASSET_ID>
  base_url: https://business.facebook.com/latest/inbox

discovery:
  niche_keywords: <NICHE_KEYWORDS>

cta:
  primary: <PRIMARY_CTA>              # one channel only

workspace:
  dir: <WORKSPACE_DIR>

alerts:
  channel: telegram | slack | discord
  webhook: <YOUR_WEBHOOK_URL>

schedule:
  timezone: Europe/Paris
  windows:
    dm_check:      "*/15 9-22 * * *"       # every 15 min
    comment_check: "10,25,40,55 9-22 * * *" # offset to avoid collision
    browser_health: "0 * * * *"
    daily_recap:   "21:00"
```

### Compatibility

| Stack | Skill install path |
|---|---|
| [Claude Code](https://claude.ai/code) | `~/.claude/skills/instagram-account-operations/` |
| [OpenClaw](https://openclaw.ai) | `~/.openclaw/skills/instagram-account-operations/` |
| ClawHub-published | one-click install via [clawhub.ai](https://clawhub.ai) |
| Cursor / Copilot CLI | drop `SKILL.md` into your project's `.cursorrules` or `AGENTS.md` |
| Any LLM agent reading markdown rules | concatenate `SKILL.md` into your system prompt |

---

## 1. The Meta Business Suite is the only sane surface

**Doctrine: EVERYTHING goes through `business.facebook.com`. Never automate against `instagram.com` directly.**

Why:
- No iframes (unlike TikTok).
- Single UI for **4 channels**: IG DMs, FB Messenger DMs, IG comments, FB comments.
- Playwright `click + type + press Enter` works out of the box.
- Built-in CRM-style features: labels, notes, prospect stages.
- Link previews are auto-generated for the `<PRIMARY_CTA>`.
- Bypasses `instagram.com`'s "redirect to `/direct/inbox/`" bug.

### Physical profile

A single browser profile per account:

- `<BROWSER_PROFILE>` (CDP direct, attached to `http://127.0.0.1:<BROWSER_PORT>`)

The IG account must be **logged into Meta Business Suite** in this profile and have an Asset assigned to a Business — otherwise the URLs below will 404 or redirect to a setup wizard.

```bash
openclaw browser --browser-profile <BROWSER_PROFILE> status
openclaw browser --browser-profile <BROWSER_PROFILE> navigate https://business.facebook.com/latest/inbox/all/?business_id=<META_BUSINESS_ID>&asset_id=<META_ASSET_ID>
openclaw browser --browser-profile <BROWSER_PROFILE> snapshot --limit 200
```

### Canonical URLs (per tab)

| Tab | URL fragment |
|---|---|
| All messages (IG DMs + FB Messenger DMs) | `/latest/inbox/all?asset_id=<META_ASSET_ID>&business_id=<META_BUSINESS_ID>` |
| Messenger only (FB DMs) | `/latest/inbox/messenger?asset_id=<META_ASSET_ID>&business_id=<META_BUSINESS_ID>` |
| Instagram DMs only | `/latest/inbox/instagram_direct?asset_id=<META_ASSET_ID>&business_id=<META_BUSINESS_ID>` |
| Instagram comments | `/latest/inbox/instagram?asset_id=<META_ASSET_ID>&business_id=<META_BUSINESS_ID>` |
| Facebook comments | `/latest/inbox/facebook?asset_id=<META_ASSET_ID>&business_id=<META_BUSINESS_ID>` |

This skill covers IG-specific concerns; for FB-specific doctrine (Pages, groups, page moderation), see the companion `facebook-account-operations` skill.

### Roles (mental separation, single physical profile)

#### Role: `ig-post`

Account cockpit (acting as the brand). Use for:
- DM replies in MBS All / IG Direct tab.
- Comment replies in MBS IG Comments tab.
- Direct profile checks (only when MBS doesn't expose the metric).

Default page: MBS `inbox/all`.

#### Role: `ig-engage`

Discovery. Use for:
- Reading public conversations under your own posts (in MBS).
- Inspecting a candidate user's profile before replying to a comment (open in a new tab on `instagram.com`, but DO NOT act from there).

Default page: MBS `inbox/instagram` (comments tab).

#### Role: `ig-stealth`

Quiet maintenance. Use for:
- Story view audits.
- Hashtag-state checks (open hashtag in incognito, NOT in this profile).

Default page: MBS dashboard.

### Operational law

- `ig-post` = act as the account via MBS.
- `ig-engage` = discover and qualify, NEVER act outside MBS.
- `ig-stealth` = maintain and observe.
- Stability matters more than speed.
- After every run, return to MBS `inbox/all`.

---

## 2. Session check (run first on every cron)

```bash
openclaw browser --browser-profile <BROWSER_PROFILE> status
openclaw browser --browser-profile <BROWSER_PROFILE> navigate "https://business.facebook.com/latest/inbox/all/?business_id=<META_BUSINESS_ID>&asset_id=<META_ASSET_ID>"
openclaw browser --browser-profile <BROWSER_PROFILE> snapshot --limit 60
```

Check:
- If `status` is `stopped`: report and stop.
- If the snapshot shows a Facebook login form: session expired, report and stop.
- If the snapshot shows the MBS chrome but with a "Reauthenticate to manage this asset" banner: same — stop and report.
- If the snapshot shows the inbox with conversation list visible: continue.

Never relaunch Chrome from inside a cron.

---

## 3. Phase gating (action-block awareness)

Instagram does not have karma; it has **action blocks** — a tiered penalty system:

- **Phase A** (account < 30 d, OR last 30 d had an action block, OR less than 500 followers): only inbound DM/comment replies inside MBS, **zero outbound actions** (no proactive DMs, no comment-on-other-people's-posts, no following).
- **Phase B** (account ≥ 30 d, no recent block, ≥ 500 followers, no community-guideline flag): all crons authorized.

Always read `<WORKSPACE_DIR>/memory/ig-state.md` at start (last line = current phase).

### Action-block thresholds (observed, not officially published)

| Action | Frequency that triggers a block |
|---|---|
| Follow / unfollow | > 50/day or > 200/week |
| Comment on others' posts | > 30/hr or > 200/day |
| DMs to non-followers (proactive) | > 10/day on a young account |
| Liking | > 60/hr |
| Posting | > 5 posts/24h |

A block lasts 24 h (warning), 7 d (second offense), or **permanent** (third+). The thresholds tighten on Phase A accounts.

### Manual override (advanced)

You can force Phase B by appending `YYYY-MM-DD - phase=B (manual override)` to `ig-state.md`. Use only if the account is grandfathered (verified business, long history, no warnings). Document in `ig-learnings.md`.

---

## 4. Qualification of an inbound DM or comment

A DM or comment is repliable only if **all** of:

- The thread has at least one user-authored message (not a pure share / reel forward — those have no question).
- The user did NOT just receive a templated auto-reply that they haven't acknowledged.
- Phase B authorized for proactive / brand-mentioning replies (see §3).
- The message is a real question or intent in your domain.
- The same user has not been sent a brand-mentioning reply in the last 7 days (`ig-reply-log.md`).

If any check fails: skip. Document why in the recap.

### Special: a user shared a Reel with no message

Default action: **skip silently**. A Reel share without a question is usually a forward to friends; replying creates noise and confuses the conversation.

### Special: existing client recognized

If the user appears in `ig-clients-known.md`: reply with empathy, **do not paste any link**, redirect to the standard support channel (NOT `<PRIMARY_CTA>` which is for prospects).

---

## 5. Reply templates

### Phase A (warming, NO brand mention)

- 1-3 sentences.
- Match the conversation tone.
- No links, no expert-grade advice.

### Phase B (brand-aware, expert)

DM reply (any length, but ≤ 700 chars stays human):
```
[Acknowledge the situation in 1 sentence, neutral tone.]

[General framework in 2-3 short paragraphs.]

[Concrete next step — point to <PRIMARY_CTA>. ONE channel only.]
```

Comment reply (≤ 200 chars, prefix with `@username` to target the parent comment):
```
@username [contextual acknowledgement]. [Indirect signal — "DM us" or "form on profile"].
```

### What never to paste verbatim

- Anything with `[brackets]` left in it (final read-through is mandatory).
- The same opening phrase across more than 2 replies in 7 days.
- A literal URL inside a DM unless it is the `<PRIMARY_CTA>`'s own link AND it is the second message in the conversation (Meta's link-preview takes 1-2 s; if pasted as the first interaction, IG marks it as spam).

### Brand link policy

- Inside a comment body: NEVER paste a URL. "Form on profile" / "DM us" is the only allowed signal.
- Inside a DM: max ONE URL, ONE channel (`<PRIMARY_CTA>`). Never a bit.ly / tinyurl / shortener — IG marks shorteners as spam.

---

## 6. Original posting cadence

Out of scope for the live reactive crons. Recommended rhythm for a Phase B account:

- **Reels**: 3-5/week. Hook in first 1.5 s. Vertical 9:16. Native sound or licensed library only.
- **Carousels**: 2-3/week. Educational, multi-slide. Drives saves (the strongest ranking signal).
- **Stories**: 3-7/day. Reuse top reel hooks. Polls + sticker engagement = strong reach signal.
- **Lives**: ad hoc, max 1/week. Plan, don't ad-lib.
- **Static feed posts**: out, except for branded covers.

Hashtag discipline (Reels + posts):
- 3-5 hashtags per post (the "30 hashtags" old advice is dead — IG reduced the cap and over-tagging looks spammy).
- 1 broad + 2-3 niche + 1 micro (< 50k posts).
- Re-check the `<WORKSPACE_DIR>/memory/ig-hashtag-state.md` registry monthly for shadowbanned tags.

---

## 7. Quotas (hard limits)

| Action | Phase A limit | Phase B limit |
|--------|---------------|---------------|
| DMs handled (inbound replies) per 24 h | 20 | 60 |
| DMs handled per cron run | 4 | 8 |
| Comment replies handled per 24 h | 30 | 100 |
| Comment replies handled per cron run | 5 | 10 |
| Outbound DMs / day (to non-followers) | 0 | 5 |
| Follows / day | 5 | 20 |
| Unfollows / day | 5 | 20 |
| Likes per hour | 30 | 60 |
| Actions in same conversation | min 60 s apart | min 30 s apart |
| Actions globally | min 30 s apart | min 15 s apart |

Quota tracking: read `ig-reply-log.md` at start of every run, count entries in the last 24 h, abort early if quotas already met.

---

## 8. Anti-spam triggers

### Content

| Avoid | Use instead |
|-------|-------------|
| "Check link in bio" repeated | (mention bio at most once per conversation) |
| `<BRAND_NAME>` more than once per reply | (max one mention) |
| "DM me", "WhatsApp me", "click here" stacked | (one CTA, one channel — `<PRIMARY_CTA>`) |
| Phone numbers, emails | (never in comment bodies; OK in DM tail if user explicitly asked) |
| Emojis in regulated / sober niches | (drop them) |
| All caps for emphasis | (use sparingly) |
| Shorteners (bit.ly / tinyurl) | (use the full canonical URL) |

### Behavioral

- Replying within 30 s of a comment going live → bot-like; wait ≥ 2 min.
- Same opening phrase across multiple replies → flagged. Vary the first 1-2 words.
- > 6 actions in 10 min → rate limit on that role.
- Following + liking the same user's last 5 posts within 1 min → instant action block.
- Sending the same DM body to > 3 users in 24 h → "Action blocked" toast within minutes.

---

## 9. Operational flow inside Meta Business Suite

Reactive DM + comment ops run inside MBS exclusively. The flow below is validated end-to-end.

### DM check / reply (validated)

URL: `https://business.facebook.com/latest/inbox/all?business_id=<META_BUSINESS_ID>&asset_id=<META_ASSET_ID>`

1. Pre-flight session check (see §2).
2. Navigate to the `all` tab. Wait 5 s for the conversation list to render.
3. **Filter for unread** by clicking the "Unread" filter chip, or query the conversation list for nodes with the unread badge.
4. For each unread conversation, top-to-bottom:
   a. Click the conversation tile (the user's name).
   b. **Read the entire message thread** for context — IG conversations often span across the auto-template + user's real reply.
   c. Qualify (see §4). If skip-eligible, click the next conversation.
   d. **Click the textbox**: selector `[contenteditable='true']` or `[aria-label*='Reply'], [aria-label*='Répondre']`.
   e. **Type the message** via Playwright `type` (or `evaluate` with `document.execCommand('insertText', false, msg)` ONLY if `contenteditable` is a vanilla React-controlled input — verify first).
   f. **Press Enter** to send. Do NOT click "Send" — there are visual duplicates of the send button and a Playwright `click` sometimes lands on the wrong one. Enter is unambiguous.
5. After sending, the textbox empties; verify before moving to the next conversation.
6. After processing all unread, switch to the `Messenger` tab and to the `Instagram` tab in turn to catch any FB-only or IG-only inboxes that didn't surface in `all`.

### Comment reply (validated — partial)

URL: `https://business.facebook.com/latest/inbox/instagram?business_id=<META_BUSINESS_ID>&asset_id=<META_ASSET_ID>`

The comments tab is **less stable than DMs** — see "Known issue" below.

1. Navigate to the comments tab. Wait 5 s.
2. Posts with new comments appear in the left rail with an unread badge.
3. For each post:
   a. Click the post tile.
   b. Comments render in the right pane.
   c. For each lead-qualified comment:
      - **Find the page-level "Ajoutez un commentaire..." / "Add a comment..."** textarea **at the bottom** of the right pane.
      - Type `@username your reply` (the `@username` prefix targets the parent comment without clicking "Reply").
      - **Click the send-arrow button** (SVG arrow to the right of the textarea) — Enter does NOT submit a comment in this UI.

### Known issue: do NOT click "Reply" on comments

Clicking the "Reply" affordance under a comment navigates the right pane to a different post (Meta's SPA bug, present in 2025-2026). The validated workaround is `@username` prefix + page-level textarea + send-arrow click — described above.

If you must produce a true nested reply (rare): open the post URL on `instagram.com` in a separate ig-engage tab, reply there manually, then mark the conversation done in `ig-reply-log.md`. Do not script the `instagram.com` reply path — Instagram's anti-automation is much tighter than MBS.

### Selectors quick-reference

| Element | Selector |
|---|---|
| DM textbox | `[contenteditable='true']` or `[aria-label*='Reply'], [aria-label*='Répondre']` |
| DM send (preferred) | `press Enter` |
| Comment textarea | `textarea[placeholder*='comment'], textarea[placeholder*='commentaire']` |
| Comment send | the SVG arrow button to the right of the textarea — `[aria-label*='Send'], [aria-label*='Envoyer']` |
| Conversation tile | `text=<user's display name>` |
| Tab "Messenger" | `text=Messenger` |
| Tab "Instagram" | `text=Instagram` (the DMs tab) |
| Tab "Commentaires Instagram" | `text=Instagram` (in comments URL — same string, different URL) |
| Unread filter chip | `text=Unread, text=Non lu` |

### Exit codes (recommended convention)

| Code | Meaning | Recap action |
|------|---------|--------------|
| 0 | Replies sent, verified | `status: ok` |
| 1 | Fatal error (selector missing, MBS error toast) | `status: error`, attach screenshot |
| 2 | "Action blocked" / "Try again later" toast | `status: blocked`, flip the role to Phase A pause |
| 3 | Session expired (login form rendered) | `status: blocked`, alert user |
| 4 | Comment "Reply" caused page navigation (known bug — see above) | `status: partial`, log for manual review |

### Gotchas

- **The MBS comment-Reply navigation bug**: still present. Use the `@username` workaround.
- **Localized labels**: `Reply` / `Répondre`, `Send` / `Envoyer` — maintain a label map and try both in selectors.
- **MBS soft logout**: after ~48 h of inactivity, MBS asks for re-authentication on next navigation. Treat as session expired (exit 3).
- **Tab switching**: if you operate on multiple tabs (`all`, `messenger`, `instagram_direct`), wait ≥ 3 s after switching — MBS re-fetches the conversation list and clicking too early lands on stale tiles.
- **The `Non Lu` / `Unread` filter chip is sometimes mis-clicked**: it has a transparent overlay. Snapshot before clicking.
- **Cron timeout**: bump to ≥ 1200 s. MBS pages can take 4-6 s to render fully.

---

## 10. Account state management

File: `<WORKSPACE_DIR>/memory/ig-state.md`

For each day:
- Phase (A / B).
- Followers count.
- Last action-block timestamp + duration.
- Last community-guideline notice.
- Posts published today (cap at 5/24h per §6).

File: `<WORKSPACE_DIR>/memory/ig-clients-known.md`

For each existing client:
- IG handle.
- Last contact date.
- Sensitive flag (do-not-paste-CTA).

Update at the end of every run.

---

## 11. Recovery & blockers

| Issue | Action |
|-------|--------|
| `status: stopped` | Report, stop. |
| Login form rendered on MBS | Session expired, alert, stop. |
| "Reauthenticate to manage this asset" banner | Same as login expired. |
| "Action blocked — try again later" toast | Flip the role to Phase A pause for 24 h. Alert. |
| "Please verify it's you" / re-captcha | Stop. Never auto-solve. Alert for manual login. |
| MBS shows "Something went wrong" generic error | Refresh once. If persists, stop and alert. |
| Comment "Reply" click navigated to wrong post | Mark exit 4, fall back to manual via `instagram.com`. |
| Followers drop > 5 % overnight | Likely shadowban — flip to Phase A, alert. |
| Two consecutive comments removed within < 10 min of post | Auto-freeze comment cron for 6 h. |

---

## 12. Mandatory recap (alert channel + memory)

At the end of each cron:

**Alert channel — final run message**:
```
[Job name] — [status: ok|partial|blocked|skipped]
DMs handled: [N or "—"]
Comments handled: [N or "—"]
Hot leads: [list short OR "—"]
Phase: [A|B]
Blockers: [text OR "—"]
Next action: [1 line]
```

**Memory** — append to `<WORKSPACE_DIR>/memory/ig-recaps.md`:
```
## YYYY-MM-DD HH:MM TZ — <job-id> — status: <status>
- Job: <description>
- Phase: A|B
- DMs sent: <N>
- Comments sent: <N>
- Hot leads: <list or "—">
- Blockers: <text or "—">
- Next useful action: <1 line>
```

---

## 13. Memory files inventory

Located at: `<WORKSPACE_DIR>/memory/`

| File | Purpose | Update cadence |
|------|---------|----------------|
| `ig-recaps.md` | Per-run logs | Every cron run |
| `ig-post-log.md` | Reels + carousels + stories (URL, type, date, reach) | Each posting run |
| `ig-reply-log.md` | DM + comment replies sent | Each reply pass |
| `ig-state.md` | Daily phase + followers + warning flags | Daily Metrics Recap |
| `ig-hashtag-state.md` | Per-hashtag reach + shadowban check | Weekly |
| `ig-clients-known.md` | Existing clients to NEVER pitch | Ad hoc |
| `ig-ideas.md` | Content backlog | Weekly Planning |
| `ig-learnings.md` | Patterns (what reached, what got removed) | Weekly + ad hoc |
| `ig-alerts-sent.md` | Anti-doublon hot-lead alerts | Each alert |

---

## 14. Account identity guardrails

- Handle: brand-aligned but not aggressively promotional (`@drsmithlegal` > `@bestlawyerinparis`).
- Bio: one line + the single `<PRIMARY_CTA>` link. No emojis, no flag salad in regulated niches.
- Never reply to a DM that asks for expert-grade advice on a specific case — redirect to `<PRIMARY_CTA>`.
- Never share private client details, names, or numbers.
- Never reuse strict CRM templates as IG content.
- Never promise an outcome ("you will win").
- Never charge or solicit payment in DM.
- If asked "are you a bot?": one sober, ambiguous line, then redirect. Do not confirm AI.

---

## 15. Phase A → Phase B transition

When the Daily Metrics Recap detects (account_age_days ≥ 30) AND (followers ≥ 500) AND (last_action_block_days_ago > 30):

1. Append to `ig-state.md`: `YYYY-MM-DD - phase=A - PHASE_B_THRESHOLD_REACHED`.
2. Send a distinct alert: `🎉 IG account ready for Phase B — review and flip outbound crons manually`.
3. Manual user flip (no auto-flip).
4. First week of Phase B: cap reply pass at **3 replies/run** (not 8).
5. Daily check on `Action Status` (MBS → Settings → Account Status). Any "warning" reverts to Phase A.

---

## 16. Stability discipline

- Read the UI before clicking.
- One click → verify with a snapshot.
- Switch tabs only after the previous tab settled.
- Close stale tabs at the end of every run.
- Never fake a successful reply — always verify the message landed in the thread.

**Better silence than spam. Better a blockage report than a fake success.**

---

## 17. First-run checklist

- [ ] Section 0 placeholders filled.
- [ ] IG account is **Business** or **Creator**, linked to a Meta Business Suite asset.
- [ ] `<META_BUSINESS_ID>` and `<META_ASSET_ID>` extracted (open MBS, copy from the URL).
- [ ] Bio is one line + single `<PRIMARY_CTA>` link.
- [ ] Browser profile launched at `http://127.0.0.1:<BROWSER_PORT>` and logged into facebook.com (the MBS gate).
- [ ] Navigating to `inbox/all` renders the conversation list (no login form, no setup wizard).
- [ ] `<WORKSPACE_DIR>/memory/` exists with the 9 memory files.
- [ ] Alert channel webhook tested.
- [ ] Phase A confirmed: only inbound DM cron enabled.
- [ ] At least 14 days of manual posting + manual replies before turning on the cron.
- [ ] Account Status checked (MBS → Settings → Account Status): **green / no warning**.

Init memory:

```bash
mkdir -p "<WORKSPACE_DIR>/memory" && cd "$_" && touch ig-recaps.md ig-post-log.md ig-reply-log.md ig-state.md ig-hashtag-state.md ig-clients-known.md ig-ideas.md ig-learnings.md ig-alerts-sent.md
```

---

## 18. FAQ

**Q: Do I need OpenClaw to use this skill?**
A: No. OpenClaw browser CLI is the example stack — the doctrine works with Playwright (Node or Python), Puppeteer, Chrome MCP, or any CDP-capable tool.

**Q: Can I just use the Instagram Graph API?**
A: Partially. The Graph API covers `instagram_basic`, `instagram_manage_messages`, `instagram_manage_comments` — if you have an approved app, you can build a more robust webhook-based flow. The doctrine in this skill is the **fallback for accounts not yet approved for Graph API access, or for cases where MBS UI features are needed** (labels, prospect stages, link previews).

**Q: What about multi-account?**
A: Clone the workspace dir per account. Use a separate browser profile + port. **Each IG account must have its own Meta Business asset** — you can manage multiple assets from one MBS, but they have distinct `<META_ASSET_ID>` values.

**Q: My account got an action block during testing. What now?**
A: Stop everything. Flip to Phase A. Manual usage only for 7-14 days. Document in `ig-learnings.md` the exact last 20 actions. Do NOT appeal automatically.

**Q: Does the doctrine cover Reels Ads / Boost / Shopping?**
A: No. This skill is for organic + reactive ops only. Ads have a separate dashboard and a separate (different) sanction pattern.

**Q: What's the most common reason this skill's crons get flagged?**
A: Same opening phrase across replies. Vary the first 1-2 words every time. The second most common: replying within 30 s of a comment landing — wait ≥ 2 min.

**Q: What if my account is suspended (not just action-blocked)?**
A: Stop everything. Do not appeal automatically — Instagram's appeal flow is sensitive to repeated automated submissions. Manual review only. Document the exact last 20 actions before the suspension in `ig-learnings.md`.
