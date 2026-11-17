## Description:

Novel Studio guides agents through a staged Chinese web-fiction production workflow for discovery, market/topic analysis, story planning, character design, drafting, polishing, proofreading, final review, and optional Feishu Wiki sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pallyoung](https://clawhub.ai/user/pallyoung)

### License/Terms of Use:

MIT-0

## Use Case:

External authors, editors, and agent operators use this skill to turn a Chinese web-novel concept into a staged, reviewable project with planning documents, character materials, chapter manuscripts, revisions, QA reports, and optional delivery sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts include under-scoped file deletion and write behavior when handling stage, branch, artifact, or file-path values.

Mitigation: Run only in trusted project workspaces, review path-like inputs before execution, and keep backups until path containment and deletion safeguards are confirmed.

Risk: Optional Feishu sync can upload manuscript content to a hard-coded, undisclosed wiki space.

Mitigation: Use Feishu sync only after verifying and changing the destination space and confirming the manuscript content is approved for upload.

Risk: The authoritative security verdict is suspicious even though the workflow itself is coherent.

Mitigation: Review before installing, treat helper scripts as project-local tools, and avoid untrusted inputs during automated workflow execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pallyoung/skills/novel-studio)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [Workflow](references/workflow.md)
- [Intake](references/intake.md)
- [Market Research](references/market-research.md)
- [Outlining](references/outlining.md)
- [Character Bible](references/character-bible.md)
- [Drafting](references/drafting.md)
- [Polishing](references/polishing.md)
- [Proofreading](references/proofreading.md)
- [Final Review](references/final-review.md)
- [State Management](references/state-management.md)
- [Subagent Execution](references/subagent-execution.md)
- [Narrative Intelligence](references/narrative-intelligence.md)
- [Feishu Sync](references/feishu-sync.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown project files, manuscript text, JSON status data, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file-backed stage artifacts, chapter manuscripts, ledgers, revision notes, progress reports, and optional Feishu sync output.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
