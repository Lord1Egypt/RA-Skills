# ClawHub publishing checklist

This is the compact publish flow for `market-trading-workflow` (published display name: `World Cup Head to Head Fixture Trader`).

## Pre-publish checks
- Skill folder has `SKILL.md`, `clawhub.json`, `DISCLAIMER.md`, and a main script.
- `SKILL.md` frontmatter `name` matches the folder and slug.
- `clawhub.json` declares `SIMMER_API_KEY` and `simmer-sdk`.
- The script compiles / runs in dry-run mode.

## Login flow
If publish reports that you are not logged in:

1. Run the ClawHub login flow.
2. Approve the device login in the browser.
3. Return to the terminal after authorization completes.
4. Retry publish.

## Publish command
From inside the skill folder:

```bash
npx clawhub@latest publish . --slug market-trading-workflow --version 1.0.20
```

## If publish is blocked
- Fix manifest mismatches before retrying.
- Re-check that the skill folder slug and published slug match.
- Keep the skill framed as a remixable template with conservative defaults.
