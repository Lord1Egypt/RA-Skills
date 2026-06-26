---
name: linkedin
description: Post updates to LinkedIn, track analytics, and optimize content.
---

# LinkedIn Skill

Post updates, track performance, and optimize your content for maximum reach.

## Setup & Authentication

1.  **Create an App**: Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps), create an app, and add the "Sign In with LinkedIn" and "Share on LinkedIn" products.
2.  **Generate Token**: Use the included helper script to generate an OAuth 2.0 Access Token.
    ```bash
    # Set your credentials
    export LINKEDIN_CLIENT_ID="your_client_id"
    export LINKEDIN_CLIENT_SECRET="your_client_secret"
    export LINKEDIN_REDIRECT_URI="http://localhost:8000/callback"

    # Run the auth helper
    uv run /opt/homebrew/lib/node_modules/openclaw/skills/linkedin/scripts/linkedin_auth.py
    ```
3.  **Save Token**: Save the generated token as `LINKEDIN_ACCESS_TOKEN` in your environment.

## Usage

### 1. Optimize & Feedback Loop (New!)
Analyze your draft against top-performing posts before you publish. Requires `GEMINI_API_KEY`.
```bash
uv run /opt/homebrew/lib/node_modules/openclaw/skills/linkedin/scripts/linkedin_feedback.py "Your draft text here..."
```

### 2. Posting
**Preview (Default):**
```bash
uv run /opt/homebrew/lib/node_modules/openclaw/skills/linkedin/scripts/linkedin.py "Your post text"
```

**Publish:**
```bash
uv run /opt/homebrew/lib/node_modules/openclaw/skills/linkedin/scripts/linkedin.py "Your post text" --confirm
```

### 3. Analytics
**View Stats:**
Reads from `linkedin_history.jsonl` and fetches current stats (Requires `r_member_social`).
```bash
uv run /opt/homebrew/lib/node_modules/openclaw/skills/linkedin/scripts/linkedin_analytics.py
```

## Configuration
- `LINKEDIN_ACCESS_TOKEN`: Valid OAuth 2.0 Access Token.
- `GEMINI_API_KEY`: Required for the Feedback Loop/Optimizer.
