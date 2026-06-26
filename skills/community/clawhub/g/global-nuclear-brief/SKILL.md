---
name: nuclear_policy_brief
description: Generate a grounded nuclear energy policy brief from live news using Apify + Contextual.
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      config: ["APIFY_API_TOKEN", "CONTEXTUAL_API_KEY"]
---

# Nuclear Policy Brief

Use this skill when the user wants a concise, grounded brief about nuclear energy policy or regulation.

## What it does
- Pulls recent nuclear policy/regulatory news via Apify.
- Uses Contextual to synthesize a structured brief grounded in the retrieved sources.

## How to run
Use `exec` to run the script. Always pass user-provided values as arguments, never interpolate raw text into the shell.

Command template:
```bash
python3 bin/nuclear_brief.py --query "<search query>" --topic "<topic focus>" --audience "<audience>" --country "<country code>" --timeframe "<timeframe>"
```

Example:
```bash
python3 bin/nuclear_brief.py --query "nuclear energy policy OR nuclear regulation" --topic "Global nuclear energy policy" --audience "policy analysts" --country "US" --timeframe "7d"
```

## Output format
Return the brief exactly as produced by the script. If the script reports missing env vars or no results, ask the user for a different query or timeframe.

## Required config
- `APIFY_API_TOKEN`
- `CONTEXTUAL_API_KEY`

## Notes
- Keep the demo under 3 minutes.
- Highlight the live data pull (Apify) and grounded generation (Contextual).
