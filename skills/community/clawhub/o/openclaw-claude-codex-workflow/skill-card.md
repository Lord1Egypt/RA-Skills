## Description: <br>
Coordinates a multi-model OpenClaw workflow where Claude Code plans and reviews, Codex implements backend work, and Gemini handles frontend or UX tasks through staged artifacts and an orchestrator script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shennng](https://clawhub.ai/user/shennng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to plan, execute, verify, and review coding tasks that split responsibilities across Claude Code, Codex, and Gemini. It is most useful when a task needs OPSX or specification alignment, staged .claude artifacts, model-specific implementation work, and a final review handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow routes local coding tasks through Claude, Codex, and Gemini provider CLIs that may read project files and prompts. <br>
Mitigation: Install only when that routing is intended, use scoped API keys, and avoid placing secrets or sensitive customer data in prompts or .claude files. <br>
Risk: Generated commands, diffs, and .claude artifacts can affect a local working tree if accepted without review. <br>
Mitigation: Run dry-run first where available, keep provider work scoped to approved paths, and review generated diffs and artifacts before committing, pushing, or attaching them to tickets. <br>


## Reference(s): <br>
- [Model Routing Guide](references/model-routing.md) <br>
- [Workflow Checklist](references/workflow-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and workflow artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces plans, scope notes, execution logs, test matrices, review notes, and orchestrator command guidance for local agent workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
