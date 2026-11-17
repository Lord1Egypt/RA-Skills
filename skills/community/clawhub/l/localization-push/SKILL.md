---
name: localization-push
description: Localizes the user's own App Store / Google Play listing into new languages through their connected App Store Connect or Play Console account - picks target locales from markets with demand, researches the keywords people actually search in each country with AppGoat, writes a localized name, subtitle, keyword field and promotional text (Play title, short and full description) within the store limits, and pushes each locale as a dry run with a before/after diff the user approves. Use when the user says "localize my app listing", "translate my App Store page", "add German / Japanese metadata", "which languages should my app support", "push keywords for other countries" or "localization push".
argument-hint: "<app> [locales]"
license: MIT
---

# Localization push

Turns one good listing into many: for each target locale it researches local search demand,
writes metadata that targets the terms people search for there (not a word-for-word translation),
and writes it to App Store Connect or Play Console after the user has seen the diff. Every write is
a `propose_action` dry run first (free), applied only on approval.

## When to use

- The user owns the app and connected App Store Connect and/or Play Console in AppGoat
  (https://dash.appgoat.ai/connections).
- Not for rewriting the base-language listing (use `aso-keywords-metadata-rewrite` first, then this).

## Inputs

- `app` (required): a linked app (App Store id or Play package; a store URL or name works for the
  research tools, then match it to the linked app).
- `locales` (optional): comma list such as `de-DE,fr-FR,ja,es-MX`. Default: suggest 3–5 from step 2
  and ask the user to confirm.

Ask the user for the base locale (default `en-US`), the brand name that stays untranslated, terms
that must not change (product names), and whether a native speaker will review the copy.

Limits per run: at most **5 locales**.

## Steps

Costs in AppGoat credits. Without the MCP, use the REST equivalents in [reference/api.md](reference/api.md).

1. `list_connections` {} - **0**. Find the `asc` or `play_console` connection with the app linked
   (`status: active`; `mode: read_only` can only dry-run). None: send the user to
   https://dash.appgoat.ai/connections and stop.
2. Pick locales (when not given): `get_app` {app, include: ["markets"]} - **1**: the countries
   where the app is available with ratings per market, and the languages it already supports.
   Suggest locales where the app has ratings but no localization, or large markets in its
   category (de-DE, fr-FR, ja, ko, es-MX, pt-BR, it, zh-Hans). Optionally check demand with
   `keyword_research` {terms: 2–3 translated core terms, store, country} - **1 per term** per
   candidate country: popularity ≥ 20 for the core term means real search demand.
3. Base listing: `read_connection` {id, what: "listing", app, locale: <base>} - **1**. Note the
   fields, their lengths, `editable`, the version and its state.
4. Per target locale:
   - `read_connection` {id, what: "listing", app, locale} - **1**. Shows what exists already
     (an empty listing will be created by the push) and what is editable now.
   - Translate 3–5 seed terms for the app's core job (meaning, not words) and research them:
     `keyword_research` {terms: seeds, store, country: <the locale's main storefront>, include: ["related"]} - **5 per seed**.
   - `keyword_research` {terms: ≤ 25 candidates, store, country, app} - **1 per term**: popularity,
     difficulty and the app's current rank there. Re-call `pending` terms after a minute.
   - Write the localized fields with the decision rules (no calls).
5. Propose per locale, with `playbook: "localization-push"` - **0**:
   - App Store: `propose_action` {type: "listing.update", connection, params: {app, locale, fields:
     {name, subtitle, promotional_text, description?}}} and `propose_action` {type: "keywords.set",
     connection, params: {app, locale, keywords: "a,b,c", mode: "replace"}}.
   - Play: `propose_action` {type: "listing.update", connection, params: {app, locale, fields:
     {title, short_description, full_description}}}.
   The dry run checks the limits and editability: a `BLOCKS` check means fix it (shorten) or, for
   "cannot be edited right now", see the ASC note below.
6. Show the user, per locale, the diff table and the target keywords (see Output format) and ask
   which locales to push. Offer to have a native speaker check the copy first.
7. `apply_action` {id} per approved action - **1 per applied action**. `pending_approval` → give
   the user the `approve_url`; "needs approval by a person" → hand over the link, don't retry;
   "account changed" → show the new diff and ask before `force: true`. `reject_action` the declined ones - **0**.
8. Report what was pushed and what the user still has to do in the console (submit the version).

Budget: **~35–60 credits per locale** (research dominates) + 1 per applied action.

**App Store Connect:** name, subtitle, description, keywords and what's new can only change on a
version in *Prepare for Submission*; promotional text can change on the live version. If the
listing says these fields are not editable, either push only `promotional_text` now or ask the user
to create the next version in App Store Connect, then run step 5 again. The localized metadata
goes live with that version after App Review. Play changes publish after Google's review (hours).

## Decision rules

- **Localize, don't translate.** Pick the terms locals search for (highest popularity × fit from
  step 4), then write natural copy around them. A literal translation with no search demand loses.
- **Apple limits:** name ≤ 30 characters, subtitle ≤ 30, keyword field ≤ **100 bytes** (comma
  separated, no spaces after commas; CJK and Cyrillic characters take 2–3 bytes each, so count
  bytes, not characters), promotional text ≤ 170, description ≤ 4000.
- **Play limits:** title ≤ 30, short description ≤ 80, full description ≤ 4000; Play indexes the
  description, so use each top term 2–4 times in natural sentences.
- **Keyword field:** no words already in the localized name or subtitle (Apple combines them), no
  plurals of present words, no competitor brands, no "app"/"free", singular forms, local spelling.
  Some storefronts also index a second locale (e.g. US: en-US + es-MX; Apple's list): do not repeat
  terms across those pairs.
- **Brand** stays as is (Latin script unless the user has a local brand name); put the top
  local term next to it in the name.
- **Claims:** keep the base listing's facts only; no "#1", "best" or features the app lacks in
  that locale (e.g. unsupported languages in-app).
- **Skip a locale** when no core term has popularity ≥ 10 there: report "low search demand" instead
  of pushing.
- **Never** overwrite an existing localized listing that ranks (the app ranks top 10 for a term
  with popularity ≥ 30 in that country) without showing the user what would be lost.

## Output format

```markdown
# Localization push: <app> (<store>) - <locales>

## de-DE (Germany) · version 2.5 (PREPARE_FOR_SUBMISSION)
| Field | Now | Proposed | Length |
|---|---|---|---|
| Name | (none) | Streaks: Gewohnheiten Tracker | 29/30 |
| Subtitle | (none) | Routinen, Ziele & Tagebuch | 26/30 |
| Keywords | (none) | gewohnheit,routine,ziel,… | 98/100 bytes |
| Promotional text | (none) | … | 142/170 |

Target terms: gewohnheiten tracker (pop 41, diff 55), routine (pop 38, …), …
Guardrail: passed 0.93 · actions act_…, act_…

## ja (Japan) - skipped: core terms below popularity 10.

Reply "push all", "push de-DE only", or edit a field.
```

Run report: pushed locales, pending approvals (links), what to do in the console next
("submit version 2.5 for review"). Credits used: <sum>.

## Automate it

Localization is a one-off push per release, not a schedule. Re-run it when a new version is in
Prepare for Submission so the localized keyword fields follow the base listing.

GitHub Action (`.github/workflows/appgoat-localization.yml`, run by hand; secrets `ANTHROPIC_API_KEY`, `APPGOAT_API_KEY`).
It submits the localized listing for approval in the AppGoat dashboard; nothing is written until
a person approves it at https://dash.appgoat.ai/approvals.

```yaml
name: AppGoat localization push
on:
  workflow_dispatch:
    inputs:
      locales:
        description: Comma list of locales, e.g. de-DE,fr-FR
        required: true
permissions:
  contents: read
jobs:
  localize:
    runs-on: ubuntu-latest
    steps:
      - name: Install AppGoat playbooks and MCP config
        env:
          APPGOAT_API_KEY: ${{ secrets.APPGOAT_API_KEY }}
        run: |
          git clone --depth 1 https://github.com/appgoat/skills /tmp/appgoat-skills
          mkdir -p .claude/skills
          cp -r /tmp/appgoat-skills/skills/* .claude/skills/
          # Hosted AppGoat MCP server; the key goes into a file, not the command line.
          jq -n --arg key "$APPGOAT_API_KEY" \
            '{mcpServers: {appgoat: {type: "http", url: "https://api.appgoat.ai/mcp", headers: {"x-api-key": $key}}}}' \
            > "$RUNNER_TEMP/appgoat-mcp.json"
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Use the localization-push skill for app <app id> with locales ${{ inputs.locales }} and base locale en-US.
            This is an unattended run: instead of asking in step 6, call apply_action once for every action without
            a blocking check (this submits it for approval in the dashboard). Never call apply_action with force.
            Print the per-locale tables as the job summary.
          claude_args: |
            --mcp-config ${{ runner.temp }}/appgoat-mcp.json
            --allowedTools mcp__appgoat__list_connections,mcp__appgoat__read_connection,mcp__appgoat__get_app,mcp__appgoat__keyword_research,mcp__appgoat__get_job,mcp__appgoat__propose_action,mcp__appgoat__apply_action,mcp__appgoat__reject_action,mcp__appgoat__get_action
```

Claude Code routine (one-off reminder after you create a version):

```text
/schedule once tomorrow 09:00 - Run the localization-push playbook for <app id> into de-DE, fr-FR and es-MX, submit the actions for approval and send me the per-locale tables.
```
