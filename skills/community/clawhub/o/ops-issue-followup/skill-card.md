## Description:

Guides Codex to clarify, investigate, verify, and summarize project/system maintenance or operations issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiluoduyu](https://clawhub.ai/user/xiluoduyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and maintainers use this skill to follow up operational issues with a structured investigation: confirm facts, identify ownership, gather local context, align on analysis, verify evidence, and summarize findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to inspect project-local documentation, source files, configuration, logs, or runtime evidence during issue follow-up.

Mitigation: Use it only in workspaces where that level of operational investigation is appropriate, and review proposed commands or edits before execution.

Risk: Follow-up summaries can include incorrect conclusions if assumptions, historical notes, or wiki context are treated as proof.

Mitigation: Keep confirmed facts separate from assumptions and verify findings against current code, logs, configuration, tests, or runtime evidence.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown prose with optional inline shell commands or code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should distinguish confirmed evidence, assumptions, likely causes, remaining unknowns, and next steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
