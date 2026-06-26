## Description: <br>
Agent Harness guides AI coding agents through disciplined planning, execution, verification, review, checkpointing, and multi-agent coordination workflows for software engineering tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christianye](https://clawhub.ai/user/christianye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to structure feature work, bug fixes, reviews, debugging, and larger multi-step coding tasks with explicit quality gates. It is especially suited to workflows that need task complexity grading, checkpointing, subagent coordination, and evidence-based verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports that the skill can guide nested Codex review in approval-bypass and broad filesystem modes by default. <br>
Mitigation: Review the skill before enabling it automatically, prefer no-yolo or AUTOREVIEW_YOLO=0, and choose fallback reviewer CLIs deliberately. <br>
Risk: External reviewer CLIs may receive sensitive local diffs when used in review workflows. <br>
Mitigation: Avoid sending sensitive local changes to external reviewer tools unless that sharing is intentional and approved. <br>


## Reference(s): <br>
- [Checkpoint Patterns for Agent Systems](references/checkpoint-patterns.md) <br>
- [MAST Failure Taxonomy for Multi-Agent Systems](references/mast-failure-taxonomy.md) <br>
- [ClawHub skill page](https://clawhub.ai/christianye/obsidian-harness) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists, tables, and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces process guidance and verification expectations rather than executable artifacts by itself.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
