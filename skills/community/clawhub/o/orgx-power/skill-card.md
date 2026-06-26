## Description: <br>
Power-user OrgX skill for OpenClaw. Use when you explicitly need the full mutation surface for entity CRUD, run control, checkpoints, stream reassignment, or agent-config policy changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hopeatina](https://clawhub.ai/user/hopeatina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they explicitly need elevated OrgX administration for entity CRUD, run control, checkpoints, stream reassignment, and managed agent configuration policy changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Elevated OrgX operations can directly mutate entities, reassign streams, control runs, restore checkpoints, or update agent configuration. <br>
Mitigation: Install or invoke this skill only in trusted OrgX environments and require explicit approval before checkpoint restores, run cancellation or rollback, stream reassignment, org-wide changes, or agent-configuration updates. <br>
Risk: The elevated tool surface may be unavailable in domain-scoped managed OrgX runtimes. <br>
Mitigation: Fall back to the default orgx skill and request the necessary human decision or orchestration context when elevated tools are not exposed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for elevated OrgX tool usage; it does not itself expose credentials or execute tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
