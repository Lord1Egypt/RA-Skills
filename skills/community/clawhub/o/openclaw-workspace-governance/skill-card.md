## Description: <br>
OpenClaw Workspace Governance is a governance playbook for complex OpenClaw workspaces that helps agents reduce drift, clarify current truth, route retrieval, manage live document freshness, and close maintenance phases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heishiqing](https://clawhub.ai/user/heishiqing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace maintainers use this skill to govern complex OpenClaw workspaces with multiple agents, layered memory, semantic retrieval, live document boundaries, and maintenance checks. It is intended for advanced workspaces where current-state drift, document drift, retrieval drift, or unclear approval paths have become operational risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The governance playbook may lead an agent to reorganize document authority, live-document boundaries, retrieval priority, or process rules across a workspace. <br>
Mitigation: Back up or snapshot the workspace before applying changes, review proposed governance edits before execution, and require human authorization for core rule or policy changes. <br>
Risk: Helper scripts can inspect freshness, document status, and semantic runtime behavior across paths or runtimes selected by the user. <br>
Mitigation: Run the scripts only against intended workspace roots, configuration paths, cache paths, and semantic runtimes; review their reported findings before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heishiqing/openclaw-workspace-governance) <br>
- [Multi-agent governance](references/multi-agent-governance.md) <br>
- [Source-of-truth layering](references/source-of-truth-layering.md) <br>
- [Query-class routing](references/query-class-routing.md) <br>
- [Live vs historical docs](references/live-vs-historical-docs.md) <br>
- [Freshness discipline](references/freshness-discipline.md) <br>
- [Semantic search diagnostics](references/semantic-search-diagnostics.md) <br>
- [Completion criteria](references/completion-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with optional JSON examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes helper scripts for freshness checks, document status scans, and semantic runtime diagnostics; scripts report results and do not automatically rewrite files.] <br>

## Skill Version(s): <br>
1.0.9 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
