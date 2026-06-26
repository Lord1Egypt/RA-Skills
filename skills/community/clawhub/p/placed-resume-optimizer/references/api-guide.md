# Placed Resume Optimizer — API Reference

Full reference for all resume optimization tools available via the Placed API.

## Authentication

All tools require a Bearer token:

```
Authorization: Bearer $PLACED_API_KEY
```

---

## check_ats_compatibility

Get ATS compatibility score and recommendations for a resume.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID to check |

**Returns:**

```json
{
  "ats_score": 82,
  "formatting_issues": [
    {
      "issue": "Table detected in skills section",
      "severity": "high",
      "fix": "Convert to bullet list"
    },
    {
      "issue": "Inconsistent date format",
      "severity": "medium",
      "fix": "Use MM/YYYY throughout"
    }
  ],
  "recommendations": [
    "Remove table from skills section",
    "Standardize date formats to MM/YYYY"
  ]
}
```

---

## get_resume_quality_score

Get overall resume quality score with breakdown by section.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID to score |

**Returns:** `{ overall_score, section_scores, recommendations }`

---

## match_job

Score resume-job fit with keyword breakdown.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |
| `job_description` | string | yes | Full job description text |

**Returns:**

```json
{
  "match_score": 78,
  "grade": "B+",
  "matched_keywords": ["distributed systems", "Go", "Kubernetes"],
  "missing_keywords": ["Kafka", "gRPC", "service mesh"],
  "recommendation": "Strong match. Add Kafka and gRPC to skills section to reach 85+.",
  "apply_recommendation": "yes"
}
```

**Score interpretation:**

- 90-100: Excellent match — apply immediately
- 80-89: Strong match — minor tweaks recommended
- 70-79: Good match — optimize before applying
- 60-69: Moderate match — significant gaps to address
- <60: Weak match — consider if role is right fit

---

## analyze_resume_gaps

Find missing keywords and skills vs. a job description.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |
| `job_description` | string | yes | Job description text |

**Returns:**

```json
{
  "critical_gaps": [
    {
      "keyword": "Kafka",
      "frequency_in_jd": 4,
      "suggestion": "Add to skills section if you have experience"
    }
  ],
  "nice_to_have_gaps": ["gRPC", "Istio", "Prometheus"],
  "keyword_gaps": ["distributed tracing", "observability"],
  "matched_keywords": ["Go", "Kubernetes", "microservices"],
  "gap_score": 72
}
```

---

## optimize_resume_for_job

AI-powered resume optimizer that tailors your resume to match a specific job description.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID to optimize |
| `job_description` | string | yes | Target job description |

**Returns:**

```json
{
  "suggested_changes": {
    "summary": "Updated summary text...",
    "experience": [{ "bullet_index": 2, "original": "...", "improved": "..." }],
    "skills": { "add": ["Kafka", "gRPC"], "reorder": ["Go", "Python"] }
  },
  "keyword_additions": ["distributed systems", "service mesh"],
  "match_score_before": 65,
  "match_score_after": 84
}
```

---

## optimize_resume_section

Optimize a specific resume section using AI.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID to optimize |
| `section_type` | string | yes | `experience`, `skills`, `summary`, `education` |
| `section_data` | string | yes | Current section content |
| `job_description` | string | no | Target job description for optimization |

**Returns:** `{ optimized_section, changes_made }`

---

## improve_bullet_point

Improve a single bullet point to make it more impactful and ATS-friendly.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `bullet_point` | string | yes | Current bullet point text |
| `context` | string | no | Context: job title, company, or role |

**Returns:**

```json
{
  "improved": "Optimized PostgreSQL query performance by 40%, reducing p99 latency from 500ms to 300ms for 10M+ daily active users",
  "changes_made": [
    "Added metrics",
    "Stronger action verb",
    "Added scale/impact"
  ]
}
```

---

## generate_resume_from_prompt

Generate a complete resume from natural language description.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | yes | Natural language description of experience, skills, background |
| `target_role` | string | no | Target job title for the resume |

**Returns:** `{ resume_id }` — ID of newly created resume.

---

## Scoring Rubrics

### ATS Score Components

| Component        | Weight | Description                         |
| ---------------- | ------ | ----------------------------------- |
| Formatting       | 30%    | No tables, graphics, unusual fonts  |
| Keyword density  | 30%    | Job description keywords present    |
| Parsing accuracy | 25%    | Can ATS extract all key fields      |
| Structure        | 15%    | Standard sections in expected order |

### Match Score Components

| Component            | Weight | Description                           |
| -------------------- | ------ | ------------------------------------- |
| Required skills      | 40%    | Must-have skills from job description |
| Experience level     | 25%    | Years and seniority match             |
| Nice-to-have skills  | 20%    | Preferred but not required            |
| Title/role alignment | 15%    | Job title similarity                  |

### Bullet Quality Formula

```
[Action Verb] + [What You Did] + [How/Scale] + [Quantified Result]
```

**Strong action verbs:**

- Technical: Architected, Built, Designed, Optimized, Implemented, Engineered, Migrated
- Leadership: Led, Managed, Mentored, Spearheaded, Directed
- Impact: Improved, Reduced, Increased, Accelerated, Scaled, Transformed

---

## Error Codes

| Code                        | Meaning                                         |
| --------------------------- | ----------------------------------------------- |
| `RESUME_NOT_FOUND`          | Resume ID invalid                               |
| `JOB_DESCRIPTION_TOO_SHORT` | Job description must be at least 100 characters |
| `NO_EXPERIENCE_SECTION`     | Resume has no experience section to optimize    |
| `OPTIMIZATION_FAILED`       | AI optimization failed — retry                  |
