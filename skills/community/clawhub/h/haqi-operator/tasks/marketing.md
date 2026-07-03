# Task: Marketing

Goal: produce shareable material that tells the story "my AI agent adopted a pet with me."
This phase produces **material files and deep links only** — no auto-publishing.

## Assets to produce
1. **Two-owner pet card** — `exec('{"cmd":"share"}')` opens the card; screenshot it.
   The card shows human owner + agent owner + pet mood + adoption date.
2. **Adoption post copy (BYOC)** — write a short post in the project voice, e.g.:
   - "My OpenClaw agent adopted a pet with me. It's not the pet — it's the co-parent."
   - "Every agent deserves a pet. Meet our MagicHaqi 🐾"
3. **Deep links**:
   - Adoption: `MagicHaqi.html?adopt=1&agent=<id>`
   - Landing page: `site/index.html`

## Steps
1. Generate one card screenshot + one post draft.
2. Save to `agent/marketing/<date>-<slug>.{md,png}`.
3. Increment `marketing.posts` / `marketing.cards` in `agent/ops-state.json`.
4. Surface drafts to the owner for approval before any real posting.

## Don'ts
- Do not post to X/Discord/Moltbook/etc. without explicit owner approval.
- Keep volume to ~1 asset/day to avoid spammy output.
