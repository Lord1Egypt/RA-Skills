# Review Responder: Setup Guide

## One-Time Setup (Your VPS)

### 1. Install Python Dependencies
```bash
pip install google-auth google-auth-oauthlib requests
```

### 2. Create a Google Cloud Project
1. Go to https://console.cloud.google.com
2. Create a new project (e.g., "Review Responder")
3. Enable the **Google My Business API** (also called Business Profile API)
4. Go to **Credentials** > **Create Credentials** > **OAuth 2.0 Client ID**
5. Application type: **Desktop app**
6. Save the **Client ID** and **Client Secret** -- you'll use these for every client

### 3. Copy Files to OpenClaw Workspace
Copy the `review-responder` folder into your OpenClaw agent workspace:
```bash
cp -r review-responder ~/.openclaw/workspace/review-responder
```

### 4. Register the Skill
Add the skill to your OpenClaw config (openclaw.json):
```json
{
  "skills": {
    "entries": {
      "review-responder": {
        "path": "~/review-responder/SKILL.md"
      }
    }
  }
}
```

### 5. Wire Up the Heartbeat
Append the review check instructions to your HEARTBEAT.md, or if you want a dedicated agent for this, reference `~/review-responder/HEARTBEAT.md` in your heartbeat config.

### 6. Set Heartbeat Interval
In openclaw.json, set the heartbeat to run every 1-2 hours:
```json
{
  "agent": {
    "heartbeat": { "every": "60m" }
  }
}
```

---

## Per-Client Onboarding

### Step 1: Get Their Authorization
You need the client to authorize your app to access their Google Business Profile.

Run this one-time script on your machine to generate a refresh token:
```bash
python3 get_client_token.py
```
This will:
1. Open a browser for the client to log in with their Google account
2. Ask them to authorize access to their Business Profile
3. Print a refresh token you save to their config file

(See `get_client_token.py` for the helper script.)

### Step 2: Find Their Account and Location IDs
After authorization, use the access token to look up their IDs:
```bash
# List accounts
curl -H "Authorization: Bearer ACCESS_TOKEN" \
  "https://mybusinessaccountmanagement.googleapis.com/v1/accounts"

# List locations for an account
curl -H "Authorization: Bearer ACCESS_TOKEN" \
  "https://mybusinessbusinessinformation.googleapis.com/v1/accounts/ACCOUNT_ID/locations"
```

### Step 3: Create Their Config File
Copy the template and fill in the values:
```bash
cp clients/_template.json clients/joes-pizza.json
```

Edit with their specific values:
```json
{
  "business_name": "Joe's Pizza",
  "account_id": "accounts/123456789",
  "location_id": "locations/987654321",
  "oauth_client_id": "YOUR_PROJECT_CLIENT_ID.apps.googleusercontent.com",
  "oauth_client_secret": "YOUR_PROJECT_CLIENT_SECRET",
  "refresh_token": "1//TOKEN_FROM_STEP_1",
  "notes": "Family pizza place, casual and friendly tone"
}
```

### Step 4: Test It
```bash
python3 gbp_reviews.py check --client joes-pizza
```

If it returns reviews (or "No new unanswered reviews"), you're good.

---

## OAuth Token Helper Script

The `get_client_token.py` script handles the one-time OAuth flow. Before running it, update the `CLIENT_ID` and `CLIENT_SECRET` variables at the top of the file with your Google Cloud project credentials.

For remote/web-based onboarding, see `oauth_server.py` instead (requires Flask).

---

## Folder Structure
```
review-responder/
  gbp_reviews.py          # Main script (check + reply)
  get_client_token.py      # One-time OAuth helper
  SKILL.md                 # Agent behavior instructions
  HEARTBEAT.md             # Periodic check instructions
  SETUP.md                 # This file
  review_log.json          # Auto-generated: tracks processed reviews
  clients/
    _template.json         # Config template
    joes-pizza.json        # Example client config
  pending/
    joes-pizza_abc123.json # Auto-generated: reviews awaiting approval
```
