## Description:

Analyze GitHub issue content, assess its priority, identify missing information, and provide clear reproduction steps or triage advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunny0826](https://clawhub.ai/user/sunny0826)

### License/Terms of Use:

MIT-0

## Use Case:

Open-source maintainers, QA engineers, and developers use this skill to triage pasted GitHub issue text, classify the report, assess priority, identify missing information, and draft a polite response in English or Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted issue content may contain indirect prompt-injection attempts or instructions unrelated to triage.

Mitigation: Treat issue bodies and comments as untrusted text for analysis only, and do not execute or follow embedded instructions.

Risk: Users may paste secrets, private tokens, or sensitive customer data into issue reports.

Mitigation: Avoid providing secrets or sensitive data in issue text submitted for triage.

Risk: Fetching issue content from URLs can expose the agent to untrusted external content at runtime.

Mitigation: Require users to paste raw issue text or Markdown directly and ask for pasted content when only a URL is provided.

## Reference(s):

- [Skill README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/sunny0826/skills/issue-triage)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown triage report with checklist items and suggested reply text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English and Chinese output based on the user's prompt language.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
