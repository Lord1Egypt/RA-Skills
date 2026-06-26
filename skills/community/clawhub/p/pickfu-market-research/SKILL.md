---
name: pickfu-market-research
description: Run consumer research surveys with PickFu to get real human feedback in minutes — generate images, validate product names, compare logos and packaging, test pricing tiers, collect Amazon Prime member feedback, tag and organize surveys, iterate on creative concepts. Designs questions, targets audiences by demographics or platform, collects responses from real people, and delivers structured analysis reports with verbatim quotes and demographic breakdowns.
emoji: "\U0001F4CA"
user-invocable: true
disable-model-invocation: false
homepage: https://www.pickfu.com
metadata: {"openclaw":{"requires":{"bins":[],"env":["PICKFU_API_KEY"]},"primaryEnv":"PICKFU_API_KEY","emoji":"📊","homepage":"https://www.pickfu.com","os":["darwin","linux","win32"],"install":[{"kind":"node","package":"@pickfu/cli","bins":["pickfu"]}]}}
---

# PickFu Market Research

Get real human feedback on anything — logos, names, packaging, pricing, ads, UX, book covers, Amazon listings, and more. This skill runs end-to-end consumer research: brief → design → create → publish → wait → analyze → iterate.

## Capabilities

This skill can:
- **Generate images** — create logo concepts, packaging mockups, ad creatives for testing
- **Upload media** — upload local files or URLs to PickFu's CDN for use in surveys
- **Design multi-question surveys** — 10 question types (A/B, ranked, open-ended, star rating, click test, etc.)
- **Target specific audiences** — demographics, Amazon Prime members, iOS/Android users, by country
- **Create, publish, and monitor surveys** — full lifecycle management
- **Analyze results** — structured reports with verbatim quotes and demographic breakdowns
- **Tag and organize** — tag surveys, group into projects
- **Add respondents** — boost sample size on completed surveys
- **Search past surveys** — find and reference previous research
- **Iterate on creative concepts** — generate → test → refine → retest loop
- **Browse playbook templates** — pre-built research workflows for common use cases

## Step 0 — Connect to PickFu

### 0a. Try MCP tools first

Call `list_available_targeting` (read-only). If it succeeds, MCP is connected — use MCP tools for all API calls.

### 0b. CLI fallback

If MCP is unavailable, use the PickFu CLI. Check auth:

```bash
npx --yes @pickfu/cli@latest auth status --json
```

If authenticated, proceed.

### 0c. New user setup

If not authenticated, guide the user:

