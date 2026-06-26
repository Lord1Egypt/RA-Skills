# CV Information Requirements

## Collection Checklist

**Required fields**

| Field | Required sub-fields |
|------|------|
| Name | — |
| Contact | Phone number with country code, email |
| Education | Institution full name, major, degree level (for example BSc/BA/MSc), study dates, GPA with scale; optional: location, class rank, core courses and grades |
| Experiences | At least one of research / internship / project / activity; each entry must include organization or project name, role, dates, and concrete responsibilities or actions |

**Optional fields**

| Field | Notes |
|------|------|
| Target program / field | Helps prioritize experiences and bullet emphasis |
| Experiences to emphasize | Which items the user wants to foreground |
| Awards | Name, date |
| Skills | Programming languages, software tools, language scores such as IELTS, certificates |
| Hobbies | — |

## Validation Rules

The Phase 1 gate checks **coverage**, not quantity or quality.

- **Addressed** means either:
  - the user provided that category with all required sub-fields, or
  - the user explicitly said they have nothing for that category, such as "I do not have research experience."
- **Not addressed** means either:
  - the category was never discussed, or
  - the category was mentioned but still lacks required sub-fields, such as an education entry with only the school name and no degree, major, or GPA.

Material quality and depth, such as the number of experiences or the detail inside bullet points, are judged in Phase 2 and do not block the Phase 1 gate.

## Material-Mining Strategy

1. Collect by module: education first, then experiences in this priority order: research -> internship -> project -> campus activity -> extracurricular activity, then awards and skills.
2. For each experience, mine bullet-point material by asking:
   - "What exactly did you do in this experience? Which methods, tools, or technologies did you use?"
   - "What came out of the work? Do you have measurable results?" Prompt with examples such as volume handled, efficiency change, or number of users served.
   - "What was the biggest challenge in this project or internship, and how did you solve it?"
3. Help the user classify experiences correctly so research, projects, and internships are not mixed together.
4. Use careful inference as a questioning aid based on the role or project name.
   - Example: "You mentioned a data analytics internship at XX company. What tools did you mainly use to process the data? Did you build models or write automation scripts?"

## Sufficiency Criteria

Sufficiency is judged in Phase 2 and determines whether the workflow goes to Branch A (final version) or Branch B (reference version).

| Judgment | Criteria |
|------|------|
| Sufficient | Education information is complete, and at least 2 experiences each have 3 or more concrete actions with methods/tools and outcomes, with enough detail to support strong bullet points. |
| Thin | Any of the following: experiences contain only titles and roles, descriptions are too generic, or there is only 1 experience with limited detail. |
