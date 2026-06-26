# Placed Career Tools — API Reference

Full reference for all career tools available via the Placed API.

## Authentication

All tools require a Bearer token:

```
Authorization: Bearer $PLACED_API_KEY
```

---

## add_job_application

Add a new job application to your tracker.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `company` | string | yes | Company name |
| `position` | string | yes | Job title/position |
| `job_url` | string | no | URL to the job posting |
| `job_description` | string | no | Job description text |
| `location` | string | no | Job location |
| `work_type` | string | no | `remote`, `hybrid`, `onsite` |
| `status` | string | no | Initial status (default: `WISHLIST`) |
| `resume_id` | string | no | Resume used for this application |
| `notes` | string | no | Private notes |

**Status values:** `WISHLIST`, `APPLIED`, `INTERVIEWING`, `OFFER`, `REJECTED`, `WITHDRAWN`

**Returns:** `{ id, company, position, status, created_at }`

---

## list_job_applications

View your application pipeline.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | no | Filter by status (see status values above) |

**Returns:** Array of application objects with full details.

---

## update_job_status

Move an application to a new stage.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `job_id` | string | yes | Job application ID |
| `status` | string | yes | New status (see status values above) |
| `notes` | string | no | Notes about the status change |

**Returns:** Updated application object.

---

## delete_job_application

Delete an application from the tracker.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `job_id` | string | yes | Job application ID |

---

## get_application_analytics

Get pipeline analytics and conversion rates.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `date_range` | string | no | `7d`, `30d`, `90d`, `all` (default: `all`) |

**Returns:**

```json
{
  "total_applications": 24,
  "by_status": { "APPLIED": 10, "INTERVIEWING": 6, "OFFER": 2, "REJECTED": 6 },
  "conversion_rates": {
    "applied_to_interviewing": 0.42,
    "interviewing_to_offer": 0.33
  },
  "avg_days_to_response": 8
}
```

---

## match_job

Score how well your resume matches a job description.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |
| `job_description` | string | yes | Full job description text |

**Returns:**

```json
{
  "match_score": 78,
  "matched_keywords": ["distributed systems", "Go", "Kubernetes"],
  "missing_keywords": ["Kafka", "gRPC", "service mesh"],
  "recommendation": "Strong match. Add Kafka and gRPC to skills section."
}
```

---

## analyze_resume_gaps

Find missing keywords and skills for a target role.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |
| `job_description` | string | yes | Job description text |

**Returns:** `{ critical_gaps, nice_to_have_gaps, keyword_gaps, matched_keywords, gap_score }`

---

## generate_cover_letter

Generate a tailored cover letter.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |
| `company_name` | string | yes | Company name |
| `job_title` | string | yes | Job title |
| `job_description` | string | yes | Job description text |
| `tone` | string | no | `professional`, `enthusiastic`, `formal` (default: `professional`) |

**Returns:** `{ cover_letter }` — Full cover letter text.

---

## get_interview_questions

Get likely interview questions for a company and role.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `job_description` | string | yes | Job description text |
| `company` | string | no | Company name |
| `question_count` | number | no | Number of questions (default: 10) |

**Returns:** Array of interview questions with context.

---

## generate_linkedin_profile

Generate an AI-optimized LinkedIn headline and About section.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |

**Returns:** `{ headline, about_section }`

---

## research_company

Get comprehensive company information.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `company_name` | string | yes | Company name to research |

**Returns:** `{ overview, culture, recent_news, ratings, funding, interview_style }`

---

## get_company_salary_data

Get market salary data for a role at a company.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `company_name` | string | yes | Company name |
| `position` | string | yes | Job title/position |
| `location` | string | no | Location (optional) |

**Returns:**

```json
{
  "base_salary": { "min": 180000, "median": 210000, "max": 260000 },
  "total_comp": { "median": 290000 },
  "data_points": 847
}
```

---

## generate_salary_negotiation_script

Generate a personalized salary negotiation script.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `current_offer` | number | yes | Current offer amount |
| `target_salary` | number | yes | Target salary amount |
| `justification` | array | no | List of justification points (strings) |

**Returns:** `{ script, email_template, talking_points }`

---

## analyze_offer

Analyze a job offer against market rates.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `company` | string | yes | Company name |
| `position` | string | yes | Job title |
| `base_salary` | number | yes | Base salary offer |
| `location` | string | yes | Job location |
| `bonus` | number | no | Bonus amount |
| `equity` | string | no | Equity details |

**Returns:** `{ market_comparison, recommendation, negotiation_range }`

---

## optimize_resume_for_job

Tailor resume content to a specific job description.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |
| `job_description` | string | yes | Target job description |

**Returns:** `{ suggested_changes, keyword_additions }`

---

## Error Codes

| Code                        | Meaning                                         |
| --------------------------- | ----------------------------------------------- |
| `RESUME_NOT_FOUND`          | Resume ID invalid                               |
| `JOB_DESCRIPTION_TOO_SHORT` | Job description must be at least 100 characters |
| `COMPANY_NOT_FOUND`         | Company not in database                         |
| `INSUFFICIENT_DATA`         | Not enough salary data for this combination     |
