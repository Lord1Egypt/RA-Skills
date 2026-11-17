## Description:

Search authorized JishuDB knowledge bases to answer questions about stored documents, file inventories, and import status with cited evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers with authorized JishuDB access use this skill to find information in existing internal documents, check file listings, and report observed import status with source citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens may be exposed if sent to an untrusted endpoint or over plain HTTP.

Mitigation: Use only a trusted, authorized JishuDB endpoint and prefer HTTPS when JISHUDB_TOKEN is set.

Risk: Search passages alone cannot establish a complete document inventory or current import status.

Mitigation: Use the host's document inventory, read, or job-status tools for those requests; disclose when they are unavailable.

## Reference(s):

- [JishuDB search skill homepage (listed in skill metadata)](https://github.com/x-aijishu/jishudb-skills/tree/main/skills/jishudb-search)
- [ClawHub skill listing](https://clawhub.ai/bowen-aijishu/skills/jishudb-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown answers with source filenames, document listings, or observed status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers depend on the configured knowledge base and available host tools; the HTTP helper supports listing knowledge bases and searching passages only.]

## Skill Version(s):

0.1.5 (source: ClawHub release; skill source metadata: 0.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
