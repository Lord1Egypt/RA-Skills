# Google Sheet Setup Guide

This guide explains how to set up the Google Sheet for the jobs-hunter-claw skill.

## Create the Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new blank spreadsheet
3. Name it "Job Applications Tracker" (or your preference)
4. Copy the spreadsheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
   ```

## Create Tabs

Create three tabs (sheets) within the spreadsheet:

### Tab 1: Jobs

Main tracker with columns A-P:

| Column | Header | Purpose |
|--------|--------|---------|
| A | Our Job ID | Internal ID (JOB001, JOB002, ...) |
| B | Employer Job ID | Employer's requisition number |
| C | Company | Company name |
| D | Role | Job title |
| E | Location | City, Remote, Hybrid |
| F | Salary Range | Compensation |
| G | Source | How discovered (LinkedIn, Recruiter, etc.) |
| H | URL | Job posting link |
| I | Status | Current status (see valid values) |
| J | Applied Date | Date applied (YYYY-MM-DD) |
| K | Contacts | Google Contacts links to recruiters/contacts |
| L | Next Action | Planned next step |
| M | Next Date | Date for next action |
| N | Resume Used | Which resume version |
| O | Cover Letter | Cover letter used |
| P | Log (Latest 3) | Auto-populated from Activity Log |

**Column P Formula** (shows latest 3 log entries):
```
=IFERROR(TEXTJOIN(CHAR(10),TRUE,QUERY('Activity Log'!A:D,"SELECT A,C,D WHERE B='"&A2&"' ORDER BY A DESC LIMIT 3")),"")
```

### Tab 2: Activity Log

Timestamped event history:

| Column | Header |
|--------|--------|
| A | Timestamp |
| B | Our Job ID |
| C | Event Type |
| D | Details |

### Tab 3: Add or Edit Job (Optional)

Form interface for manual entry. Created automatically by the Apps Script `setupDataValidation()` function, or can be set up manually with:

- Form fields for each job attribute
- Dropdown for Status (data validation)
- Dropdown for Event Type (data validation)
- Reference section showing valid values

## Configure the CLI

Set the `JOB_TRACKER_SPREADSHEET_ID` environment variable:

```bash
export JOB_TRACKER_SPREADSHEET_ID="your-spreadsheet-id-here"
```

For persistent configuration, add to your shell profile (`~/.bashrc`, `~/.zshrc`):

```bash
echo 'export JOB_TRACKER_SPREADSHEET_ID="your-spreadsheet-id"' >> ~/.bashrc
source ~/.bashrc
```

## Valid Status Values

Use these exact values (Title Case):

- Discovered
- Applied
- Screening
- Interview
- Karat Test Scheduled
- Offer
- Rejected
- Withdrawn
- Accepted
- Closed

## Valid Event Types

Use these exact values (lowercase):

- discovered
- applied
- recruiter_contact
- user_reply
- interview_scheduled
- interview_completed
- test_scheduled
- test_completed
- offer_received
- rejection
- follow_up
- status_change
- note

## Install Apps Script (Optional)

For form automation in the Google Sheet:

1. Open your spreadsheet
2. Go to **Extensions → Apps Script**
3. Delete any existing code
4. Paste the contents of `scripts/job-tracker-appscript.js`
5. Click **Save** (💾 icon)
6. Refresh your spreadsheet
7. Click **🎯 Job Tracker → ⚙️ Setup Data Validation**
8. Authorize the script when prompted

## Share Settings

If using with multiple devices or agents:

1. Click **Share** in the top right
2. Add your Google account(s) with Editor access
3. For service account access, share with the service account email

## Backup

Consider enabling version history:

1. Go to **File → Version history → See version history**
2. Name important versions before major changes

The Activity Log tab provides a natural audit trail of all changes.
