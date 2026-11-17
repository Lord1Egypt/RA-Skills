## Description:

Immigration, tax, and business compliance alerts for STEM OPT, H-1B, I-140, CPT status, upcoming deadlines, risk findings, and tax filing obligations from Guardian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lee-chenyu](https://clawhub.ai/user/lee-chenyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to check Guardian-backed immigration, tax, and business compliance status, deadlines, risk findings, documents, and specific compliance questions from their chat agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a bearer token and potentially sensitive immigration, tax, business compliance, deadline, risk, document, and question data to Guardian's remote service.

Mitigation: Configure GUARDIAN_TOKEN only for the intended Guardian account and assume data requested through the skill may be sent to the Guardian API.

Risk: Setting GUARDIAN_API_URL changes the remote endpoint that receives the bearer token and compliance requests.

Mitigation: Avoid overriding GUARDIAN_API_URL unless the endpoint is trusted.

Risk: Guardian output may affect decisions in legal, immigration, tax, or business compliance contexts.

Mitigation: Treat Guardian as compliance risk detection rather than legal or tax advice, and consult an immigration attorney or qualified CPA for critical issues.

## Reference(s):

- [Guardian Compliance on ClawHub](https://clawhub.ai/lee-chenyu/skills/guardian-compliance)
- [Guardian Compliance Homepage](https://guardian-compliance.fly.dev)
- [Publisher Profile](https://clawhub.ai/user/lee-chenyu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text returned from Guardian API-backed shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and GUARDIAN_TOKEN; sends compliance questions and dashboard requests to the configured Guardian API endpoint.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
