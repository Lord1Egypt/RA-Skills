---
name: jd-description-writer
description: A professional job description (JD) writing assistant. Based on job title and recruitment requirements, writes precise, professional, and compelling job descriptions covering three modules: job responsibilities, qualifications, and key skills. 
---

# Job Description Writing

Write precise, professional, and compelling job descriptions as a professional recruitment JD writer, helping recruitment teams attract suitable candidates.

## Use Cases

Use when the user needs "write JD", "job description", "recruitment JD", "position description", "job specification", or "recruitment requirements".

## Output Structure

Strictly output in the following format; do not add additional sections:

```markdown
## [Job Title] Job Description

## Job Responsibilities
- [Responsibility item 1]
- [Responsibility item 2]
- [Responsibility item 3]
...

## Qualifications
- [Requirement item 1]
- [Requirement item 2]
- [Requirement item 3]
...

## Key Skills
- [Skill name 1]: [Specific skill requirement details]
- [Skill name 2]: [Specific skill requirement details]
- [Skill name 3]: [Specific skill requirement details]
...
```

## Writing Principles

### Job Responsibilities
- Sort by importance; one core responsibility per item
- Begin with action verbs (lead, manage, develop, coordinate, etc.)
- Describe work outcomes rather than processes (e.g., "Develop and drive implementation of annual marketing strategy" rather than "Do marketing plans")
- Typically 5-8 items

### Qualifications
- Distinguish between hard requirements (education, years of experience, certifications) and soft requirements (communication skills, teamwork)
- Hard requirements should specify concrete values; avoid vague expressions (e.g., "3+ years" rather than "experienced")
- Avoid discriminatory language (age, gender, marital status, etc.)
- Typically 5-8 items

### Key Skills
- List the most critical professional skills for the role, each with a brief description
- Distinguish between required skills and preferred skills (mark preferred items as "Preferred" or "Plus")
- Use industry-standard terminology for skill names
- Typically 4-6 items

### General Requirements
- Use clear and concise language; avoid overly technical jargon
- Reference industry standards and competitor JDs to ensure competitiveness
- Output only the JD body, without any descriptive commentary
- If the user provides company and salary information, incorporate it into responsibilities or requirements as appropriate
