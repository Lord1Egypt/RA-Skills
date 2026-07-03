## Description: <br>
Scrapes Indeed job listings by keyword, location, and country and returns structured job details including title, company, salary, rating, description, benefits, and application links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, recruiters, analysts, and developers use this skill to collect Indeed job listing data for job search, recruiting research, salary benchmarking, competitor hiring monitoring, or job-market analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use a browser session with logged-in Indeed cookies, which can expose account-bound access and sensitive session context. <br>
Mitigation: Use only an authorized browser session, avoid sharing credentials or unrelated tabs, and review collected output before reuse. <br>
Risk: The security evidence flags captcha-solving and stealth-session instructions that may conflict with anti-abuse controls or site terms. <br>
Mitigation: Do not use bypass or stealth techniques; confirm collection is permitted by Indeed, the user, and the user's organization before running the workflow. <br>
Risk: Saved memory or output files may contain sensitive job, company, salary, or browsing-session-derived data. <br>
Mitigation: Store only necessary results, redact sensitive fields when sharing, and delete temporary files after the task is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/skills/indeed-job-search) <br>
- [Indeed search URL pattern](https://www.indeed.com/jobs?q={keyword}&l={location}) <br>
- [Indeed job detail URL pattern](https://www.indeed.com/viewjob?jk={jobkey}) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash command templates and JSON result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results can include job listing metadata, application links, benefits, salary fields, and full HTML job descriptions when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
