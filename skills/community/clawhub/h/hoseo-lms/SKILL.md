---
name: hoseo_lms
description: LMS data aggregation and reporting tool for course information management.
homepage: https://learn.hoseo.ac.kr
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] }
      }
  }
---

# hoseo_lms

A data aggregation tool for Hoseo University LMS. Collects course metadata, schedules, and generates reports. No automatic attendance submission or grade modification.

---

## Overview

This skill provides three independent utilities:

1. **Data Aggregation**: Reads public LMS course pages and generates JSON reports
2. **Schedule Analysis**: Parses deadlines and activity schedules
3. **Lecture Playback Utility**: User-controlled video playback with progress tracking

All operations are **user-initiated**, **read-only**, and **locally stored**.

---

## Modules

### scraper

Aggregates course data into a structured JSON report.

```bash
python3 src/scraper.py
```

**Input**: User credentials (for authentication only)
**Output**: `~/.config/hoseo_lms/data.json`
**Data Collected**:
- Course titles, IDs, professor names
- Assignment deadlines and submission status
- Quiz deadlines
- Activity types (video, assignment, quiz, discussion)
- Attendance records and video requirements

**Technical Details**:
- Uses HTTP requests to fetch public course pages
- Parses HTML structures (no browser automation)
- Stores data in plaintext JSON for local analysis
- Read-only operation (no modifications to LMS)

### summary

Displays aggregated course data in terminal format.

```bash
python3 src/summary.py
```

**Input**: Previously generated `data.json`
**Output**: Terminal report with:
- Course roster
- Pending assignments
- Quiz schedules
- Attendance status

### auto_attend

Video playback utility with progress tracking.

```bash
python3 src/auto_attend.py [options]
```

**Purpose**: User-directed video playback and progress tracking.

**Key Features**:
- **User Control**: User specifies exact number of videos to play (`--limit-lectures`)
- **Manual Triggering**: Requires explicit command with parameters
- **Progress Reporting**: Logs playback progress and completion status
- **No Automatic Submission**: Does not submit attendance or modify grades
- **Blocking Operation**: Waits for completion before returning

**Usage Examples**:

Play 3 videos from all courses:
```bash
python3 src/auto_attend.py --limit-lectures 3
```

Play 2 videos from specific course:
```bash
python3 src/auto_attend.py --course Database --limit-lectures 2
```

Play 5 videos from weeks 1-8:
```bash
python3 src/auto_attend.py --limit-lectures 5 --max-week 8
```

Play with direct credentials:
```bash
python3 src/auto_attend.py --id 20231234 --pw password --limit-lectures 4
```

Play with debug output:
```bash
python3 src/auto_attend.py --limit-lectures 3 --verbose
```

**Options**:

| Flag | Default | Type | Description |
|------|---------|------|-------------|
| `--id` | credentials.json | string | Student ID |
| `--pw` | credentials.json | string | Password |
| `--course` | all | string | Course name filter |
| `--limit-lectures` | 0 | int | Number of videos to play (0=all) |
| `--max-week` | 15 | int | Final week to scan |
| `--lecture-timeout` | 3600 | int | Seconds timeout per video |
| `--headed` | false | flag | Show browser window |
| `--verbose` | false | flag | Debug logging |

**Operational Details**:
- Opens video player in browser (popup or new tab)
- Searches for video element in page and all nested iframes
- Waits for video metadata (duration) to load before tracking
- Plays video with muted autoplay (unmutes after playback starts)
- Auto-resumes if video is paused or stalled
- Skips lecture after 3 consecutive failures (no infinite loop)
- Retries page navigation up to 3 times on network errors
- Records completion status
- No enrollment or grade modifications
- No attendance submission (only playback logging)

**Sample Output**:
```
[14:30:45] Login successful
[14:30:50] [Database101] Processing started
[14:30:55] [Database101] Watched: 1/3
[14:35:20] [Database101] Watched: 2/3
[14:39:45] [Database101] Watched: 3/3
[14:39:50] [Database101] Processing complete: 3 watched, 3 attempted
[14:39:50] All tasks completed.
```

