## Description:

围绕疾病，药品，症状，诊断，并发症，饮食及其关系的知识图谱。仅限初步研究，具体应用需根据实际情况调整。

This skill is for research and development only.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect a hosted medical knowledge graph schema and run read-only Cypher queries for preliminary research about diseases, drugs, symptoms, diagnoses, complications, diet, and their relationships. Outputs should be treated as research support, not clinical guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries are sent to the XiaoBenYang MCP API.

Mitigation: Avoid sending sensitive health or personal data unless the user has reviewed and accepted the external service terms and data-handling expectations.

Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file.

Mitigation: Use a disposable or scoped API key, restrict local file access, and ensure .env is not committed or shared.

Risk: The artifact includes inconsistent references to an unrelated gaokao/admissions skill.

Mitigation: Confirm the package contents and intended medical knowledge graph behavior with the publisher before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/medical-knowledge-graph)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Guidance]

**Output Format:** [Markdown summaries of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key before tool calls can be made.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
