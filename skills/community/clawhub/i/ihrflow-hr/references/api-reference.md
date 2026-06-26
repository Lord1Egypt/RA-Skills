# iHRFlow MCP Tool & Resource Reference

Complete parameter tables and response schemas for all 20 MCP tools and 2 MCP resources.

---

## Authentication

### `login`

Authenticate user session. Must be called before other tools (unless server has default credentials).

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | yes | Username |
| `password` | string | yes | Password |
| `tenant_id` | string | no | Tenant ID (required for multi-tenant) |

**Response:** `{"status": "ok", "message": "登录成功，用户: xxx"}`

---

## Candidate Management

### `search_candidates`

Search resumes by keyword. Uses AI semantic search engine (skill matching, synonym expansion).

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `keyword` | string | yes | Search keyword, e.g. "Java 3年经验", "张三", "北京大学" |
| `page` | int | no | Page number, default 1 |
| `page_size` | int | no | Items per page, default 10, max 100 |

**Response:**
```json
{
  "total": 42,
  "page": 1,
  "candidates": [
    {
      "id": "uuid",
      "name": "张三",
      "match_score": 0.85,
      "skills": ["Java", "Spring Boot"],
      "location": "北京",
      "experience": 5,
      "match_type": "vector",
      "match_label": "精确匹配",
      "is_exact_match": true
    }
  ]
}
```

### `get_resume_detail`

Get full resume details (education, work history, skills, etc.).

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |

**Response:** Full resume object from backend.

### `add_resume_note`

Add a note to a resume (communication logs, assessments, etc.).

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |
| `content` | string | yes | Note content, max 2000 chars |

### `recommend_candidate_for_position`

Recommend a candidate to a specific position, entering its screening pipeline.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Candidate resume ID |
| `position_id` | string | yes | Target position ID |
| `reason` | string | no | Recommendation reason, max 1000 chars |

---

## Position Management

### `list_positions`

List positions with optional status filter.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | no | Filter: `pending`, `active`, `paused`, `closed` |
| `page` | int | no | Page number, default 1 |
| `page_size` | int | no | Items per page, default 10 |

**Response:**
```json
{
  "total": 15,
  "page": 1,
  "positions": [
    {
      "id": "uuid",
      "title": "高级Java工程师",
      "department": "技术部",
      "status": "active",
      "headcount": 3,
      "hired_count": 1,
      "recruiter_name": "李四",
      "location": "北京",
      "salary_range": "25k-35k"
    }
  ]
}
```

### `get_position_detail`

Get full position details (description, requirements, interview flow, etc.).

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `position_id` | string | yes | Position ID |

### `get_position_candidates`

List candidates under a specific position with filtering.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `position_id` | string | yes | Position ID |
| `status` | string | no | Filter: `pending`, `approved`, `rejected`, `interviewing` |
| `search` | string | no | Name/email search keyword |
| `page` | int | no | Page number, default 1 |
| `page_size` | int | no | Items per page, default 10 |

**Response:**
```json
{
  "total": 8,
  "page": 1,
  "candidates": [
    {
      "resume_id": "uuid",
      "name": "王五",
      "screening_status": "hr_approved",
      "applied_at": "2026-03-10T09:00:00",
      "email": "wangwu@example.com"
    }
  ]
}
```

### `update_position_status`

Change position status (publish, pause, close).

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `position_id` | string | yes | Position ID |
| `status` | string | yes | Target status: `active`, `paused`, `closed` |

### `create_recruitment_need`

Create a new position/recruitment need.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | yes | Position title, e.g. "高级Java工程师" |
| `department` | string | yes | Department name |
| `headcount` | int | no | Headcount, default 1, max 1000 |
| `description` | string | no | Job description, max 5000 chars |
| `requirements` | string | no | Requirements, max 5000 chars |
| `salary_range` | string | no | Salary range, e.g. "20k-30k" |
| `location` | string | no | Work location |

---

## Interview Management

### `list_interviews`

List interviews with optional status filter.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | no | Filter: `to_be_scheduled`, `scheduled`, `pending_evaluation`, `completed`, `cancelled` |
| `page` | int | no | Page number |
| `page_size` | int | no | Items per page |

**Response:**
```json
{
  "total": 5,
  "page": 1,
  "interviews": [
    {
      "id": "uuid",
      "candidate_name": "张三",
      "position_title": "高级Java工程师",
      "interviewer_name": "李四",
      "scheduled_time": "2026-03-15T14:00:00",
      "status": "scheduled",
      "round_number": 1,
      "interview_type": "technical"
    }
  ]
}
```

### `get_interview_detail`

Get full interview details (interviewers, schedule, feedback, etc.).

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `interview_id` | string | yes | Interview ID |

### `create_interview`

Schedule a new interview.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Candidate resume ID |
| `position_id` | string | yes | Position ID |
| `interviewer_id` | string | yes | Interviewer user ID |
| `scheduled_at` | string | yes | Interview time, ISO 8601 (e.g. "2026-03-15T14:00:00") |
| `duration_minutes` | int | no | Duration in minutes, default 60, range 15-480 |
| `round_number` | int | no | Interview round (1, 2, 3, ...) |
| `round_name` | string | no | Round name (e.g. "技术面", "HR面") |
| `location_type` | string | no | Format: `online` (default), `offline` |
| `meeting_link` | string | no | Online meeting URL |

