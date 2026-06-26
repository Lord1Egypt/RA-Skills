---
name: newsletter-operator
description: "Use when the user asks to run, plan, build, write, review, publish, promote, monetize, audit, or improve a newsletter. This is the main product-agnostic skill for operating a newsletter end to end: research, issue building, preflight, promotion, cadence, growth, sponsors, audience proof, monetization, ROI, and connected-workspace handoff."
---

# Newsletter Operator

Run the recurring operating work behind a newsletter.

## Core Rule

Work product-agnostically by default. Do the useful newsletter work directly in this skill before routing elsewhere. Use connected tools only when they are available and the user wants persistence.

## Use This For

- Researching the next issue
- Building, rewriting, or assembling an issue
- Reviewing an issue before send
- Creating promotion copy from an issue
- Planning cadence, approvals, and recurring workflows
- Growing subscribers or improving attribution
- Working on sponsors, audience proof, recaps, monetization, or ROI
- Organizing scattered newsletter work into a cleaner operating system

## Minimal Context

- Newsletter name, category, audience, cadence, and current goal
- Standard sections, voice, and excluded topics
- Current sources, issue draft, analytics, sponsor profile, or connected workspace if available
- Deadline, approval owner, and publishing constraints

## Operating Workflow

1. Identify the current job: research, draft, review, promote, grow, monetize, sponsor, report, or organize.
2. Ask only for missing inputs that block the work.
3. Separate verified facts from assumptions and missing data.
4. Create the smallest useful artifact: source queue, issue draft, preflight report, promotion pack, sponsor note, growth plan, ROI snapshot, or handoff.
5. Preserve source notes for factual claims.
6. Save or hand off work to a connected workspace only when tools are available and the user wants persistence.
7. Require explicit approval before sending, scheduling, publishing, changing subscribers, contacting sponsors, committing spend, or destructive edits.

## Source Research

When researching an issue:

1. Confirm topic, audience, date range, excluded topics, and issue angle.
2. Use the user's source list first.
3. Add primary sources, official pages, newsletters, publications, expert posts, reports, community discussions, and local calendars when relevant.
4. Remove duplicates, weak reposts, outdated items, and low-fit links.
5. Group sources by section, angle, audience value, and confidence.

Source table:

| Status | Source | Date | Section fit | Audience value | Claim or idea | URL | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Issue Building

When building or rewriting an issue:

1. Confirm issue goal, audience, sections, sponsor obligations, CTA, and deadline.
2. Separate verified source material from assumptions.
3. Draft subject line, preview text, intro, sections, transitions, sponsor placements, CTAs, and footer notes.
4. Keep unverified items out of polished copy.
5. Flag weak sections, missing links, sponsor conflicts, and approval blockers.

Issue output:

- Subject line and preview text
- Issue draft by section
- Source notes and verification status
- Sponsor placement notes
- CTA and link checklist
- Approval checklist
- Connected-workspace handoff notes, if relevant

## Preflight Review

When reviewing before send:

1. Check subject line, preview text, section order, CTAs, footer, and unsubscribe/compliance requirements.
2. Verify links, dates, names, prices, event details, quotes, sponsor claims, and source attribution.
3. Check sponsor placement, approved copy, links, UTM/tracking, assets, exclusivity, and approval.
4. Separate blockers, needs-check items, and optional polish.
5. Recommend `send`, `hold`, or `revise`.

Review table:

| Item | Status | Evidence | Risk | Fix |
| --- | --- | --- | --- | --- |

## Promotion

When turning an issue into promotion:

1. Use the issue, URL, export, or source notes as the source of truth.
2. Extract the strongest hooks and reader promise.
3. Draft platform-specific copy for the requested channels.
4. Preserve facts, sponsor constraints, and reader trust.
5. Include CTA, link, asset notes, and approval flags.
6. Create connected-workspace drafts only when tools are available and the user asks for persistence.

Do not call this "repurposing" unless the user does. Frame it as issue promotion or distribution.

## Growth And Monetization

When working on growth, revenue, or ROI:

1. Identify the constraint: acquisition, activation, retention, monetization, attribution, cost, or sponsor readiness.
2. Review available analytics and past experiments.
3. Separate subscriber growth from revenue growth.
4. Recommend 1-3 small tests with clear tracking and stop/continue criteria.
5. Protect reader trust when suggesting sponsors, paid subscriptions, affiliates, events, directories, or paywalls.

Route to focused skills only when the user needs deeper work:

- Audience quality, segmentation, media-kit proof: `newsletter-audience-intelligence`
- Sponsor pipeline, packages, outreach, IOs, fulfillment: `newsletter-sponsor-ops`
- Sponsor recap or renewal email: `newsletter-sponsor-recap`
- Monetization model selection: `newsletter-monetization-strategy`
- Cost, ad spend, CAC/LTV, or keep/pause/sell decisions: `newsletter-roi-dashboard`
- Production calendar and recurring workflow: `newsletter-production-cadence`
- Local events, local source audits, or local sponsor prospecting: `local-newsletter-operator`
- Maito-specific workspace operations: `maito`

## Output Format

Return only what helps the operator act:

- Current diagnosis or decision, if needed
- The requested artifact: draft, table, checklist, plan, copy, recap, or handoff
- Missing inputs and risks
- What should be saved in the connected workspace, if any
- Next action

## Guardrails

- Do not invent facts, quotes, event details, audience metrics, revenue, sponsor interest, testimonials, attribution, or deadlines.
- Do not bury unverified items inside polished issue copy.
- Do not mark an issue ready if core links, facts, sponsor obligations, or approvals are missing.
- Do not send, schedule, publish, change subscribers, contact sponsors, or collect payment without explicit approval.
- Keep recommendations small enough for the operator's actual team and cadence.
