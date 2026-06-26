---
name: popular-skill-scout
description: Find popular and practical skills across ClawHub and GitHub. Use when the user asks for hot skills, useful skills, ClawHub recommendations, GitHub skill discovery, or wants a shortlist of skills that are both installable and worth trying for a concrete workflow.
---

# Popular Skill Scout

Find shortlist-quality skill recommendations instead of dumping search results.

Use ClawHub for candidate discovery and GitHub for maintenance validation.

## Search media priority

Use these media in this order:

1. ClawHub website pages
2. GitHub website pages
3. ClawHub CLI such as `npx clawhub search`
4. Other skill directories and marketplaces
5. General web search only as fallback

Do not rely on memory for popularity or freshness when a live source is available.

## Workflow

1. Identify the actual use case before searching.
2. Search ClawHub first for direct candidates and current popularity signals.
3. Search GitHub next to verify maintenance, source quality, and installation realism.
4. Verify each candidate for reliability, accuracy of claims, and credible upstream source before it is shown to the user.
5. Rank only the verified candidates by usefulness first, then popularity, then maintenance, then safety.
6. Return a short, opinionated shortlist with caveats.

## Step 1: Lock the target job

Convert vague asks like "find good skills" into a concrete job:

- coding productivity
- repo understanding
- browser automation
- file handling
- document analysis
- personal workflow automation

If the user already named a task, do not broaden it unnecessarily.

If the user explicitly specifies a skill type or domain, keep the search constrained to that type and still apply the same verification, upstream checking, and final recommendation process.

## Step 2: Search ClawHub

Prefer the browser path because ClawHub exposes installs, stars, suspicious flags, version count, and detail pages in one place.

Use the search and sort workflow in [references/sources-and-queries.md](./references/sources-and-queries.md).

Start with targeted query families instead of random keywords. Reuse the keyword templates in [references/query-templates.md](./references/query-templates.md).

While reviewing ClawHub results:

- keep `nonSuspicious=true` when possible
- check both `Installs` and `Stars`
- open detail pages for the top few candidates
- reject skills with vague summaries, undeclared runtime needs, or conflicting install instructions
- treat security warnings as hard negatives unless the user explicitly wants to inspect risky skills

## Step 3: Search GitHub

Use GitHub as a second-pass validator, not the primary ranking source.

Look for:

- a real `SKILL.md`
- active maintenance
- clear installation or usage guidance
- coherent repository scope
- evidence the skill is not abandoned boilerplate

Prefer repositories with recent commits, readable docs, and a focused purpose. Do not overvalue GitHub star count if the repo is stale or generic.

If you cannot identify a credible GitHub source for a candidate, do not promote it to the strongest recommendation tier unless ClawHub evidence is exceptionally strong and the skill is simple, low-risk, and clearly instruction-only.

Use the search patterns and review checklist in [references/sources-and-queries.md](./references/sources-and-queries.md).

Only fall back to general web search when ClawHub and GitHub do not surface enough signal for a concrete recommendation.

## Step 3.5: Use broader directories as fallback

If ClawHub and GitHub do not produce enough credible candidates, check broader discovery sources listed in [references/sources-and-queries.md](./references/sources-and-queries.md):

- OpenClaw Directory
- LobeHub Skills Marketplace
- community discussions

Use these sources to discover additional candidates, then bring those candidates back through the same GitHub and scoring workflow. Do not recommend a candidate from a secondary directory without validating it.

## Step 4: Verify before showing

Do not show raw search hits as recommendations.

Before a candidate is eligible for the final result, verify:

- the summary matches the detail page
- the claimed capability is specific enough to understand
- the runtime requirements are coherent
- the safety posture is acceptable
- a credible upstream source exists when the skill is substantial

Preferred verification order:

1. ClawHub detail page
2. GitHub repository or upstream source
3. only then final recommendation output

Use these decision rules:

- if the detail page is vague, downgrade or drop
- if the upstream source cannot be identified, keep it out of the strongest recommendation tier
- if the upstream source contradicts the marketplace page, prefer the upstream reality
- if the skill looks like a duplicate wrapper with weak provenance, drop it

## Step 5: Score candidates

Use the rubric in [references/ranking-rubric.md](./references/ranking-rubric.md).

Bias toward practical adoption:

- solves a real repeated task
- low setup friction
- low ambiguity in triggering
- clear boundaries and caveats
- likely to save user time quickly
- low environment coupling

Popularity is useful, but do not recommend a flashy skill over a boring one that is better maintained and easier to use.

## Step 6: Return the shortlist

Return at least 10 candidates when enough credible options exist.

Prefer 10 to 15 candidates for broad discovery requests. Use fewer only when quality would clearly drop.

For each candidate, provide:

- skill name
- what it does in one plain sentence
- source: ClawHub or GitHub
- why it is useful
- popularity signal seen during review
- verification summary
- maintenance or safety note

Prefer this output shape:

### Recommended

- `skill-name`
- what it does: one plain sentence
- source: ClawHub or GitHub
- why it is useful: one short sentence
- popularity: one short line
- verification: one short line
- note: one short line

### Worth inspecting

- `skill-name`
- what it does: one plain sentence
- source: ClawHub or GitHub
- why it is useful: one short sentence
- popularity: one short line
- verification: one short line
- note: one short line

### Skip

- `skill-name`
- what it does: one plain sentence
- source: ClawHub or GitHub
- why it is useful: optional, one short sentence
- popularity: one short line if relevant
- verification: one short line
- note: the reason it should not be recommended now

When useful, expand each item into flat fields:

- skill name
- what it does
- source
- why it is useful
- popularity
- verification summary
- maintenance or safety note

After the final shortlist, add a short next-step suggestion asking whether the user wants a trial install and live verification run for one or more candidates.

## Step 7: Offer trial install and live verification

After presenting the recommendations, offer to validate promising skills in practice.

If the user agrees, the validation goal is:

- install the selected skill
- trigger it with a realistic request
- compare the actual behavior against the skill description
- identify any mismatch, hidden setup friction, or broken assumptions
- summarize practical usefulness so the user can decide whether to keep or remove it

In the validation summary, report:

- what the skill claimed to do
- what happened during real use
- whether the behavior matched the description
- setup friction or hidden requirements
- whether the skill feels practically useful
- suggested keep or remove stance, while leaving the final decision to the user

Example:

### Worth inspecting

`workspace-files`

- what it does: Provides safe workspace-scoped file listing, reading, writing, and file-name search.
- source: ClawHub
- why it is useful: Adds safer day-to-day file operations for listing, reading, writing, and searching text files.
- popularity: 195 downloads on ClawHub during review
- verification: ClawHub detail page and bundled files align on workspace-scoped file operations.
- note: Benign on ClawHub, but the documented sandbox path is environment-specific.

Validation follow-up example:

- If you want, I can trial-install `workspace-files`, run one realistic task, and report whether its real behavior matches the listing and whether it is worth keeping.

## Existing high-signal examples

Use [references/current-seeds.md](./references/current-seeds.md) as a starting point for likely-useful skills. Treat it as a seed list only and re-check current popularity before recommending.

## Rules

- keep the shortlist opinionated
- prefer current popularity over memory
- prefer ClawHub metrics over guesswork
- verify each candidate before showing it to the user
- use GitHub to verify, not to inflate
- offer trial validation after recommending
- call out suspicious or stale skills explicitly
- avoid recommending more than one near-duplicate unless the user asks for options
- keep each field short enough to scan in one line when possible
- prefer block-style results over dense paragraph summaries
