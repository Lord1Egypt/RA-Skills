## Description:

Secure, per-user-isolated email reasoning and analysis via the iGPT Context Engine API for summaries, task and decision extraction, sentiment detection, and structured answers over connected email context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sammy-spk](https://clawhub.ai/user/sammy-spk)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, and developers use this skill to ask questions about connected email, summarize threads, extract action items and decisions, assess sentiment or risk, and produce text or structured JSON answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected mailbox data and user questions are sent to iGPT for analysis.

Mitigation: Install only where iGPT is trusted and approved to process the connected mailbox data.

Risk: API keys and OAuth consent can grant access to sensitive email context.

Mitigation: Use a least-privileged or approved email account where possible, review OAuth consent before authorizing, keep IGPT_API_KEY protected, and prefer a pinned reviewed igptai version in managed environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sammy-spk/skills/igpt-email-ask)
- [iGPT Playground](https://igpt.ai/hub/playground/)
- [iGPT Documentation](https://docs.igpt.ai)
- [iGPT Ask API Reference](https://docs.igpt.ai/docs/api-reference/ask)
- [iGPT Security Model](https://docs.igpt.ai/docs/security/model)
- [igptai Python SDK](https://pypi.org/project/igptai/)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Markdown guidance with Python examples; runtime answers may be text, JSON, or schema-validated JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports streaming SSE responses; requires IGPT_API_KEY and a connected email datasource.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
