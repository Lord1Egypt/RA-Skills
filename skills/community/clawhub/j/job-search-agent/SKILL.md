---
name: job-search-agent
version: 1.0.0
description: AI-powered job search assistant that searches multiple job boards, matches opportunities against your CV, and helps you apply faster.
tags: jobs, career, automation, job-search, employment
license: MIT
---

# Job Search Agent

> Let AI find your dream job. Automated job search, CV matching, and applications.

## Features

- **Multi-platform job search**: Search LinkedIn Jobs, Indeed, Glassdoor, and more from one place
- **Smart CV matching**: Automatically match job requirements against your skills and experience
- **Auto-apply**: Apply to multiple matching jobs with one command
- **Application tracking**: Keep track of all your applications in one place
- **Cover letter generation**: Generate personalized cover letters for each application

## Supported Platforms

- LinkedIn Jobs
- Indeed
- Glassdoor
- JSearch API
- RemoteOK
- WeWorkRemotely

## Usage Examples

### Basic Job Search

```
"Find software engineer jobs in San Francisco"
"Search for remote Python developer positions paying $150k+"
"Look for senior backend roles at startups"
```

### CV Matching

```
"Match these jobs against my CV and rank by fit"
"Show me only jobs that match at least 80% of my skills"
"What skills should I add to my CV to match more jobs?"
```

### Auto-Apply

```
"Apply to the top 10 matching jobs"
"Apply to all remote positions under my salary threshold"
```

## Configuration

```json
{
  "search": {
    "keywords": ["python", "backend", "machine learning"],
    "locations": ["remote", "San Francisco"],
    "salary_min": 120000
  },
  "profile": {
    "experience_years": 5,
    "skills": ["Python", "FastAPI", "PostgreSQL", "AWS"]
  }
}
```

## Service Pricing

| Service | Price |
|---------|-------|
| Basic Setup | $100-200 |
| CV Optimization | $50-100 |
| Premium Auto-Apply | $200-400 |

---

*Version: 1.0.0*
*Author: OpenClaw Community*