### `cancel_interview`

Cancel a scheduled interview.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `interview_id` | string | yes | Interview ID |

### `reschedule_interview`

Reschedule an interview to a new date/time.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `interview_id` | string | yes | Interview ID |
| `new_date` | string | yes | New date, YYYY-MM-DD |
| `new_time` | string | yes | New time, HH:MM |
| `reason` | string | no | Reason for rescheduling |

---

## Screening Pipeline

### `update_screening_status`

Advance or reject a candidate in the screening pipeline.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Candidate resume ID |
| `action` | string | yes | Pipeline action (see below) |
| `notes` | string | no | Notes, max 1000 chars |

**Action values:**

| Action | Description | Pipeline Effect |
|--------|-------------|-----------------|
| `hr_approve` | HR initial screening pass | pending -> hr_approved |
| `hr_reject` | HR initial screening reject | pending -> hr_rejected |
| `dept_approve` | Department screening pass | -> dept_approved |
| `dept_reject` | Department screening reject | -> dept_rejected |
| `final_approve` | Final approval (send offer) | -> final_approved |
| `final_reject` | Final rejection | -> final_rejected |

**Full backend pipeline (including exam phase managed outside MCP):**
```
pending -> hr_approved -> exam_pending -> exam_in_progress -> exam_passed
-> dept_screening -> dept_approved -> interview_pending -> interview_scheduled
-> interview_in_progress -> interview_passed -> final_approved
```

Note: Exam phase transitions (`exam_pending` through `exam_passed`) and interview sub-state transitions are managed by the backend automatically. MCP tools handle the HR/dept/final approval gates.

---

## Interview Evaluation

### `submit_interview_feedback`

Submit interviewer feedback. Creates an evaluation record and submits manual feedback.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `interview_id` | string | yes | Interview ID |
| `passed` | bool | yes | Whether the candidate passed |
| `feedback` | string | yes | Evaluation content, min 10 chars |
| `score` | int | no | Interview score 1-100 |
| `notes` | string | no | Additional notes |

**Internal flow:** POST `/interview-evaluations/{interview_id}/evaluation` to create record, then POST `/interview-evaluations/{evaluation_id}/manual-feedback` with feedback data.

---

## Talent Search

### `search_talent`

AI-powered semantic talent search (Redis vectors + Neo4j tags + text fallback).

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | yes | Natural language query, e.g. "3年以上Python后端，熟悉微服务" |
| `top_k` | int | no | Number of results, default 10, max 100 |

**Response:**
```json
{
  "query": "Python后端",
  "results": [
    {
      "id": "uuid",
      "name": "张三",
      "match_score": 0.92,
      "skills": ["Python", "FastAPI", "Docker"],
      "location": "上海",
      "experience": 4,
      "match_type": "vector",
      "match_label": "高度匹配"
    }
  ]
}
```

---

## Statistics & Schedule

### `get_recruitment_statistics`

Get overall recruitment statistics. No parameters.

**Response:**
```json
{
  "position_stats": { "total": 15, "active": 8, "closed": 5, "paused": 2 },
  "interview_stats": { "total": 42, "scheduled": 5, "completed": 30, "cancelled": 7 }
}
```

### `get_today_schedule`

Get today's schedule (interviews, meetings, etc.). No parameters.

**Response:**
```json
{
  "date": "2026-03-12",
  "event_count": 3,
  "events": [
    { "type": "interview", "time": "14:00", "title": "技术面 - 张三", "status": "scheduled" }
  ]
}
```

---

## MCP Resources

Resources are read-only contextual data accessed via `resources/read` method.

### `ihrflow://recruitment/overview`

Current recruitment overview: position stats and interview stats summary.

**Response:** JSON with `position_stats` and `interview_stats` objects.

### `ihrflow://positions/active`

All currently active (recruiting) positions.

**Response:**
```json
{
  "total": 8,
  "positions": [
    { "id": "uuid", "title": "高级Java工程师", "department": "技术部", "headcount": 3, "hired_count": 1 }
  ]
}
```

---

## Domain Reference

### Position Status Values

| Status | Description |
|--------|-------------|
| `pending` | Created, not yet published |
| `active` | Actively recruiting |
| `paused` | Temporarily paused |
| `closed` | Closed (filled or cancelled) |

### Interview Status Values

| Status | Description |
|--------|-------------|
| `to_be_scheduled` | Awaiting scheduling |
| `scheduled` | Scheduled, not yet conducted |
| `pending_evaluation` | Conducted, awaiting feedback |
| `completed` | Feedback submitted |
| `cancelled` | Cancelled |

### Candidate Screening Status Values

| Status | Description |
|--------|-------------|
| `pending` | Awaiting HR review |
| `hr_approved` / `hr_rejected` | HR screening result |
| `exam_pending` / `exam_passed` / `exam_failed` | Exam phase (auto-managed) |
| `dept_approved` / `dept_rejected` | Department screening result |
| `interview_pending` / `interview_scheduled` / `interview_passed` / `interview_failed` | Interview phase |
| `final_approved` / `final_rejected` | Final decision |
