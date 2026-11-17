## Description:

Provides lightweight retrieval, analysis, and summaries for public Lagou job listings and company pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to summarize public Lagou job listings, job details, and company pages for internal analysis and reminders. It is scoped to lightweight public-page analysis and excludes login automation, applications, API calls, and bulk scraping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may browse or parse public Lagou pages in ways that conflict with platform rules or create excessive traffic.

Mitigation: Keep use lightweight, avoid bulk scraping and API calls, apply frequency controls, and follow Lagou platform rules.

Risk: The agent may attempt logged-in actions or job applications outside the skill's intended scope.

Mitigation: Do not automate login, account actions, or applications; limit use to public job and company pages.

Risk: Dynamic pages and human verification can make extracted job information incomplete or stale.

Mitigation: Open pages manually when required, review extracted summaries before use, and include the collection time in outputs.

## Reference(s):

- [Lagou Homepage](https://www.lagou.com/)
- [Lagou Job Search](https://www.lagou.com/jobs/list_)
- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/lagou)
- [ClawHub Publisher Profile](https://clawhub.ai/user/codekungfu)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include job titles, salary ranges, city, experience, education, job type, posting time, responsibilities, requirements, skill tags, benefits, company profile details, source links, and collection time.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
