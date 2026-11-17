## Description:

Premium PH outreach agent - automates community discovery, enrichment, and LinkedIn engagement locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techievena](https://clawhub.ai/user/techievena)

### License/Terms of Use:

MIT-0

## Use Case:

External founders, marketers, and launch teams use this skill to run local Product Hunt outreach workflows: discovering community prospects, enriching profiles, generating LinkedIn messages, and monitoring campaign status from a local dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables recurring LinkedIn-facing outreach automation with broad triggers and unclear safeguards.

Mitigation: Confirm how scheduled runs are enabled or removed, set conservative outreach limits, and require human approval before connection requests or direct messages are sent.

Risk: The skill stores a local LinkedIn browser session for authentication.

Mitigation: Use a dedicated browser profile where possible, restrict local filesystem access, and clear the saved session when the campaign is complete.

Risk: The installed package is expected to execute server-side local files that are not present in the submitted artifact.

Mitigation: Review the installed server files before first execution, especially network calls, data handling, scheduler behavior, and dashboard endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/techievena/skills/ph-wingman)
- [ProductHunt Wingman Homepage](https://producthunt.eonik.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with local setup commands, status summaries, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger local service checks, scheduled outreach workflows, browser-based LinkedIn authentication, and local dashboard interactions.]

## Skill Version(s):

1.6.1 (source: SKILL.md frontmatter, skill.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
