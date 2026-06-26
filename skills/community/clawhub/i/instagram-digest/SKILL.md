---
name: instagram-digest
description: Scrape recent Instagram reels, transcribe audio, summarize with OpenRouter, and save a digest.html file
metadata:
  openclaw:
    requires:
      env:
        - OPENROUTER_API_KEY
      optionalEnv:
        - INSTAGRAM_USERNAME
        - INSTAGRAM_PASSWORD
      anyBins:
        - python3
        - python
    primaryEnv: OPENROUTER_API_KEY
---

# Instagram Digest Skill

Scrapes Instagram reels from a configured list of accounts, transcribes their audio, generates AI summaries, and saves a `digest.html` file for local viewing.

## When to Use

Trigger this skill when the user asks to:
- Run / send the Instagram digest
- Get a summary of recent Instagram reels
- Check what accounts are being tracked
- Add or remove accounts from the digest
- Do a dry run / preview without sending email

## Working Directory

All commands must be run from the skill's own directory:
```
cd /path/to/instagram-digest
```

## Commands

### Run the digest (saves digest.html)
```
python main.py
```

### Run digest for specific accounts only
```
python main.py --accounts username1 username2 username3
```

### List currently configured accounts
```
python main.py --list-accounts
```

## Adding / Removing Accounts Permanently

The default account list lives in `config.py` under `INSTAGRAM_ACCOUNTS`. To permanently add or remove an account, edit that list. Then confirm by running `--list-accounts`.

## Environment Variables

| Variable | Required | Purpose |
|---|---|---|
| `OPENROUTER_API_KEY` | ✅ Required | OpenRouter API key for transcript summarization (uses Nvidia Nemotron via OpenRouter) |
| `INSTAGRAM_USERNAME` | Optional | Instagram login for story access — use a dedicated throwaway account |
| `INSTAGRAM_PASSWORD` | Optional | Instagram password for story access — use a dedicated throwaway account |

## Output

Writes `digest.html` to the skill directory. Open it in a browser to read audio summaries for each reel.

## Error Handling

- If Instagram returns a login wall for an account, that account is skipped and the digest continues with the rest.
- If transcription or analysis fails for a reel, a fallback message is shown for that item — the digest still sends.
- If no new reels or stories are found across all accounts, the email is skipped entirely and a message is printed.