# LinkedIn Jobs Module Rules

## 1. Module Scope

Use this module for LinkedIn company job count, company job listings, and selected job detail.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. Job demand sizing

- Documentation: `https://docs.keyapi.ai/en/linkedin/get_company_job_count.md`
- Purpose: Estimate hiring footprint for a company.

### Best Suited For

- quick open-role count
- hiring trend proxy
- company screening

### Routing Rules

- Use when the user asks how many jobs a company has or needs a quick hiring signal.
- Pair with company profile when company identity is uncertain.
- Do not treat count as a complete labor-market trend without listings or repeated measurements.

## 3. Company job listings

- Documentation: `https://docs.keyapi.ai/en/linkedin/get_company_jobs.md`
- Purpose: Retrieve job listings for a company.

### Best Suited For

- open role research
- job category scan
- recruiting or competitive hiring analysis

### Routing Rules

- Use after company identity is known.
- Apply documented filters and pagination; stop when requested result size is met.
- Preserve job identifiers for detail calls.

## 4. Selected job detail

- Documentation: `https://docs.keyapi.ai/en/linkedin/get_job_detail.md`
- Purpose: Retrieve detailed information for one selected job.

### Best Suited For

- role requirement analysis
- job description extraction
- compensation/location/detail checks when returned

### Routing Rules

- Use only after a job ID is known or selected from listings.
- For multiple jobs, shortlist first and then fetch details for selected roles.

## 5. Common Workflows

- Hiring report: company profile -> job count -> company jobs -> selected job detail.
- Role analysis: company jobs -> shortlist by title/location -> job detail for selected roles.
