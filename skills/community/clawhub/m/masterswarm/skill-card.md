## Description:

Analyze documents with 15 parallel AI engines via the MasterSwarm cloud API and return professional intelligence reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contrario](https://clawhub.ai/user/contrario)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to send document text or questions to MasterSwarm's hosted API for multi-engine analysis across business, research, market, legal, financial, food, and forecasting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document text and prompts are sent to the third-party MasterSwarm/NeuroDoc cloud service.

Mitigation: Use only with data approved for that service, and avoid secrets, credentials, confidential business files, and regulated medical, legal, or financial data unless an appropriate review has approved the workflow.

Risk: The provided shell substitution example can execute local commands if used with untrusted input.

Mitigation: Serialize request bodies with a safe JSON builder and explicitly review or reject hostile user-supplied text before invoking shell commands.

## Reference(s):

- [MasterSwarm Homepage](https://masterswarm.net)
- [MasterSwarm API Endpoint](https://api.neurodoc.app/aetherlang/execute)
- [AetherLang Documentation](https://aetherlang.net)
- [ClawHub Skill Page](https://clawhub.ai/contrario/skills/masterswarm)
- [Publisher Profile](https://clawhub.ai/user/contrario)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON API responses, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MASTERSWARM_API_KEY; API calls may take 120-180 seconds and consume paid credits.]

## Skill Version(s):

1.1.2 (source: server release metadata, SKILL.md frontmatter, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
