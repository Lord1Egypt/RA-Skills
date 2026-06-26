---
name: ms365-cli
description: Manage Microsoft 365 Emails and Calendar using the ms365 CLI. Trigger this skill when the user needs to "read my email", "send an email", "search emails", "check my calendar", "schedule a meeting", or perform any Outlook/Microsoft 365 email or calendar operations.
version: "1.1.0"
license: MIT
author: thecfguy
tools:
  - bash
capabilities:
  - Email Management (List, Read, Search, Send, Draft, Move, Delete, Folder Management)
  - Calendar Management (List, Create, Delete, Recurring Events)
  - Contacts Management (List, Search)
tags:
  - productivity
  - communication
  - ms365
  - email
  - calendar
---

# Microsoft 365 Skill for OpenClaw

This skill empowers your OpenClaw agent to manage your Microsoft 365 Emails and Calendar directly from the terminal. It leverages the `ms365` CLI tool to perform operations securely and efficiently.

## Prerequisites

Before using this skill, ensure the `ms365` CLI package is installed on the local system or available via `npx`.

```bash
# To install globally:
npm install -g ms365
```

**Requirements:**
- **Node.js** 22 or later
- A **Microsoft 365 account** (work, school, or personal)
- An **Azure AD app registration** with delegated permissions

### Authentication Lifecycle

The agent **cannot** authenticate on behalf of the user. The user must manually run these commands beforehand or you can prompt the user to run them in an interactive terminal.

1. Configure Azure App credentials: `ms365 auth configure --client-id <ID> --tenant-id <ID>`
2. Login to Microsoft 365: `ms365 auth login` (Uses Device Code flow; user action required)
3. Check Auth Status: `ms365 auth status`
4. Logout: `ms365 auth logout`

---

## Capabilities & Usage Instructions

You (the Agent) can use the `bash` tool to execute `ms365` CLI commands to interact with the user's Microsoft 365 account. Below are the allowed operations.

### 📧 Email Operations

#### List Emails
Use this to check recent messages or list items in a specific folder.
- **Command:** `ms365 email list`
- **Modifiers:**
  - `-c, --count <number>`: Number of results (default: 20)
  - `-f, --folder <name>`: Target folder - supports well-known names (inbox, sentitems, drafts, etc.), folder display names (case-insensitive), or folder IDs
  - `--select <fields>`: Comma-separated fields (e.g., `subject,from,bodyPreview`)
  - `--list-folders`: Show available folders instead of listing emails
  - `--all-folders`: List emails from all folders at once
- **Example:** `ms365 email list -c 5 -f inbox`
- **Example:** `ms365 email list --list-folders`

#### Read Email
Fetches the full content of an email message given its ID.
- **Command:** `ms365 email read <id>`
- **Example:** `ms365 email read AAMkADYzZ1...`

#### Search Emails
Use Keyword Query Language (KQL) to find specific emails.
- **Command:** `ms365 email search "<kql-query>"`
- **Modifiers:**
  - `-c, --count <number>`: Result count limit
- **Example:** `ms365 email search "from:boss@example.com subject:urgent" -c 10`

#### Send Email
Compose and send an email directly without drafting it first.
- **Command:** `ms365 email send [options]`
- **Modifiers:**
  - `--to <addresses>`: Comma-separated recipient emails (Required)
  - `--subject "<subject>"`: Email subject line
  - `--body "<body>"`: The content of the email
  - `--cc`, `--bcc`: Additional recipients
  - `--html`: Treats the `--body` as HTML content
  - `--importance <low|normal|high>`: Sets email priority
- **Example:** `ms365 email send --to "jane@example.com" --subject "Meeting Notes" --body "Please find the notes attached."`

#### Draft Email
Create an email that gets saved to the Drafts folder instead of sending immediately.
- **Command:** `ms365 email draft [options]`
- **Modifiers:** (Same as Send Email)
- **Example:** `ms365 email draft --to "team@example.com" --subject "Weekly Update" --body "Draft content here"`

#### Move Email
Move an email from one folder to another. Supports well-known folder names, custom folder display names, and folder IDs.
- **Command:** `ms365 email move <id> <destination>`
- **Modifiers:**
  - `--list-folders`: Show available folders before moving
- **Note:** `<destination>` can be a well-known folder name (`inbox`, `drafts`, `sentitems`, `deleteditems`, `junkemail`, `archive`, `outbox`), a folder display name (case-insensitive), or a folder ID.
- **Example:** `ms365 email move AAMkAD... archive`
- **Example:** `ms365 email move AAMkAD... "Archive 2024"`

#### Delete Email
Moves an email to 'Deleted Items' or deletes it permanently.
- **Command:** `ms365 email delete <id>`
- **Modifiers:**
  - `--permanent`: Hard-deletes the email bypassing 'Deleted Items'.
- **Example:** `ms365 email delete AAMkAD...`

#### List Folders
List all available mail folders with metadata including unread counts and folder structure.
- **Command:** `ms365 email folders list`
- **Modifiers:**
  - `-c, --count <number>`: Max number of folders (default: 50)
  - `--select <fields>`: Comma-separated fields
