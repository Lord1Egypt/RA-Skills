# API Setup

## Access level

Google Ads API Basic Access is approved, so this skill can support real production reporting and operational workflows.

## Required credentials

- `GOOGLE_ADS_DEVELOPER_TOKEN`
- `GOOGLE_ADS_CLIENT_ID`
- `GOOGLE_ADS_CLIENT_SECRET`
- `GOOGLE_ADS_REFRESH_TOKEN`
- `GOOGLE_ADS_MANAGER_ACCOUNT_ID` optional
- `GOOGLE_ADS_CLIENT_ACCOUNT_ID` optional

## Credential handling

Do not tell users to store credentials in plaintext files.
For this OpenClaw environment, follow the current key protocol used by the workspace owner.
Keep credentials in secure storage and expose them to the runtime through approved environment injection.

## Dependencies

```bash
pip3 install -r requirements.txt
```

## Authentication flow

Run:

```bash
python3 scripts/authenticate.py
```

Use the result to obtain or refresh the Google Ads refresh token.
Do not paste credentials into tracked files.

## Test connection

```bash
python3 scripts/get_account_summary.py --account YOUR-ACCOUNT-ID
```

If this fails:
- verify all required environment variables exist
- verify the developer token is valid
- verify the refresh token is current
- verify the account ID is a 10-digit ID without dashes

## Operational note

Prefer manager-account-driven access when multiple accounts are involved.
Keep client account IDs explicit when running analysis to avoid checking the wrong account.