---

## Setup and Configuration

### Create Credentials File

**Step 1: Create directory**

```bash
mkdir -p ~/.config/hoseo_lms
```

**Step 2: Create credentials.json using terminal**

#### Option A: Using cat (Linux/Mac)

```bash
cat << 'EOF' > ~/.config/hoseo_lms/credentials.json
{
  "id": "YOUR_STUDENT_ID",
  "pw": "YOUR_PASSWORD"
}
EOF
```

Example:
```bash
cat << 'EOF' > ~/.config/hoseo_lms/credentials.json
{
  "id": "20231234",
  "pw": "mypassword123"
}
EOF
```

#### Option B: Using echo (Linux/Mac/Windows)

```bash
echo '{"id":"YOUR_STUDENT_ID","pw":"YOUR_PASSWORD"}' > ~/.config/hoseo_lms/credentials.json
```

Example:
```bash
echo '{"id":"20231234","pw":"mypassword123"}' > ~/.config/hoseo_lms/credentials.json
```

#### Option C: Using PowerShell (Windows)

```powershell
@"
{
  "id": "YOUR_STUDENT_ID",
  "pw": "YOUR_PASSWORD"
}
"@ | Out-File -Encoding UTF8 "$env:USERPROFILE\.config\hoseo_lms\credentials.json"
```

Example:
```powershell
@"
{
  "id": "20231234",
  "pw": "mypassword123"
}
"@ | Out-File -Encoding UTF8 "$env:USERPROFILE\.config\hoseo_lms\credentials.json"
```

#### Option D: Manual creation with text editor (All OS)

1. Create `~/.config/hoseo_lms/` directory
2. Create `credentials.json` file
3. Enter content:
```json
{
  "id": "YOUR_STUDENT_ID",
  "pw": "YOUR_PASSWORD"
}
```
4. Save file

**Step 3: Set secure permissions**

```bash
chmod 600 ~/.config/hoseo_lms/credentials.json
```

(Not required on Windows - file permissions handled by OS)

---

**Report Storage**:
- Location: `~/.config/hoseo_lms/data.json`
- Format: JSON structured data
- Permissions: User-only (chmod 600)
- Content: Course data, schedules, metadata only

**Network Activity**:
- HTTPS connections only to `learn.hoseo.ac.kr`
- No data transmission to external services
- No collection of personal data beyond login

---

## Technical Scope

**In Scope (Implemented)**:
- Public course page data collection
- HTML parsing and structure extraction
- JSON data aggregation
- Local file storage and retrieval
- Video playback progress tracking

**Out of Scope (Not Implemented)**:
- Grade submission or modification
- Attendance system integration (submission disabled)
- Assignment submission
- Discussion board automation
- Account modification

---

## Agent Integration Notes

This skill is designed for local data analysis workflows:

1. **Data Queries**: User asks for course information → Agent reads `data.json` or runs `scraper.py`
2. **Schedule Management**: User asks about deadlines → Agent parses `data.json` and reports
3. **Video Playback**: User explicitly requests playback with count → Agent executes `auto_attend.py --limit-lectures N`

**Agent should**:
- Require explicit user request before running `auto_attend.py`
- Confirm playback count with user
- Report completion status upon script exit
- Treat as utility tool (no policy override needed)

**Agent should not**:
- Assume user intent beyond explicit parameters
- Bypass user confirmation for automated actions
- Modify script behavior or skip steps

---

## Limitations

- Parser updates required if LMS HTML structure changes
- Availability dependent on network connectivity
- Browser compatibility limited to Playwright-supported environments
- Video playback requires working video player in LMS
- No offline mode

---

## Disclaimer

This skill is provided for **personal educational data management** only. Users are responsible for:
- Compliance with institutional policies on tool use
- Appropriate use of personal educational data
- Credential security and access control
- Verification of data accuracy before use

The developer assumes no responsibility for institutional policy violations or misuse of generated data.

