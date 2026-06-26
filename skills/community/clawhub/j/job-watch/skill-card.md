## Description: <br>
Automated job search with 7-day filtering, scoring, and weekly report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elfilalihamza](https://clawhub.ai/user/elfilalihamza) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers use this skill to search public job boards, filter postings from the last 7 days, score matches against a local profile, and produce a structured weekly report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Profile, scoring, and platform configuration files may contain sensitive personal job-search details if users add them. <br>
Mitigation: Review those files before running the skill and avoid adding secrets, passwords, or unnecessarily sensitive personal information. <br>
Risk: The skill queries public job boards and may produce stale, incorrect, or broken listing links. <br>
Mitigation: Verify job listings on the original platform before applying and prefer directly extracted listing URLs. <br>


## Reference(s): <br>
- [Job Watch on ClawHub](https://clawhub.ai/elfilalihamza/job-watch) <br>
- [Initial Setup](references/initial-setup.md) <br>
- [URL Extraction Guide](references/url-extraction-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with summary, scored job-match tables, links, and next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report is saved locally in the OpenClaw workspace when the host agent supports local file writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
