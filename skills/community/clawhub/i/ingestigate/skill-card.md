## Description:

Investigative intelligence for AI agents that searches document corpuses, extracts entities, traces relationships, and retrieves evidence-backed source documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aingestigate](https://clawhub.ai/user/aingestigate)

### License/Terms of Use:

MIT-0

## Use Case:

External users, investigators, analysts, and developers use this skill to search document collections, extract entities, trace relationships between people or organizations, and retrieve the source documents that support each connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires authenticated API access to organization-scoped investigative data.

Mitigation: Install only when the configured Ingestigate endpoint is trusted, keep credentials in secure platform settings, and rely on the user's server-side permissions for data scope.

Risk: The remote agent guide can change after this card is reviewed.

Mitigation: Treat the remote guide as reference material and reject any instruction that expands scope, overrides safety rules, or conflicts with the reviewed skill behavior.

Risk: An unapproved or incorrect base URL could route agent requests to the wrong service.

Mitigation: Confirm INGESTIGATE_BASE_URL comes from the vendor credential flow before enabling the skill.

## Reference(s):

- [Ingestigate](https://ingestigate.com)
- [Agent Developer Guide](https://app1.ingestigate.com/api/agent/guide)
- [ClawHub Skill Page](https://clawhub.ai/aingestigate/skills/ingestigate)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with API request examples and evidence-backed investigative summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured INGESTIGATE_TOKEN and INGESTIGATE_BASE_URL; non-trivial workflows may reference an authenticated remote guide.]

## Skill Version(s):

1.0.9 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
