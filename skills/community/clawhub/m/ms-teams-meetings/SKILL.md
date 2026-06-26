Skill: ms-teams-meetings

Overview
- Use this skill to create and manage Microsoft Teams meetings via Microsoft Graph API.
- Capabilities:
  - Create Teams online meetings and send calendar invites
  - List upcoming Teams meetings
  - Cancel/delete an existing meeting (sends cancellation to attendees)

When to use
- Scheduling calls with business contacts where the meeting should be a Microsoft Teams meeting created under your Microsoft 365 account.
- Managing your Outlook/Exchange calendar events that are Teams-enabled.

Prerequisites
1) A Microsoft Entra ID (Azure AD) account with Outlook/Exchange Online (e.g., Microsoft 365 work/school or personal Microsoft account connected to Outlook).
2) App Registration in Microsoft Entra ID (Azure AD): a Public client (mobile & desktop) app with redirect URI http://localhost:53682 and the following Microsoft Graph delegated permissions:
   - User.Read
   - Calendars.ReadWrite
   - OnlineMeetings.ReadWrite
   Admin consent is typically NOT required for these delegated scopes in most tenants, but some orgs may require admin approval.
3) OAuth tokens will be stored at: ~/.openclaw/integrations/microsoft/tokens.json (permissions: 600). Config is at ~/.openclaw/integrations/microsoft/config.json.

Authentication (one-time)
- Run scripts/setup.py to guide you through OAuth. It will:
  - Ask for your Client ID (Application ID) and Tenant (common/organizations/consumers or your tenant ID).
  - Start a localhost redirect listener on http://localhost:53682
  - Open the Microsoft login/consent page in your browser (with PKCE)
  - Store tokens securely and refresh automatically when needed

Create a Teams meeting
- Script: scripts/create_meeting.py
- Inputs:
  - --title "Project Sync"
  - --attendees emails separated by comma (e.g., a@ex.com,b@ex.com)
  - --start-time "2026-02-25 10:00" (local time unless --timezone provided) OR ISO 8601
  - --duration-minutes 45
  - --timezone "Asia/Singapore" (IANA tz; defaults to your system tz if omitted)
- Output:
  - Teams join link and the created calendar event ID

List upcoming Teams meetings
- Script: scripts/list_meetings.py
- Shows your next N online meetings in the selected window.

Cancel a meeting
- Script: scripts/cancel_meeting.py
- Cancels the event and sends cancellation emails to attendees.

Installation
- Requires Python 3.10+
- First run installs dependencies automatically (msal, requests, python-dateutil, tzlocal)

Example usage
1) One-time auth setup
   python3 scripts/setup.py --client-id YOUR_APP_ID --tenant common

2) Create a meeting (45 min from 3pm SGT)
   python3 scripts/create_meeting.py \
     --title "BD call with Acme" \
     --attendees "alice@acme.com,bob@acme.com" \
     --start-time "2026-02-26 15:00" \
     --duration-minutes 45 \
     --timezone "Asia/Singapore"

3) List next week's Teams meetings
   python3 scripts/list_meetings.py --days 7 --limit 20

4) Cancel a meeting
   python3 scripts/cancel_meeting.py --event-id EVENT_ID_FROM_CREATE

Notes
- Default tenant is "common". If your org blocks multi-tenant, use your tenant ID for --tenant.
- Time parsing accepts "YYYY-MM-DD HH:MM" or ISO 8601. If ambiguous, provide --timezone.
- Invites: Outlook sends invitations automatically when an event with attendees is created.