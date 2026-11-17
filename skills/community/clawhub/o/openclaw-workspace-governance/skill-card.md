## Description:

OpenClaw Workspace Governance helps agents manage complex OpenClaw workspaces by reducing drift, clarifying current truth, bounding live documents, and routing semantic retrieval more carefully.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heishiqing](https://clawhub.ai/user/heishiqing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to classify governance drift, separate source-of-truth layers, keep a minimal working set fresh, and evaluate semantic search reliability before making workspace changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Governance or routing changes could alter workspace source-of-truth behavior if applied without review.

Mitigation: Treat outputs as proposals, back up the workspace, and require human review before applying process or routing changes.

Risk: The freshness checker reads paths from its working-set config and could inspect files outside the intended workspace if the config is untrusted.

Mitigation: Run local diagnostic scripts only with trusted configs scoped to the intended workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/heishiqing/skills/openclaw-workspace-governance)
- [README](README.md)
- [Completion Criteria](references/completion-criteria.md)
- [Freshness Discipline](references/freshness-discipline.md)
- [Live vs Historical Docs](references/live-vs-historical-docs.md)
- [Multi-Agent Governance](references/multi-agent-governance.md)
- [Query-Class Routing](references/query-class-routing.md)
- [Semantic Search Diagnostics](references/semantic-search-diagnostics.md)
- [Source of Truth Layering](references/source-of-truth-layering.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance, JSON examples, and local diagnostic command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose workspace file, routing, or documentation changes; bundled diagnostic scripts do not automatically rewrite files.]

## Skill Version(s):

1.0.9 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