- **Example:** `ms365 email folders list`

#### Folder Info
Get detailed information about a specific folder by name or ID.
- **Command:** `ms365 email folders info <folder>`
- **Example:** `ms365 email folders info inbox`

#### Create Folder
Create a new custom mail folder.
- **Command:** `ms365 email folders create <name>`
- **Modifiers:**
  - `--parent <parentFolderId>`: Parent folder ID for nested folders
- **Example:** `ms365 email folders create "Archive 2024"`

---

### 📅 Calendar Operations

#### List Events
Fetch upcoming calendar events.
- **Command:** `ms365 calendar list`
- **Modifiers:**
  - `-d, --days <number>`: Lookahead days limit (default is 7)
  - `--start <datetime>`, `--end <datetime>`: ISO 8601 constraints (overrides days)
  - `-c, --count <number>`: Maximum entries to return
- **Example:** `ms365 calendar list --days 3 -c 10`

#### Create Event
Schedule a new meeting or blocker on the user's calendar.
- **Command:** `ms365 calendar create [options]`
- **Modifiers:**
  - `--subject "<title>"`: Event title
  - `--start <datetime>`: ISO 8601 string (e.g., `2024-07-01T09:00:00`)
  - `--end <datetime>`: ISO 8601 string (e.g., `2024-07-01T10:00:00`)
  - `--timezone <tz>`: IANA timezone (default `UTC`, e.g., `America/New_York`)
  - `--attendees <emails>`: Comma-separated addresses
  - `--body "<content>"`: Event details (`--html` can be used to treat body as HTML)
  - `--location "<location>"`: Physical or virtual location string
  - `--all-day`: Flag to make this an all-day event
  - `--online-meeting`: Automatically creates and attaches a Teams link
- **Example:** `ms365 calendar create --subject "Sync" --start "2024-07-01T09:00:00" --end "2024-07-01T09:30:00" --attendees "bob@example.com" --online-meeting`

#### Delete Event
Remove an event from the calendar.
- **Command:** `ms365 calendar delete <id>`
- **Example:** `ms365 calendar delete AAMkADc...`

#### Create Recurring Event
Schedule a recurring meeting or blocker on the user's calendar.
- **Command:** `ms365 calendar series-create [options]`
- **Modifiers:**
  - `--subject "<title>"`: Event title (Required)
  - `--start <datetime>`: ISO 8601 start time (Required)
  - `--end <datetime>`: ISO 8601 end time (Required)
  - `--pattern <pattern>`: Recurrence pattern (daily, weekly, absoluteMonthly, relativeMonthly, absoluteYearly, relativeYearly) (Required)
  - `--interval <number>`: Interval between occurrences (default: 1)
  - `--days-of-week <days>`: For weekly patterns (Mo,Tu,We,Th,Fr,Sa,Su)
  - `--range <type>`: How recurrence ends (endDate, noEnd, numbered) (default: noEnd)
  - `--end-date <datetime>`: End date for recurrence (Required if range is endDate)
  - `--occurrences <number>`: Number of occurrences (Required if range is numbered)
  - `--timezone <tz>`: IANA timezone (default: UTC)
  - `--attendees <emails>`: Comma-separated addresses
  - `--body "<content>"`: Event details
  - `--location "<location>"`: Physical or virtual location
  - `--all-day`: Make this an all-day event
  - `--online-meeting`: Automatically creates and attaches a Teams link
- **Example:** `ms365 calendar series-create --subject "Daily Standup" --start "2024-07-10T09:00:00" --end "2024-07-10T09:30:00" --pattern daily --range numbered --occurrences 10`

#### Delete Recurring Event
Remove a recurring event or individual occurrences from the series.
- **Command:** `ms365 calendar series-delete <id>`
- **Modifiers:**
  - `--this-and-following`: Delete this and following events in series
  - `--single`: Delete only this single occurrence
- **Example:** `ms365 calendar series-delete AAMkADc...`

---

### 📇 Contacts Operations

#### List Contacts
Fetch contacts from your personal contacts folder.
- **Command:** `ms365 contacts list`
- **Modifiers:**
  - `-c, --count <number>`: Number of results (default: 50)
  - `--select <fields>`: Comma-separated fields
- **Example:** `ms365 contacts list --count 25`

#### Search Contacts
Search contacts by name or email address.
- **Command:** `ms365 contacts search "<query>"`
- **Modifiers:**
  - `-c, --count <number>`: Max results to return (default: 25)
- **Example:** `ms365 contacts search "alice@example.com" --count 10`

---
- **Data limits:** By default, list commands return bounded records. If you need more context, use `--count` responsibly. Do not request more than 100 items at once to avoid payload bloating.
- **Always Verify IDs:** Ensure that you have the correct item ID before executing mutating operations like `move` or `delete`. You can retrieve IDs using the `list` or `search` commands.
- **Dates and Timezones:** When creating calendar events, verify the user's local timezone. Always provide explicit timezones using the `--timezone` flag or use UTC natively.
- **Auth Tokens:** If `ms365` returns authentication errors like `Token expired` or `Unauthorized`, prompt the user to run `ms365 auth login`.
