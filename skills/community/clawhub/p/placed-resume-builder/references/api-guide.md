# Placed Resume Builder — API Reference

Full reference for all resume builder tools available via the Placed MCP server.

## Authentication

All tools require a Bearer token:

```
Authorization: Bearer $PLACED_API_KEY
```

---

## create_resume

Create a new resume.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | yes | Resume name (e.g., "Senior Engineer Resume") |
| `target_role` | string | no | Target job title for AI optimization hints |
| `summary` | string | no | Professional summary |
| `skills` | array | no | List of skills |
| `use_profile_experience` | boolean | no | Include experience from your profile (default: false) |
| `use_profile_education` | boolean | no | Include education from your profile (default: false) |

**Returns:** `{ resume_id, title, created_at }`

**Example:**

```json
{
  "title": "Staff Engineer Resume",
  "target_role": "Staff Software Engineer",
  "use_profile_experience": true,
  "use_profile_education": true
}
```

---

## get_resume

Retrieve a resume with all sections.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | no | Resume ID (defaults to most recent resume) |

**Returns:** Full resume object with all populated sections.

---

## update_resume

Update any part of a resume. All fields are optional — only include what you want to change.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |
| `title` | string | no | New resume title |
| `slug` | string | no | URL-friendly slug |
| `visibility` | string | no | `public` or `private` |
| `summary` | string | no | Professional summary (HTML allowed) |
| `basics` | object | no | Basic info (name, email, phone, headline, location) |
| `experience` | array | no | Work experience entries |
| `education` | array | no | Education entries |
| `skills` | array | no | Skills list |
| `languages` | array | no | Language proficiencies |
| `certifications` | array | no | Professional certifications |
| `awards` | array | no | Awards and honors |
| `projects` | array | no | Projects |
| `publications` | array | no | Publications |
| `references` | array | no | Professional references |
| `volunteer` | array | no | Volunteer experience |
| `interests` | array | no | Interests and hobbies |
| `profiles` | array | no | Social profiles (LinkedIn, GitHub, etc.) |

**Section data shapes:**

### basics

```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1-555-0100",
  "headline": "Senior Software Engineer",
  "location": "San Francisco, CA"
}
```

### experience

```json
[
  {
    "company": "Acme Corp",
    "title": "Senior Software Engineer",
    "location": "San Francisco, CA",
    "startDate": "2020-01",
    "endDate": "present",
    "bullets": [
      "Led migration of monolith to microservices, reducing deploy time by 60%",
      "Mentored 4 junior engineers, 2 promoted within 12 months"
    ]
  }
]
```

### education

```json
[
  {
    "institution": "Stanford University",
    "degree": "B.S. Computer Science",
    "graduationDate": "2017-05",
    "gpa": "3.8",
    "honors": "Magna Cum Laude"
  }
]
```

### skills

```json
["Python", "Go", "Kubernetes", "PostgreSQL", "Docker"]
```

---

## list_resumes

List all resumes for the authenticated user.

**Parameters:** None

**Returns:** Array of `{ resume_id, title, template_id, updated_at, sections_count }`

---

## get_resume_schema

Get the full JSON schema for all resume sections.

**Parameters:** None

**Returns:** JSON Schema object describing all fields, types, and constraints.

---

## list_resume_templates

Browse all 37 available resume templates.

**Parameters:** None

**Returns:** Array of `{ template_id, name, category, preview_url }`

---

## get_template_preview

Get details and preview for a specific template.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `template_id` | string | yes | Template ID from `list_resume_templates` |

**Returns:** `{ template_id, name, description, preview_url, ats_score, best_for }`

---

## change_resume_template

Apply a template to a resume. Non-destructive — content is preserved.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |
| `template_id` | string | yes | Template ID to apply |

**Returns:** `{ resume_id, template_id, updated_at }`

---

## get_resume_pdf_url

Generate a PDF download URL. URL expires in 15 minutes.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |

**Returns:** `{ url, expires_at }`

---

## get_resume_docx_url

Generate a DOCX (Word) download URL.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |

**Returns:** `{ url, expires_at }`

---

## export_resume_json

Export resume as structured JSON.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |

**Returns:** Full resume JSON object (same schema as `get_resume`).

---

## export_resume_markdown

Export resume as formatted Markdown text.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_id` | string | yes | Resume ID |

**Returns:** `{ markdown }` — Formatted Markdown string.

---

## Error Codes

| Code                      | Meaning                                            |
| ------------------------- | -------------------------------------------------- |
| `RESUME_NOT_FOUND`        | Resume ID doesn't exist or belongs to another user |
| `TEMPLATE_NOT_FOUND`      | Template ID is invalid                             |
| `INVALID_SECTION`         | Section name is not recognized                     |
| `SCHEMA_VALIDATION_ERROR` | Section data doesn't match expected schema         |
| `EXPORT_FAILED`           | PDF/DOCX generation failed — retry                 |
| `RATE_LIMIT_EXCEEDED`     | Too many requests — wait and retry                 |

---

## Rate Limits

| Tier    | Requests/min | Exports/day |
| ------- | ------------ | ----------- |
| Free    | 10           | 5           |
| Pro     | 60           | 50          |
| Premium | 300          | unlimited   |
