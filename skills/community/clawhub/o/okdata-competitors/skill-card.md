## Description:

Fetches recent posts and engagement metrics for named competitor accounts across 11 social platforms and summarizes them in a table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and social media teams use this skill to compare recent competitor posts and engagement across supported platforms. It returns the requested posts and metrics in a table to help identify which content is gaining traction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each account lookup is a paid Okdata request and sends the account identifier or handle to the service.

Mitigation: State the endpoint rate and expected maximum cost before fetching, and send only accounts the user asked to check.

Risk: The security scan was partial because some local references could not be resolved; the benign verdict is not a safety guarantee.

Mitigation: Review the unresolved references and consider whether you are comfortable with the Okdata service before installing.

## Reference(s):

- [Okdata competitor monitoring skill guide](https://okdata.online/skills/competitors/?src=skill-okdata-competitors)
- [Okdata competitor monitoring skill guide (Chinese)](https://okdata.online/zh/skills/competitors/?src=skill-okdata-competitors)
- [Okdata agent connection guide](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Markdown, Analysis]

**Output Format:** [Markdown table with a concise summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per account by default; each account call is billed at the endpoint rate.]

## Skill Version(s):

0.2.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
