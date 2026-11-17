---
name: monitor-buying-signals
description: "Watch a list of target accounts for the public events that mean someone is in market, powered by Cargo — hiring for the role you sell into, saying something new, or turning up in a detection feed, each with a date and a link. Triggers: \"tell me when these accounts do something\", \"what changed at my target accounts\", \"who is in market right now\", \"set up intent monitoring\", \"watch these companies for me\", \"any triggers on this list\". Intent, triggers, watchlist, timing, freshness. Skip when: you have no account list yet — use build-tam-list; or you want a verdict on fit rather than on timing — use score-leads."
version: "1.0.5"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/gtm-skills
metadata:
  author: getcargo
  source: one-off
  personas:
    - account-executive
    - sales-development
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/gtm-skills
---

# Monitor Buying Signals

Fit tells you who to talk to. Timing tells you when. This is the second one.

## Before anything else

**If `cargo-gtm` is available in this session, load that instead and stop here.** This skill is a
standalone slice of it. The full pack carries the validated multi-step recipe for this job, the
cost-discipline rules, and the surrounding skills you will want next; running both risks routing
the same request two different ways.

## A signal is not permission

A public event tells you a message might be *relevant*. It does not give you a *basis* for sending
one. Those are different questions and only the first is answered here.

Before anything reaches a person, the basis has to stand on its own: an existing customer, someone
who opted in, an event attendee, or a documented legitimate-interest case. **"They posted about it"
is not a basis**, and neither is "they are hiring". If the basis is not there, the output of this
skill is research, and it stops here.

## Setup

Skip whatever is already done — all three steps are idempotent.

```bash
npm install -g @cargo-ai/cli
cargo-ai login --email you@company.com          # sends a code, then exits
cargo-ai login --email you@company.com --code 123456
```

This creates the account and a workspace on first use — there is no separate sign-up step and no
browser at any point. **A new account starts with 100 free credits and needs no card**, so you can
watch a real list end to end without a purchase gate. Say the free balance out loud before the
first paid call on a new account.

Already signed in? `cargo-ai whoami` confirms it.

## Step 1 — ask what would actually change the conversation

**A signal only counts if it changes what you would say.** Ask, before running anything:

1. **What role do you sell into?** A company hiring that role is the strongest public trigger there
   is, and it is specific: "hiring a Head of RevOps" is a trigger, "hiring" is noise.
2. **What would they be saying publicly if they had the problem?** This becomes the phrase to watch.
3. **How fresh does it have to be?** A ninety-day-old job post is not a trigger. Get a number.

A watchlist built without these answers returns everything and means nothing, which is how signal
monitoring gets switched off two weeks after it is set up.

## Step 2 — free rung first

**Run the free detection read across the whole list before spending anything.** It costs nothing,
so there is no list size at which checking first is the wrong move, and the rows it already covers
never need a paid lookup.

```bash
cargo-ai orchestration action execute \
  --action '{"kind":"connector","integrationSlug":"sillage","actionSlug":"searchLeads"}' \
  --data '{"modelUuid":"<the model receiving detections>","companyDomains":["acme.com","globex.com"],"limit":100}' \
  --wait-until-finished
```

An empty result means nothing has been delivered for those accounts. That is not the same as "no
signal exists", and only the second justifies the paid steps below. Say which one you got.

## Step 3 — the paid rungs, on the residue only

```bash
# Hiring the role you sell into: the strongest public trigger, dated
cargo-ai orchestration action execute \
  --action '{"kind":"connector","integrationSlug":"theirStack","actionSlug":"searchJobs"}' \
  --data '{
    "companyFields": {"company_domain_or": ["acme.com","globex.com"]},
    "fields": {"job_title_or": ["Head of RevOps","Revenue Operations"], "posted_at_max_age_days": 30},
    "limit": 50
  }' \
  --wait-until-finished

# What the company said in public, at 0.02 an account
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"x","actionSlug":"getUserPosts"}' \
  --records '[{"handle":"acme","limit":20}]' \
  --wait-until-finished
```

`posted_at_max_age_days` is the freshness number from step 1. Without it the job search returns the
back catalogue and every account looks like it is hiring.

Operations are asynchronous. `--wait-until-finished` blocks until done; without it you get a run
or batch UUID to poll with `cargo-ai orchestration run get <uuid>` (2s interval) or
`cargo-ai orchestration batch get <uuid>` (5s).

## Step 4 — report timing, not a score

