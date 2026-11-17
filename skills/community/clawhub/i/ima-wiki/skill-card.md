## Description:

Organizes source material into a structured Tencent IMA wiki with topic guides, folder organization, tagging, and knowledge-base health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cookfish1979](https://clawhub.ai/user/cookfish1979)

### License/Terms of Use:

MIT-0

## Use Case:

People maintaining Tencent IMA knowledge bases use the skill to ingest materials, organize folders and tags, compile or update topic guides, and check content health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use IMA API credentials to read and change knowledge-base content.

Mitigation: Enable it only for knowledge bases you intend the agent to manage; review proposed note writes, file moves, tag changes, and cascade updates before approval.

Risk: Knowledge-base content may be sent to Tencent IMA and associated COS endpoints.

Mitigation: Do not use it with content that you do not want sent to those services.

## Reference(s):

- [Tencent IMA API documentation](https://ima.qq.com/agent-interface)
- [Ingest workflow](references/ingest.md)
- [Wiki guide schema](references/schema.md)
- [Knowledge-base health checks](references/lint.md)
- [Safety guidance](references/security.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown topic guides, audit reports, and actionable instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update notes, tags, and folders in the user's IMA knowledge base.]

## Skill Version(s):

1.2.0 (source: server-resolved ClawHub release; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
