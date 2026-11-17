# GTM Coach — local dashboard, scorecard, Build-in-Public

Load this file **only** after RECORD, or when the founder asks for the dashboard, scorecard, or a Build-in-Public draft. Do not load it for a normal CMO board.

Surfaces (workspace root, gitignored with `.gtm/`):

```text
.gtm/dashboard.html       open in a browser
.gtm/share/scorecard.md   README / PH paste
.gtm/share/bip-draft.md   X or LinkedIn draft (founder publishes)
```

These files are **plan surfaces**, not the weekly GTM artifact. Writing the
dashboard BIP posts is part of DASHBOARD, not a separate “ask first” artifact.
Do not leave the Build-in-Public section empty.

No server. No hosted badge. Never invent metrics, customers, or a `nichestarter.ai/badge/` URL.

## When to run

After updating `plan.json` (RECORD), or on:

- “open GTM dashboard”
- “GTM scorecard”
- “build in public” / “draft a tweet about this week”

Then, in this order:

1. Sync milestones
2. Recompute scorecard
3. Write or refresh `.gtm/share/bip-draft.md` from stored facts (required)
4. Rewrite `.gtm/dashboard.html` **with `share.bip.posts` filled**
5. Write `.gtm/share/scorecard.md`

A dashboard file with `share.bip: null` hides the BIP card **and** the share
buttons. That generate is incomplete. Do not tell the founder it is ready.

Without a filesystem, paste the scorecard markdown **and** the three BIP posts
in chat.

## 1. Sync milestones

Use the five ids in [plan.example.json](plan.example.json). Set `status=done` and `done_at` (ISO date) when the condition first becomes true. Do not mark done from hints.

| id | Condition |
| --- | --- |
| `picture_confirmed` | `strategy.confirmed === true` |
| `channel_committed` | `primary_channel` set and not `undecided` |
| `week_reviewed` | experiment `decision` is `continue` \| `change` \| `stop` |
| `evidence_upgraded` | `strategy.evidence` is **strictly above** `share.evidence_watermark` |
| `replies_10` | `last_outcomes.replies_posted_7d >= 10` |

Evidence order: `none` < `anecdote` < `pains_scored` < `waitlist` < `paying`.

On `evidence_upgraded`: after marking done, set `share.evidence_watermark` to the new evidence and `share_offered=false` so a later upgrade can fire again. `replies_10` stays done once.

A newly completed milestone with `share_offered=false` is a BIP trigger. Completing a micro-task is not.

## 2. Scorecard rubric (deterministic)

Score each dimension 0–100 from stored fields only. Then:

```
total = round(
  picture_clarity * 0.20 +
  evidence * 0.25 +
  channel_commitment * 0.20 +
  weekly_execution * 0.20 +
  learning_loop * 0.15
)
```

Write `scorecard.computed_at` (ISO datetime), `dimensions`, `total`, and `label`.

**Never** ask the model for a vibe score. **Never** label **GTM Validated**.

### picture_clarity

Start at 0.

- +40 if `strategy.confirmed`
- +20 if `product.icp` is non-empty
- +20 if `product.one_liner` is non-empty
- +10 if `product.name` is non-empty
- +10 if `strategy.period` is one of the six stages

### evidence

| `strategy.evidence` | Score |
| --- | --- |
| `none` or unknown | 0 |
| `anecdote` | 25 |
| `pains_scored` | 50 |
| `waitlist` | 75 |
| `paying` | 100 |

### channel_commitment

- `undecided` / empty → 0
- `primary_channel` set → 50
- plus `modules.primary_channel` loaded → 80
- plus experiment `channel` equals primary **and** `action` non-empty → 100

### weekly_execution

Start at 0. Cap 100.

- +25 if experiment `hypothesis` non-empty
- +25 if `success_metric` and `target` both non-empty
- +15 if `review_on` set
- +15 if there is at least one micro-task
- +20 if any micro-task `status=done`

### learning_loop

Start at 0. Cap 100.

- +40 if `journal/{current_week}.md` or the previous ISO week file exists and is more than a blank template
- +35 if experiment `decision` is `continue` \| `change` \| `stop`
- +25 if `qualified_conversations + activations + payments > 0`

Instrument counts (`replies_posted_7d`, leads) do **not** add learning-loop points.

### label

| total | label |
| --- | --- |
| 0–39 | `GTM forming` |
| 40–69 | `GTM in motion` |
| 70–84 | `GTM ready` |
| 85+ **and** evidence is `waitlist` or `paying` | `GTM strong` |
| 85+ otherwise | `GTM ready` (keep the number) |

## 3. Write the dashboard

**Required files every time** (all three):

