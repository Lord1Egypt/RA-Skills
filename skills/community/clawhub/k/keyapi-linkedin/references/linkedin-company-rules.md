# LinkedIn Company Module Rules

## 1. Module Scope

Use this module for LinkedIn company profile, employees, company posts, and company hiring footprint.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. Company profile baseline

- Documentation: `https://docs.keyapi.ai/en/linkedin/get_company_profile.md`
- Purpose: Retrieve company profile information before employee, post, or hiring workflows.

### Best Suited For

- company validation
- account research
- firmographic summaries
- company report baseline

### Routing Rules

- Use this first when the company identity is ambiguous.
- Preserve company identifiers needed for people, posts, and job endpoints.
- Do not infer private financial or employee data beyond returned fields.

## 3. Employee and people mapping

- Documentation: `https://docs.keyapi.ai/en/linkedin/get_company_people.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_profile.md`
- Purpose: Retrieve employees associated with a company and optionally enrich selected people.

### Best Suited For

- org mapping
- lead discovery
- hiring/team structure research
- employee shortlist enrichment

### Routing Rules

- Use company people after company identity is resolved.
- Enrich only selected people with user module endpoints.
- Do not treat returned employee list as complete unless the API docs define coverage.

## 4. Company content activity

- Documentation: `https://docs.keyapi.ai/en/linkedin/get_company_posts.md`
- Purpose: Retrieve posts published by a company.

### Best Suited For

- brand activity review
- content monitoring
- company communications analysis

### Routing Rules

- Use after company profile when the user asks about content or announcements.
- Enrich people or job context only when the user asks for adjacent analysis.

## 5. Hiring footprint

- Documentation: `https://docs.keyapi.ai/en/linkedin/get_company_job_count.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_company_jobs.md`
- Purpose: Quantify and inspect open roles tied to a company.

### Best Suited For

- hiring demand checks
- role/category monitoring
- company growth signals

### Routing Rules

- Use job count for quick hiring footprint.
- Use company jobs when listings are needed.
- Use job detail from the jobs module only for selected roles.

## 6. Common Workflows

- Company report: company profile -> company people/posts/jobs depending on requested sections.
- Hiring analysis: company profile -> job count -> company jobs -> selected job detail.
- Account research: company profile -> company posts -> key employees if requested.
