## Description:

Connects an agent to Jotform to retrieve forms, questions, submissions, and account information, and to create submissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People with a connected Jotform account can retrieve account, form, question, and submission data, or create a submission for a form.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute an unpinned remote installer without installation-specific approval.

Mitigation: Review and install a fixed CLI release yourself before use, and review or disable its automatic agent-skill synchronization. Consider whether Jotform submission data may pass through OOMOL, and retain the required confirmation before writes. Exact installer effects remain unverified; no malicious behavior was established.

## Reference(s):

- [Jotform API documentation](https://api.jotform.com/docs/)
- [Jotform](https://www.jotform.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Jotform skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-jotform)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Jotform API response data, typically JSON, with optional natural-language summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the connected Jotform account and the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
