# Historical Scan Authentication

## Issue
The historical email and calendar scans (`taste.historical.email` and `taste.historical.calendar`) failed due to incorrect OAuth token usage. The script was authenticating as the agent account (`<third-party-or-user-email>`) instead of <operator>'s account (`<user-google-email>`). This caused the scans to miss 10 years of Gmail and calendar history.

## Root Cause
- The script was using the agent's credentials (`<user-google-email>.json`) instead of <operator>'s credentials (`<hermes-home>/<user-google-email>.json`).
- The historical scans were not explicitly configured to use <operator>'s credentials.

## Fix
Always use <operator>'s credentials (`<hermes-home>/<user-google-email>.json`) for historical scans. The credentials file must be loaded and used explicitly:

```python
# Load <operator>'s credentials
with open("<hermes-home>/<user-google-email>.json", "r") as f:
    owner_credentials = json.load(f)

# Parse the expiry string into a datetime object
try:
    expiry_str = owner_credentials['expiry']
    expiry_str_clean = expiry_str.replace(".295559", "").replace("+00:00", "")
    expiry = datetime.strptime(expiry_str_clean, "%Y-%m-%dT%H:%M:%S")
    owner_credentials['expiry'] = expiry
    
    # Build the Calendar service
    service = build('calendar', 'v3', credentials=Credentials(**owner_credentials))
    
    # List <operator>'s calendars
    calendars = service.calendarList().list().execute()
    
    # List <operator>'s Gmail inbox
    gmail_service = build('gmail', 'v1', credentials=Credentials(**owner_credentials))
    owner_email = '<user-google-email>'
    owner_results = gmail_service.users().messages().list(userId=owner_email).execute()
    
except Exception as e:
    print(f"Error parsing expiry or building service: {e}")
```

## Verification
After applying the fix, verify the following:
1. The historical scans (`taste.historical.email` and `taste.historical.calendar`) run successfully.
2. The data is stored in `<hermes-home>/commons/data/ocas-taste/`.
3. The signals and items are enriched and ready for recommendation generation.