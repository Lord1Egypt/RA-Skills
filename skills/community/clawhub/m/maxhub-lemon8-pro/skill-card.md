## Description:

Queries Lemon8 posts, comments, user profiles, search, and discovery content through the MaxHub API to support content and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Content researchers, marketers, and creators use the skill to query public Lemon8 content and analyze posts, comments, creator profiles, search results, and topic trends. It returns data for user-directed, read-only analysis through the MaxHub API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Share links and query details are sent to the third-party MaxHub API.

Mitigation: Before submitting a link, check that it contains no private information and that sending it to the third-party service is acceptable.

Risk: The skill writes local compliance and audit records.

Mitigation: Review the local records and protect or remove them according to your data-handling policies.

Risk: The documented installer is unpinned, and the security analysis was partial because some references were missing or ambiguous.

Mitigation: Review the source and release before installation, and inspect the incomplete references before relying on the skill.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-lemon8)
- [ClawHub release](https://clawhub.ai/xiewxx/skills/maxhub-lemon8-pro)
- [MaxHub API service](https://www.aconfig.cn)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Text]

**Output Format:** [JSON query results summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only queries; results may include user-generated content and personal data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
