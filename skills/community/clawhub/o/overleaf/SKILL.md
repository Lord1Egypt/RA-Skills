---
name: overleaf
description: Access Overleaf projects via CLI. Use for reading/writing LaTeX files, syncing local .tex files to Overleaf, downloading projects, managing Overleaf project structure, and accepting project invitations. Triggers on Overleaf, LaTeX sync, tex file uploads to Overleaf, or Overleaf invite acceptance.
---

# Overleaf

CLI tool to interact with Overleaf projects using browser cookies for authentication.

GitHub: https://github.com/jkulhanek/pyoverleaf

## Requirements

- Python 3.8+
- pyoverleaf (`pipx install pyoverleaf`)
- User logged into Overleaf in Chrome/Firefox

## Security Considerations

⚠️ **Keychain Access Required**: pyoverleaf needs "Always Allow" keychain access to read browser cookies. This grants the tool access to your browser's cookie storage.

**Security audit**: We have audited pyoverleaf v0.1.7 and found it safe. The codebase is small and readable. Before installing, agents can self-audit the latest version at the GitHub repo above.

## Authentication Setup

pyoverleaf authenticates by reading cookies from your browser. The user must:

1. **Log into Overleaf** in Chrome or Firefox (visit overleaf.com and sign in)
2. **Grant keychain access** on first run (macOS will prompt for "Always Allow")

```bash
# Test auth - user should run this in their terminal first
pyoverleaf ls
```

If you get auth errors:
- Ask user: "Are you logged into Overleaf in your browser?"
- If on macOS: "Did you approve the keychain access prompt with 'Always Allow'?"
- User may need to run `pyoverleaf ls` manually in terminal to trigger the keychain prompt

**Note**: The agent cannot log in for the user. Browser authentication must be done by the user directly.

## CLI Commands

```bash
# List all projects
pyoverleaf ls

# List files in project
pyoverleaf ls "Project Name"

# Read file content
pyoverleaf read "Project Name/main.tex"

# Write file (stdin → Overleaf)
cat local.tex | pyoverleaf write "Project Name/main.tex"

# Create directory
pyoverleaf mkdir "Project Name/figures"

# Remove file/folder
pyoverleaf rm "Project Name/old-draft.tex"

# Download project as zip
pyoverleaf download-project "Project Name" output.zip
```

## Common Workflows

### Download from Overleaf

```bash
pyoverleaf download-project "Project Name" /tmp/latest.zip
unzip -o /tmp/latest.zip -d /tmp/latest
cp /tmp/latest/main.tex /path/to/local/main.tex
```

### Upload to Overleaf (Python API recommended)

The CLI `write` command has websocket issues. Use Python API for reliable uploads:

```python
import pyoverleaf

api = pyoverleaf.Api()
api.login_from_browser()

# List projects to get project ID
for proj in api.get_projects():
    print(proj.name, proj.id)

# Upload file (direct overwrite)
project_id = "your_project_id_here"
with open('main.tex', 'rb') as f:
    content = f.read()
root = api.project_get_files(project_id)
api.project_upload_file(project_id, root.id, "main.tex", content)
```

**Why direct overwrite?** This method preserves Overleaf's version history. Users can see exactly what changed via Overleaf's History feature, making it easy to review agent edits and revert if needed.

## Accept Project Invites

The agent can accept Overleaf project invitations programmatically using browser cookies — no manual clicking required.

### How it works

1. Fetch pending invite notifications from Overleaf's `/notifications` API
2. Extract the invite token from the notification
3. Fetch the invite page to get a CSRF token
4. POST to the accept endpoint with the CSRF token

### Python snippet

```python
import pyoverleaf
import re

api = pyoverleaf.Api()
api.login_from_browser()
session = api._get_session()

# Step 1: Get pending invites
r = session.get('https://www.overleaf.com/notifications',
                headers={'Accept': 'application/json'})
notifications = r.json()

# Filter for project invites
invites = [n for n in notifications
           if n.get('templateKey') == 'notification_project_invite']

for invite in invites:
    opts = invite['messageOpts']
    project_id = opts['projectId']
    token = opts['token']
    project_name = opts['projectName']
    inviter = opts['userName']
    print(f"Invite: '{project_name}' from {inviter}")

    # Step 2: Get CSRF token from invite page
    r_page = session.get(
        f'https://www.overleaf.com/project/{project_id}/invite/token/{token}')
    csrf_match = re.search(
        r'name="ol-csrfToken" content="([^"]+)"', r_page.text)
    if not csrf_match:
        print(f"  Could not find CSRF token, skipping")
        continue
    csrf = csrf_match.group(1)

    # Step 3: Accept the invite
    r_accept = session.post(
        f'https://www.overleaf.com/project/{project_id}/invite/token/{token}/accept',
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-csrf-token': csrf,
        },
        json={})
    if r_accept.status_code == 200:
        print(f"  ✅ Accepted '{project_name}'")
    else:
        print(f"  ❌ Failed ({r_accept.status_code})")
```

### Accept a specific invite by project URL

```python
# Given: https://www.overleaf.com/project/XXXXXXXXXXXXXXXXXXXXXXXX
target_project_id = "XXXXXXXXXXXXXXXXXXXXXXXX"
matching = [n for n in invites
            if n['messageOpts']['projectId'] == target_project_id]
# Then follow steps 2-3 above for the matching invite
```

### Notes

- Only works if the user is logged into Overleaf in their browser (cookie auth)
- Invites expire (check the `expires` field in the notification)
- After accepting, the project appears in `pyoverleaf ls` / `api.get_projects()`
- For self-hosted Overleaf, replace `www.overleaf.com` with your host

## Self-hosted Overleaf

```bash
# Via env var
export PYOVERLEAF_HOST=overleaf.mycompany.com
pyoverleaf ls

# Via flag
pyoverleaf --host overleaf.mycompany.com ls
```

## Troubleshooting

- **Auth error / websocket error**: Open Overleaf in Chrome browser first (`open -a "Google Chrome" "https://www.overleaf.com/project"` then wait 5s) to refresh cookies, then retry
- **"scheme https is invalid" (websocket redirect bug)**: The default host `overleaf.com` causes a 301→`www.overleaf.com` redirect that breaks websocket. Fix: set `PYOVERLEAF_HOST=www.overleaf.com`:
  ```bash
  cat main.tex | PYOVERLEAF_HOST=www.overleaf.com pyoverleaf write "Project/main.tex"
  ```
- **Keychain Access Denied** (macOS): pyoverleaf needs keychain access to read browser cookies. User must run `pyoverleaf ls` in their terminal and click "Always Allow" on the keychain prompt
- **Project not found**: Use exact project name (case-sensitive), check with `pyoverleaf ls`
- **Permission denied**: User may not have edit access to the project