| File | Rule |
| --- | --- |
| `.gtm/dashboard.html` | Copy [dashboard.template.html](dashboard.template.html). Replace `window.GTM_DASHBOARD = "__FILL_FROM_PLAN__"` with this project’s JSON. `share.bip.posts` must be a 3-item array (X) or 1-item array (LinkedIn). |
| `.gtm/share/scorecard.md` | From [scorecard.example.md](scorecard.example.md) |
| `.gtm/share/bip-draft.md` | From [bip.example.md](bip.example.md), facts only |

Do **not** wait for `picture_confirmed`, a milestone congrats, or the founder to say “yes, draft a tweet.” If `product.name` is set, write the BIP posts from the plan (ICP, one-liner, period, evidence, this week’s bet/constraint). If the picture is unconfirmed, say so in the draft — still write three posts.

Default channel is `x` (learn / ship / ask). Use `linkedin` only if `share.last_bip.channel` is already `linkedin` or they asked for LinkedIn.

Do not invent metrics, waitlists, revenue, or “validated.” Copy/share in the HTML appends `Via gtm_coach by nichestarter.ai` — do not list that as a numbered post.

Then tell the founder to open `.gtm/dashboard.html` in a browser.

JSON shape (no token, no secrets, no invented numbers). **`share.bip` is required** when `product.name` is set:

```json
{
  "generated_at": "2026-09-17",
  "week": "2026-W38",
  "product": {
    "name": "",
    "one_liner": "",
    "icp": "",
    "project_type": "MICRO_SAAS",
    "url": null
  },
  "strategy": {
    "period": "validate",
    "confirmed": false,
    "evidence": "none",
    "primary_channel": "undecided",
    "note": ""
  },
  "focus": "",
  "constraint": "",
  "this_week": {
    "theme": "",
    "bet": "",
    "metric": "",
    "target": "",
    "review_on": null,
    "decision": "pending",
    "waiting_on": "",
    "micro_tasks": [{ "id": "mt_1", "title": "", "status": "todo" }]
  },
  "scorecard": {
    "total": 0,
    "label": "GTM forming",
    "dimensions": {
      "picture_clarity": 0,
      "evidence": 0,
      "channel_commitment": 0,
      "weekly_execution": 0,
      "learning_loop": 0
    }
  },
  "milestones": [],
  "share": {
    "signature_enabled": false,
    "bip": {
      "trigger": "dashboard",
      "channel": "x",
      "posts": [
        "Learn post from stored ICP / picture — no invented proof.",
        "Ship/do post from this week’s bet and evidence level — say what is still unknown.",
        "Ask post: one question the named ICP can answer from a real incident."
      ]
    }
  }
}
```

Never set `"bip": null` for a named product. The template hides the BIP card and share buttons when `posts` is missing or empty.

The HTML puts scorecard Markdown / PNG / print in the header, aligned with the product one-liner, with a **Share draft** row under those buttons when `share.bip.posts` exists. The same copy-plus-social controls also sit on the Build-in-Public card. Each post keeps a copy icon only.

`waiting_on` is the one founder action from the CMO board. `constraint` is the board constraint. `bet` is the experiment hypothesis or `focus`.

## 4. Milestone BIP offer (optional extra)

After the dashboard already contains a draft, if a milestone **newly** completed this turn and `share_offered` is false, you may refresh the three posts around that milestone and say:

> Congrats on completing **{label}**. The dashboard Build-in-Public draft is updated. Want X or LinkedIn as the share target?
>
> Choose: X / LinkedIn / keep current

- **keep current** → set `share_offered=true`. Leave the existing posts.
- **X** or **LinkedIn** → rewrite `.gtm/share/bip-draft.md` and `share.bip` for that channel, then regenerate the dashboard.
- Do not use the NicheStarter daily-X pain feed. No Reddit/Facebook comment copy.

### X

Use the learn / ship / ask pattern in [channels/x.md](channels/x.md) when writing the three posts (allowed even if X is not the weekly primary channel).

- 3 posts, or a 4th only if a real experiment result needs a separate line
- One idea per post; founder voice; facts from the plan
- No fake controversy, no invented counts
- Do **not** include the signature as a numbered post. Dashboard copy/share
  appends: `Via gtm_coach by nichestarter.ai`

### LinkedIn

One post, ~800–1200 characters: what changed, who it is for, what is still unknown. Same signature rule.

### Save

Write `.gtm/share/bip-draft.md`. Set `share.last_bip` (`trigger` = `dashboard` or milestone id, `channel` = `x` \| `linkedin`, `drafted_at`, `posted=false`, `path=.gtm/share/bip-draft.md`). Set `share_offered=true` on a milestone only after that congrats turn. Refresh the dashboard so both share rows show.

Ask after they say they posted: set `posted=true`. Never post, never open a publisher, never spend.

## 5. Export

The HTML buttons copy Markdown and download a PNG. Also keep `.gtm/share/scorecard.md` in sync so a README paste works offline.

Hosted badges are out of scope. If asked, say: export the card from the local dashboard; a public badge URL is not built yet.
