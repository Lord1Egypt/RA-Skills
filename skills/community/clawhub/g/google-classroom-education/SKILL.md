---
name: google-classroom-education
description: Manage Google Classroom courses, coursework, students, teachers, submissions, and announcements via the Google Classroom API. Use this skill when users want to list courses and rosters, inspect coursework and submissions, create or update assignments after confirmation, post announcements, or review grades in Google Classroom.
---

# Google Classroom

![Google Classroom](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/google-classroom.svg?v=2)

Access Google Classroom via the Google Classroom API with OAuth authentication. Manage courses, coursework, students, teachers, submissions, and announcements.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-classroom-education) for hosted connection flows and credentials so you do not need to configure Google Classroom API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Google Classroom |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Classroom |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Google Classroom │
│   (User Chat)   │     │   (OAuth)    │     │   API (REST)     │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Google Classroom                   │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │Classroom │
   │  File    │           │ Auth     │           │ Courses  │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Classroom again."

## Quick Start

```bash
# List courses
clawlink_call_tool --tool "google_classroom_list_courses" --params '{}'

# Get course details
clawlink_call_tool --tool "google_classroom_get_course" --params '{"id": "course-id"}'

# List students in a course
clawlink_call_tool --tool "google_classroom_list_students" --params '{"course_id": "course-id"}'

# List coursework
clawlink_call_tool --tool "google_classroom_list_course_work" --params '{"course_id": "course-id"}'
```

## Authentication

All Google Classroom tool calls are authenticated automatically by ClawLink using the user's connected Google account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Google Classroom API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=google-classroom and connect Google Classroom.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `google-classroom` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration google-classroom
```

**Response:** Returns the live tool catalog for Google Classroom.

### Reconnect

If Google Classroom tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=google-classroom
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration google-classroom`

## Security & Permissions

- Access is scoped to Google Classroom courses the connected account can manage.
- Teachers can manage their own courses; students have read-only access to their enrolled courses.
- **All write operations require explicit user confirmation.** Before executing any coursework creation, announcement posting, or grade changes, confirm the intended effect with the user.
- Destructive actions (deleting coursework, removing students) are marked as high-impact and must be confirmed.

## Tool Reference

### Courses

| Tool | Description | Mode |
|------|-------------|------|
| `google_classroom_list_courses` | List courses the user is enrolled in or teaches | Read |
| `google_classroom_get_course` | Get course details | Read |
| `google_classroom_create_course` | Create a new course | Write |
| `google_classroom_update_course` | Update course name, description, or section | Write |
| `google_classroom_delete_course` | Delete a course | Write |

### Coursework

| Tool | Description | Mode |
|------|-------------|------|
| `google_classroom_list_course_work` | List all coursework in a course | Read |
| `google_classroom_get_course_work` | Get specific coursework details | Read |
| `google_classroom_create_course_work` | Create new assignment or question | Write |
| `google_classroom_update_course_work` | Update an existing assignment | Write |
| `google_classroom_delete_course_work` | Delete coursework | Write |

### Students & Teachers

| Tool | Description | Mode |
|------|-------------|------|
| `google_classroom_list_students` | List students enrolled in a course | Read |
| `google_classroom_list_teachers` | List teachers of a course | Read |
| `google_classroom_add_student` | Add a student to a course | Write |
| `google_classroom_add_teacher` | Add a teacher to a course | Write |
| `google_classroom_remove_student` | Remove a student from a course | Write |
| `google_classroom_remove_teacher` | Remove a teacher from a course | Write |

### Submissions

| Tool | Description | Mode |
|------|-------------|------|
| `google_classroom_list_submissions` | List student submissions for coursework | Read |
| `google_classroom_get_submission` | Get submission details and grade | Read |
| `google_classroom_patch_submission` | Update submission grade or status | Write |

### Announcements

| Tool | Description | Mode |
|------|-------------|------|
| `google_classroom_list_announcements` | List announcements in a course | Read |
| `google_classroom_create_announcement` | Post an announcement to a course | Write |
| `google_classroom_delete_announcement` | Delete an announcement | Write |

## Code Examples

### List all courses

```bash
clawlink_call_tool --tool "google_classroom_list_courses" \
  --params '{}'
```

### List students in a course

```bash
clawlink_call_tool --tool "google_classroom_list_students" \
  --params '{
    "course_id": "course-id"
  }'
```

### Create a new assignment

```bash
clawlink_call_tool --tool "google_classroom_create_course_work" \
  --params '{
    "course_id": "course-id",
    "title": "Week 5 Homework",
    "description": "Complete exercises 1-10 from Chapter 5",
    "due_date": {
      "year": 2025,
      "month": 2,
      "day": 15
    },
    "work_type": "ASSIGNMENT",
    "state": "PUBLISHED"
  }'
```

### Post an announcement

```bash
clawlink_call_tool --tool "google_classroom_create_announcement" \
  --params '{
    "course_id": "course-id",
    "text": "Reminder: The midterm exam is scheduled for next Tuesday. Please review Chapters 1-8.",
    "state": "PUBLISHED"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Classroom is connected.
2. Call `clawlink_list_tools --integration google-classroom` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `google-classroom`.
5. If no Google Classroom tools appear, direct the user to https://claw-link.dev/dashboard?add=google-classroom.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List courses → Get course → List students         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Preview announcement → User confirms              │
│           → Execute post                                     │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Course IDs are unique strings (e.g., `abc123xyz`) assigned by Google Classroom.
- Only teachers and administrators can create or modify coursework and announcements.
- Students can only view their own submissions and grades.
- Coursework `due_date` requires year, month, and day fields.
- Deleting a course removes all associated coursework, submissions, and announcements.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration google-classroom`. |
| Missing connection | Google Classroom is not connected. Direct the user to https://claw-link.dev/dashboard?add=google-classroom. |
| `404 Not Found` | Course, student, or coursework does not exist. Verify the IDs. |
| `403 Forbidden` | The connected account is not a teacher or admin for this course. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `google-classroom`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Google Classroom API Reference](https://developers.google.com/classroom/reference/rest)
- [Google Classroom API Overview](https://developers.google.com/classroom/api/guides/overview)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-classroom-education)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Related Skills

- [Google Calendar](https://clawhub.ai/hith3sh/google-calendar-scheduling) — For scheduling class sessions
- [Google Drive](https://clawhub.ai/hith3sh/google-drive) — For file management in Classroom

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-classroom-education)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)