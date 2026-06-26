## Description: <br>
Monitor Indeed job postings for businesses hiring receptionists, customer service reps, or front desk staff in target areas and output an enriched lead list with company name, phone when available, location, and pain point summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JayJJimenez](https://clawhub.ai/user/JayJJimenez) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales and operations users can use this skill to find local businesses with active front-desk, receptionist, customer service, and related hiring signals. It produces a lead list for follow-up research and outreach planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The browser-based path drives a local Chrome/OpenClaw browser profile against Indeed. <br>
Mitigation: Use a dedicated browser profile where possible and confirm the browser relay is expected before running. <br>
Risk: The fallback path invokes an external Scrapling helper. <br>
Mitigation: Review and trust the external scraping helper before using the fallback workflow. <br>
Risk: Running with --save appends results to a hard-coded local lead-list path. <br>
Mitigation: Review or change the save path before running with --save. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JayJJimenez/indeed-monitor) <br>
- [Indeed job search](https://www.indeed.com/jobs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Console text with optional Markdown lead-list entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Lead fields may include company, job title, location, salary when listed, post date, job URL, and pain point or signal summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
