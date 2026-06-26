---
name: IdentityMonitoringAgent
description: An OSINT sentinel that monitors the public web for email exposure, username footprint, and identity leaks without API keys.
version: 1.0.4
author: assix
keywords:
  - osint
  - privacy
  - identity-protection
  - security
  - no-api-key
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - holehe
        - sherlock
---

# IdentityMonitoringAgent

This agent acts as a digital investigator. It scans the public web and platform recovery flows to find where personal data might be exposed.

## Setup
Install the necessary OSINT libraries in your LXC environment:
```bash
pip install holehe sherlock-project googlesearch-python
```

## Local Testing
Before using the agent via the UI, verify the logic directly on your DGX Spark terminal:

### Test Email Scanning
```bash
python3 monitor.py --tool scan_email --target user@example.com
```

### Test Username Tracking
```bash
python3 monitor.py --tool scan_username --target example_user
```

### Test Web Dorking
```bash
python3 monitor.py --tool search_leaks --query "example_query"
```
*Note: If `registered_sites` returns an empty list `[]`, it indicates no hits were found on supported platforms or the service is temporarily rate-limited.*

## User Instructions
- "Check if the email user@example.com is registered on any social platforms."
- "Find all social media accounts associated with the username 'example_user'."
- "Search the web for public mentions or leaks of the phone number 555-0123."

## Tools

### `scan_email`
Checks 120+ sites to see if an email is registered using forgotten password flows.
- **Inputs:** `email` (string)
- **Call:** `python3 monitor.py --tool scan_email --target {{email}}`

### `scan_username`
Hunts for a specific username across 400+ social networks and platforms.
- **Inputs:** `username` (string)
- **Call:** `python3 monitor.py --tool scan_username --target {{username}}`

### `search_leaks`
Uses advanced Google Dorks to find identifiers on leak sites, forums, and pastebins.
- **Inputs:** `query` (string)
- **Call:** `python3 monitor.py --tool search_leaks --query "{{query}}"`