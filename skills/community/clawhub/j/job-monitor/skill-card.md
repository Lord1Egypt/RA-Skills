## Description:

Analyze JD text and return structured match summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghong5233](https://clawhub.ai/user/wanghong5233)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers, recruiters, and career-support agents use this skill to analyze job descriptions, summarize role requirements, estimate match fit, identify gaps, and inspect BOSS job search results with user confirmation before external actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User job descriptions or search terms are sent to a local backend at 127.0.0.1:8010.

Mitigation: Install and use the skill only when the local backend is trusted and users are comfortable sharing that job-search content with it.

Risk: The skill tells the agent to construct shell curl commands from user-provided job text.

Mitigation: Use safe JSON serialization or a structured HTTP client/tool instead of interpolating user input into shell commands.

Risk: The BOSS scanning behavior may interact with an external job platform.

Mitigation: Require user confirmation before external platform actions and clearly document the scanning capability before broad use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wanghong5233/skills/job-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Concise Markdown or text summary derived from JSON returned by a local HTTP backend.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For JD analysis, output may include parsed title, skill list, match score, and gap analysis. For BOSS scanning, output may include keyword, total count, pages scanned, top jobs, and an optional screenshot path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
