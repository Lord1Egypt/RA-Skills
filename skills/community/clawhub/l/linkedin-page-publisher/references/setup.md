# Setup guide

Read this if the user is setting up LinkedIn publishing for the first time, or if they're seeing errors that look like "unauthorized," "permission denied," or "Community Management API access not granted." Most first-run pain comes from one of the steps below being skipped.

## 1. Create a LinkedIn Developer app

1. Go to https://www.linkedin.com/developers/apps
2. Click **Create app**.
3. Fill in:
   - **App name** — anything descriptive.
   - **LinkedIn Page** — the Company Page you want to post to. This is the critical step; the app must be associated with the target page, and the user creating the app must be an admin of that page.
   - **App logo** — required; LinkedIn rejects apps without one.
4. Accept the legal agreement and create the app.

## 2. Request Community Management API access

The `w_organization_social` scope (needed to create posts on a Company Page) lives inside the **Community Management API** product. It is not available in the free tier.

1. In the app dashboard, go to the **Products** tab.
2. Request **Community Management API**.
3. LinkedIn will ask for:
   - A description of what you're building.
   - Screenshots or a demo video.
   - A privacy policy URL.
   - Sometimes a call with a LinkedIn rep.
4. Approval typically takes a few days to a couple of weeks. Plan accordingly. During review, the app can still authenticate but `POST /rest/posts` will 403.

If you just want to test without approval, you can use `w_member_social` to post to a personal profile instead. But this skill is scoped to Company Pages, so that path needs changes to both `client.py` (use `urn:li:person:...`) and the CLI (accept a person URN instead of an org ID).

## 3. Configure Auth settings

In the app's **Auth** tab:

1. Add `http://localhost:8765/callback` to **Authorized redirect URLs for your app**. This matches the redirect URI in `scripts/get_token.py`.
2. Note the **Client ID** and **Client Secret** — you'll need them in a moment.
3. Under **OAuth 2.0 scopes**, verify that `w_organization_social` (and ideally `r_organization_social` for read access) appear. If they don't, the Community Management API request hasn't gone through yet.

## 4. Find the Company Page's numeric ID

The URN format used by the API is `urn:li:organization:<id>`, where `<id>` is the numeric ID — not the vanity slug.

1. Go to the Company Page's admin view: `https://www.linkedin.com/company/<slug>/admin/`.
2. Once you're in the admin view, the URL changes to include the numeric ID, e.g. `https://www.linkedin.com/company/5515715/admin/`.
3. That `5515715` is what you export as `LINKEDIN_ORG_ID`.

If you don't see an admin view link on the Company Page, the authenticated user is not an admin and the posts will 403 no matter what scope the token has.

## 5. Run the OAuth helper

```bash
export LINKEDIN_CLIENT_ID=<client id from step 3>
export LINKEDIN_CLIENT_SECRET=<client secret from step 3>
python scripts/get_token.py
```

The helper opens a browser, you sign in as the Company Page admin, approve the scopes, and the script prints the access token and refresh token to stdout. Copy them into your shell profile or `.env`:

```bash
export LINKEDIN_ACCESS_TOKEN=AQV...
export LINKEDIN_REFRESH_TOKEN=AQW...
export LINKEDIN_ORG_ID=5515715
```

## 6. Verify with a dry run

```bash
python scripts/publish.py text --text "Test" --dry-run
```

This prints the post body that would be sent. If it renders correctly and the org URN looks right, you're set. Then try a real text post to confirm end-to-end.

## Refreshing the access token later

Access tokens last 60 days. Refresh tokens last 365. To mint a new access token without prompting the user again:

```python
import requests
resp = requests.post(
    "https://www.linkedin.com/oauth/v2/accessToken",
    data={
        "grant_type": "refresh_token",
        "refresh_token": os.environ["LINKEDIN_REFRESH_TOKEN"],
        "client_id": os.environ["LINKEDIN_CLIENT_ID"],
        "client_secret": os.environ["LINKEDIN_CLIENT_SECRET"],
    },
)
new_access_token = resp.json()["access_token"]
```

For a long-running deployment, wire this into a cron or a startup hook that refreshes if the current token is within, say, 5 days of expiry.