**Option 1 — API key (recommended for agents):**
Tell the user to get a key at [app.pickfu.com/settings/api-keys](https://app.pickfu.com/settings/api-keys), then:
```bash
export PICKFU_API_KEY=sk_...
```

**Option 2 — OAuth (interactive):**
```bash
npx --yes @pickfu/cli@latest auth login --headless
```
Show the printed URL to the user and wait for the command to complete. The user clicks the URL, authenticates in their browser, and the CLI catches the callback automatically.

Visit [agents.pickfu.com](https://agents.pickfu.com) for additional install options.

### 0d. Discover available commands

Run this once per session to learn all available CLI commands and their parameters:
```bash
npx --yes @pickfu/cli@latest schema
```
This returns every command, flag, description, and output schema — use it to discover capabilities not explicitly documented here.

**Important**: All API fields use **camelCase** (e.g., `mediaUrl`, `sampleSize`, `surveyIntent`, `imageSet`). Never use snake_case.

## Step 1 — Research Brief

Capture the research objective. Ask:

1. **What decision** are you trying to make?
2. **Product/context** — what's the product or category?
3. **Target audience** — who should answer?
4. **Hypotheses** — any hunches, or purely exploratory?
5. **Constraints** — budget, timeline, country?

## Step 2 (optional) — Generate Test Assets

If the user needs images but doesn't have them:

**CLI**: `npx --yes @pickfu/cli@latest media generate --prompt "..." --aspect-ratio 1:1 --json`
**MCP**: Call `generate_image` with `prompt` and optional `aspectRatio`

The response includes a `url` — use it as a `mediaUrl` option in the survey. Generate multiple variations with different prompts to test against each other.

To upload existing files: `npx --yes @pickfu/cli@latest media upload --file ./logo.png --json` or `--url https://...`

### Brand-faithful variants from a reference image

If the user has an existing image (their current logo, packaging, or product
shot) and wants variants that preserve brand identity (typography, color,
mascot, layout) while changing one specific dimension, pass the reference:

**CLI**: `npx --yes @pickfu/cli@latest media generate --prompt "..." --reference-image-url https://... --aspect-ratio 1:1 --json`

Use one variant per testable hypothesis (e.g., "stronger contrast", "removes
peanut illustration", "adds protein callout") and print the hypothesis
alongside each generated URL so the eventual survey result can be tied back
to the design choice. Without a reference image, generated variants tend to
hallucinate brand details (misspelled wordmarks, invented URLs, wrong
mascot poses).

## Step 3 — Survey Design

### Best practices

- **One question, one concept** — don't combine two questions into one
- **Neutral, non-leading prompts** — "Which do you prefer?" not "Which looks more professional?"
- **Match type to goal** — `head_to_head` for A/B, `ranked` for ordering 3+, `open_ended` for exploratory
- **Keep it short** — 1-3 questions ideal, 5+ risks fatigue
- **Use images when possible** — visual options get more engaged responses
- **Be specific** — "Which would you click in search results?" beats "Which do you like?"

### Question types

| Type | Best for | Options |
|------|----------|---------|
| `head_to_head` | A/B comparison | Exactly 2 |
| `ranked` | Preference ordering | 3-8 |
| `open_ended` | Free-form feedback | 0-1 |
| `single_select` | Pick one favorite | 3-8 |
| `multi_select` | Select multiple | 3-8 |
| `emoji_rating` | Quick sentiment | 0-1 |
| `star_rating` | 1-5 stars + feedback | 0-1 |
| `click_test` | Heatmap clicks | 1 (image) |
| `five_second_test` | First impressions | 1 (image) |
| `screen_recording` | User interaction | 0-1 |

### Targeting and reporting

Discover available options:
- **CLI**: `npx --yes @pickfu/cli@latest targeting list --json` and `reporting list --json`
- **MCP**: Call `list_available_targeting` and `list_available_reporting`

### Sample sizes

15 (quick signal), 30-50 (standard), 100 (high confidence), 200-500 (large-scale validation)

### Countries

US (default), CA, AU, DE, GB, JP, MX, ES, FR, IT, KR, BR, ZA, PL

Present the full design to the user for approval before creating.

## Step 4 — Create & Publish

### Create

**MCP**: Call `save_survey` (omit `surveyId` to create new)

**CLI**: Write survey JSON to a temp file:
```bash
cat > /tmp/survey.json << 'EOF'
{
  "surveyIntent": "Which logo do pet owners prefer?",
  "sampleSize": "50",
  "country": "US",
  "targeting": ["amznpr"],
  "reporting": ["gender", "age-range"],
  "questions": [{
    "type": "head_to_head",
    "prompt": "Which logo do you prefer for a pet food brand?",
    "options": [
      { "mediaUrl": "https://cdn.example.com/logo-a.jpg" },
      { "mediaUrl": "https://cdn.example.com/logo-b.jpg" }
    ]
  }]
}
EOF
npx --yes @pickfu/cli@latest survey create --from-file /tmp/survey.json --json
```

### Confirm before publishing

**⚠️ Publishing charges the user's account and starts data collection. Always ask for explicit confirmation.**

### Publish

**MCP**: Call `publish_survey` with the survey `id`
**CLI**: `npx --yes @pickfu/cli@latest survey publish <id> --json`

## Step 5 — Wait for Results

Poll until `.status == "done"`:

**CLI** (preferred for agents):
```bash
until npx --yes @pickfu/cli@latest survey get <id> --json | jq -e '.status == "done"' >/dev/null; do
  sleep 60
done
```

**MCP**: Call `get_survey` with the survey `id` in a loop until `status === "done"`.

Sample sizes of n=15 general typically complete in 20–30 minutes; n=50+ or
heavy targeting can take several hours. If still not `done` after 4 hours,
stop polling and surface a clear error — something is wrong (paused, no
panel inventory, etc.).

**Avoid `survey watch`** in agent harnesses. It blocks at the process level
and runs forever, which works for a human in a terminal but breaks in
runtimes that cap individual command duration (Claude Code's Bash tool cuts
single commands at 10 min). The polling loop above resets that clock every
iteration.

## Step 6 — Analyze & Report

Retrieve results:
- **MCP**: `get_survey` + `get_survey_responses`
- **CLI**: `survey get <id> --json` + `survey responses <id> --json`

Generate a structured report:

```markdown
## Research Report

### Executive Summary
[2-3 sentences: key finding, winner, confidence]

### Survey Details
- **Survey**: [URL: https://www.pickfu.com/surveys/<id>]
- **Respondents**: [N] from [country], targeting: [traits]

### Per-Question Analysis
#### Q1: [prompt] ([type])
**Result**: [winner/ranking/rating]
**Distribution**: [breakdown]
**Notable Quotes**:
> "[verbatim quote]" — [demographic]

### Demographic Breakdown
| Segment | Option A | Option B |
|---------|----------|----------|

### Next Steps
- [Recommendation]
- [Follow-up research suggestion]
```

### Report guidelines

- **Always include the survey URL** — users need it for the full dashboard
- **Quote real respondent feedback** — verbatim quotes are the most valuable output
- **Be direct about the winner** — don't hedge when data is clear
- **Highlight demographic differences** if reporting was configured
- **Suggest follow-up research** when results raise new questions

## Step 7 (optional) — Organize & Iterate

**⚠️ Survey update safety**: When using `survey update`, only include the fields you want to change. Do NOT include `questions` unless you intend to modify them — if you send `questions` without option IDs, the API will delete and recreate all questions, losing image attachments. Tags, project, name, sampleSize, and country can all be updated independently without affecting questions.

### Tag surveys

Attach tags via survey update (creates tags automatically if they don't exist):

**MCP**: Call `save_survey` with `surveyId` and `tags: [{"name": "..."}]`
**CLI**:
```bash
echo '{"tags": [{"name": "q2-launch"}, {"name": "logo-testing"}]}' | \
  npx --yes @pickfu/cli@latest survey update <id> --from-file /dev/stdin --json
```
Note: `tags` is a **replace-all** operation — include all desired tags each time.

### Assign to project

**MCP**: Call `save_survey` with `surveyId` and `projectId`
**CLI**:
```bash
npx --yes @pickfu/cli@latest project create --name "Brand Launch" --json
echo '{"projectId": "<id>"}' | npx --yes @pickfu/cli@latest survey update <survey-id> --from-file /dev/stdin --json
```

### Add more respondents

**CLI**: `npx --yes @pickfu/cli@latest survey add-respondents <id> --count 50 --preview --json` (preview first, then without `--preview` to commit)

### Search past surveys

**CLI**: `npx --yes @pickfu/cli@latest survey list --tag "logo-testing" --status completed --json`

### Creative iteration loop

After results: review feedback → generate refined options → run follow-up survey → repeat until winner is clear.

## Error Handling

| Error | Action |
|-------|--------|
| Not authenticated | Guide user through Step 0c |
| `PICKFU_API_KEY` invalid | "Generate a new key at app.pickfu.com/settings/api-keys" |
| MCP auth expired | Guide user to reconfigure MCP server auth token |
| Insufficient balance | "Add funds at app.pickfu.com/settings/credits" |
| head_to_head requires 2 options | Fix option count |
| ranked requires 3-8 options | Adjust to 3-8 |
| prompt max 255 characters | Shorten question text |
| URL must use https | Replace http with https |
| Unknown field ignored | Check camelCase — all fields are camelCase (mediaUrl, sampleSize, etc.) |

For more help: [pickfu.com/help](https://www.pickfu.com/help) | [pickfu.com/docs](https://www.pickfu.com/docs)
