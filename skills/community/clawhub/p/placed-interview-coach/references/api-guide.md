# Placed Interview Coach — API Reference

Full reference for all interview coaching tools available via the Placed MCP server.

## Authentication

All tools require a Bearer token:

```
Authorization: Bearer $PLACED_API_KEY
```

---

## start_interview_session

Begin a mock interview session.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume to use for context |
| `job_title` | string | yes | Target job title |
| `difficulty` | string | no | `easy`, `medium`, `hard` (default: `medium`) |
| `company` | string | no | Target company (tailors question style) |

**Returns:** `{ session_id, first_question }`

---

## continue_interview_session

Submit an answer and receive the next question with immediate feedback.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | string | yes | Session ID from `start_interview_session` |
| `user_answer` | string | yes | Your answer to the current question |

**Returns:** `{ next_question, question_feedback, session_complete, questions_remaining }`

`question_feedback` includes:

- `score` (0-10)
- `strengths` — what you did well
- `improvements` — specific suggestions
- `model_answer` — example strong answer

---

## get_interview_feedback

Get comprehensive performance analysis for a completed session.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | string | yes | Completed session ID |

**Returns:**

```json
{
  "overall_score": 7.5,
  "technical_depth": 8.0,
  "communication": 7.0,
  "problem_solving": 7.5,
  "strengths": ["Clear explanation of trade-offs", "Good edge case handling"],
  "improvements": ["Discuss time complexity earlier", "Ask clarifying questions first"],
  "question_breakdown": [...],
  "recommended_topics": ["Dynamic programming", "Graph traversal"],
  "next_session_difficulty": "hard"
}
```

---

## list_interview_cases

Browse available system design cases.

**Parameters:** None

**Returns:** Array of `{ case_id, title, difficulty, category, description, key_concepts }`

**Available cases include:**

- `design-url-shortener` — Hash functions, collision handling, database design
- `design-twitter` — Feed generation, real-time updates, distributed systems
- `design-netflix` — Video streaming, CDN, recommendation engine
- `design-uber` — Geolocation, real-time matching, consistency
- `design-instagram` — Photo storage, feed ranking, sharding
- `design-slack` — Real-time messaging, presence, search
- `design-google-drive` — File storage, sync, versioning
- `design-rate-limiter` — Token bucket, sliding window, distributed rate limiting
- `design-distributed-cache` — Eviction policies, consistency, replication
- `design-search-autocomplete` — Trie, ranking, personalization

---

## start_system_design

Start a system design interview session.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `case_id` | string | yes | Case ID from `list_interview_cases` |
| `difficulty` | string | no | `junior`, `mid`, `senior` (default: `mid`) |

**Returns:** `{ session_id, case_description, requirements_prompt }`

---

## get_behavioral_questions

Get behavioral interview questions for a target role.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `target_role` | string | yes | Target job title |
| `focus_categories` | array | no | Categories to focus on (see below) |

**Available categories:**

- `leadership` — Led teams, made decisions, drove initiatives
- `conflict-resolution` — Disagreements, difficult people, competing priorities
- `failure` — Mistakes, failed projects, lessons learned
- `teamwork` — Cross-team collaboration, helping others succeed
- `initiative` — Took ownership, improved processes, solved problems
- `pressure` — Tight deadlines, high stakes, ambiguity
- `growth` — Learning, feedback, career development
- `technical-decisions` — Architecture choices, trade-offs, technical debt

**Returns:** Array of `{ question, category, follow_ups, what_interviewers_look_for }`

---

## save_story_to_bank

Save a STAR story for reuse across interviews.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `situation` | string | yes | Context and background |
| `task` | string | yes | Your specific responsibility |
| `action` | string | yes | What you did (be specific) |
| `result` | string | yes | Quantified outcome |
| `category` | string | yes | Story category (see `get_behavioral_questions` categories) |

**Returns:** `{ story_id, category, created_at }`

---

## Session States

| State       | Description                                |
| ----------- | ------------------------------------------ |
| `active`    | Session in progress                        |
| `completed` | All questions answered, feedback available |
| `abandoned` | Session timed out or cancelled             |

Sessions expire after 2 hours of inactivity.

---

## Error Codes

| Code                | Meaning                                                 |
| ------------------- | ------------------------------------------------------- |
| `SESSION_NOT_FOUND` | Session ID invalid or expired                           |
| `SESSION_COMPLETE`  | Session already finished — use `get_interview_feedback` |
| `RESUME_NOT_FOUND`  | Resume ID invalid                                       |
| `CASE_NOT_FOUND`    | System design case ID invalid                           |
| `INVALID_CATEGORY`  | Behavioral category not recognized                      |