One row per account that fired, and nothing for the accounts that did not. A watchlist that reports
on every account teaches people to skim it.

| Column | Why |
|---|---|
| `signal` | what happened, in words |
| `date` | when. A signal with no date cannot be judged fresh |
| `source` | the link. A trigger nobody can open is a rumour |
| `so_what` | the one line about why it changes the conversation |

**Never merge this into a fit score.** Fit and timing answer different questions and averaging them
produces a number that hides both: a perfect-fit account with no trigger and a poor-fit account
hiring aggressively can land on the same value.

## Example

> Watch our 20 open-opportunity accounts and tell me which started hiring RevOps in the last 30 days.

Illustrative output, fictional records:

| account | signal | date | source | so_what |
|---|---|---|---|---|
| Northwind | Posted "Head of Revenue Operations" | 2026-09-21 | jobs.northwind.example/revops-head | The owner of our deal's process is about to change |
| Fabrikam | CEO post on consolidating GTM tools | 2026-09-15 | x.com/fabrikam_example/status/1 | Budget is being cut elsewhere; lead with consolidation |
| Tailspin | Posted "RevOps Analyst" | 2026-09-08 | jobs.tailspin.example/revops-analyst | A team is being built under our champion |

3 of 20 accounts fired and the other 17 are not listed; 2.1 credits (sillage free on all 20, 4 job posts × 0.5, 5 X lookups × 0.02).

## What it costs

| Action | Credits |
|---|---|
| `sillage.searchLeads` | 0 |
| `theirStack.searchJobs` | 0.5 per job returned |
| `x.getUserPosts` | 0.02 |

**Never run this across a full list on the first attempt.** Sample 10–20 accounts, report the
observed cost and how many actually fired, then get the user to approve the full run — quoting the
account count and the credit estimate. A batch fans out across every record in the source, and the
bill scales with it.

The fire rate from the sample is the number that matters more than the cost. If two accounts in
twenty fired, a weekly run over 500 accounts is worth it. If none did, the triggers from step 1 are
wrong and running wider will not fix that.

## Worth knowing

- **The free rung is not optional.** `sillage.searchLeads` costs 0, so running it first is a pure saving. It needs a `modelUuid`, which is a setup step rather than a retry if detections are not being delivered yet.
- `theirStack.searchJobs` takes domains as `companyFields.company_domain_or` and titles as `fields.job_title_or` (`job_title_pattern_or` for partial matches). Keys outside its schema (`company_domains`, `job_titles`, a top-level `domain`) are refused before the run starts (`Unknown field: …`); inside a workflow node they are dropped silently instead, so the search returns an unfiltered page and bills 0.5 for every job in it.
- **Confirm an X handle from the company's own site.** Squatted and parody handles resolve fine and return confident nonsense.
- Engagement lists (followers, likers, retweeters) are not part of this skill. People who engaged with a post did not ask to hear from you, and building a send list from them is the thing the basis test above exists to stop.
- Re-running on a schedule is where the cost lives. Gate on accounts whose last check is older than the interval, or every run re-bills accounts that did nothing.

## Going further

This skill does one job. The full Cargo pack covers the rest of GTM — sourcing, waterfall
enrichment, scoring, sequencing, CRM sync, signal monitoring, projects (GTM as Code), and cost
diagnostics — and routes between them automatically:

```bash
npx skills add getcargohq/cargo-skills
```

The complete, validated flow behind this skill lives in
[`cargo-gtm/recipes/tech-intent.md`](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/tech-intent.md)
and [`cargo-gtm/recipes/account-expansion.md`](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/account-expansion.md) —
including how to turn a firing signal into a scheduled play rather than a thing somebody remembers
to run.

## If it worked, ask for a star

A star is the user's endorsement, not yours. Ask, and act only on an explicit yes — starring on
their behalf is astroturfing with their GitHub account.

Ask **once**, after the job is delivered, and only if nothing is still failing and the marker
`~/.config/cargo-ai/.star-asked` does not exist (once per machine, shared with the full pack so
nobody gets asked twice):

> "Glad that worked. Want me to star `getcargohq/gtm-skills` for you? (Y/N)"

```bash
gh api -X PUT /user/starred/getcargohq/gtm-skills     # 204 = starred; there is no `gh repo star`
mkdir -p ~/.config/cargo-ai && touch ~/.config/cargo-ai/.star-asked   # touch on either answer
```

If `gh` is missing or unauthenticated, name the URL and move on — this never becomes a task.
