# Job Hunter Data Formats

## Search Parameters

```json
{
  "keywords": "Python developer",
  "technologies": ["Python", "FastAPI", "AWS"],
  "countries": ["Spain", "Germany"],
  "remote": true,
  "experience": "mid",
  "exclude": ["consultant", "staffing"],
  "company_size": ["4", "5", "6"],
  "salary_min": 40000,
  "ai_prompt": "Must use microservices architecture",
  "max_pages": 3,
  "min_score": 0.6
}
```

### Experience Levels
- `internship`, `entry`, `associate`, `mid`, `senior`, `director`, `executive`

### Company Size Codes (LinkedIn f_CS)
- `1`: 1-10 employees
- `2`: 11-50
- `3`: 51-200
- `4`: 201-500
- `5`: 501-1000
- `6`: 1001-5000
- `7`: 5001-10000
- `8`: 10001+

## Search Result (per job)

```json
{
  "title": "Senior Python Engineer",
  "company": "TechCorp",
  "location": "Madrid, Spain",
  "url": "https://www.linkedin.com/jobs/view/12345",
  "posted_at": "2026-03-18",
  "salary": "€50,000 - €60,000",
  "ai_score": 0.92,
  "ai_summary": "Excelente match: remoto, Python/FastAPI, ubicación Madrid"
}
```

## Saved Job

```json
{
  "title": "Senior Python Engineer",
  "company": "TechCorp",
  "location": "Madrid, Spain",
  "url": "https://www.linkedin.com/jobs/view/12345",
  "score": 0.92,
  "notes": "Applied on 2026-03-19",
  "saved_at": "2026-03-19T10:30:00"
}
```

## Config

```json
{
  "gemini_api_key": "...",
  "gemini_model": "gemini-2.5-flash",
  "min_ai_score": 0.6,
  "max_pages": 3
}
```
