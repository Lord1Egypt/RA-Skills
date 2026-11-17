## Description:

上市公司合规、任职资格、公司治理及信息披露咨询，使用 hegui MCP 核验法规数据库正文，并在法规支持披露义务时检索公告案例和公告格式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoeluli7459-dev](https://clawhub.ai/user/zoeluli7459-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users, compliance teams, and developers use this skill to answer Chinese listed-company compliance, governance, qualification, and disclosure questions from database-backed legal evidence. It helps an agent separate legal basis, applicability analysis, announcement format requirements, and verified comparable announcement files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides database-backed compliance research that could be mistaken for final legal advice.

Mitigation: Treat outputs as research assistance and route consequential compliance decisions through qualified legal review.

Risk: The skill depends on a configured hegui MCP token and service availability.

Mitigation: Install only when the user intends to use the hegui MCP service, protect the token in MCP configuration, and retry later when the service reports retrieval failures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoeluli7459-dev/skills/hegui)
- [hegui MCP endpoint](https://www.dxy-aiagent.com/mcp/hegui/mcp)
- [Installation guide](INSTALL.md)
- [Retrieval strategy](references/retrieval-strategy.md)
- [Citation standard](references/citation-standard.md)
- [Full-text verification](references/full-text-verification.md)
- [Routing contract](references/routing-contract.md)
- [Format retrieval](references/format-retrieval.md)
- [Announcement retrieval](references/announcement-retrieval.md)
- [Clarification policy](references/clarification-policy.md)
- [Answer contract](references/answer-contract.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with legal evidence summaries, complete clause quotations when verified, applicability analysis, and reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include announcement templates, comparable announcement files, missing-fact questions, and retrieval limitation notes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
