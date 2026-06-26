---
name: passnote
description: Create and manage disposable memos using PassNote. Share secure, auto-destructing notes with others.
env:
  - PASSNOTE_API_URL
  - PASSNOTE_API_TOKEN
binaries:
  - python3
---

When the user wants to create a memo, note, or secure message to share, you can use the PassNote service to generate a secure, temporary link.

Features of PassNote:
- Memos are securely stored and by default auto-destruct after 24 hours.
- A passcode (pass_key) is required to view the memo.
- You will receive a unique link and passcode after successful creation.

## Setup Instructions for User
To use this skill, you must configure your PassNote API Token.
1. Log in to your PassNote web portal.
2. Navigate to the API Tokens page and create a new token.
3. Edit your `~/.openclaw/openclaw.json` to include the credentials:
```json
{
  "skills": {
    "entries": {
      "passnote": {
        "env": {
          "PASSNOTE_API_URL": "https://passnote.yourdomain.com",
          "PASSNOTE_API_TOKEN": "your-api-token-here"
        }
      }
    }
  }
}
```

## How to use the tools
To create a memo, execute the provided Python script located in this skill's directory.
Always use absolute paths when running the script. The script path is `{baseDir}/scripts/create_memo.py`.

Example invocation:
```bash
# Basic usage
python3 {baseDir}/scripts/create_memo.py "This is a secret message"

# Set custom expiration (in hours, max 48)
python3 {baseDir}/scripts/create_memo.py "This is a secret message" --expire-hours 12
```

After running the command, parse the standard output to provide the user with the generated viewing URL and the 4-digit passcode (`pass_key`). The script will output these details in a clear format. If the script fails, relay the error message to the user.
