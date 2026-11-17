## Description:

Calls the Pincaimao Career Planning Assistant V2 API to upload a resume and generate career advice for an initial career stage, career transition, or promotion path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pincaimao](https://clawhub.ai/user/pincaimao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to send a selected resume to Pincaimao and receive career-planning advice for one of three supported advice types. It is intended for authenticated users with a Pincaimao API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume content and the selected career advice request are sent to Pincaimao for processing and may be stored by Pincaimao.

Mitigation: Use the skill only when that data sharing is acceptable, avoid unnecessary sensitive details in resumes, and review Pincaimao's terms before use.

Risk: A wrong or overly broad resume file could be uploaded.

Mitigation: Confirm the exact resume file path before running the upload request.

Risk: The API key authorizes requests to the Pincaimao API.

Mitigation: Use a dedicated API key stored in PCM_CAREER_PLANNING_KEY and do not hardcode or share it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pincaimao/skills/pincaimao-career-planning-v2)
- [Pincaimao homepage](https://www.pincaimao.com)
- [Pincaimao API endpoint](https://api.pincaimao.com)
- [Pincaimao API key registration](https://www.pincaimao.com/agents/login?invite_code=uwqc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown or raw API answer text, with shell command examples for API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a summarized answer by default or the raw answer field when raw output is requested.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
