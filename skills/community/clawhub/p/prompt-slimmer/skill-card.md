## Description: <br>
Prompt Slimmer audits and slims down OpenClaw workspace files to reduce system prompt token usage by identifying redundancy, low-frequency content, cross-file duplication, and ghost Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit OpenClaw workspace Markdown files, reduce always-on prompt overhead, and create an approval-gated slimming plan with before-and-after size estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace Markdown edits could accidentally remove or archive critical identity, safety, or credentials-handling rules. <br>
Mitigation: Ask for a plan and diff before approving edits, keep a backup, and verify that critical rules remain in active workspace files. <br>
Risk: Archived content may become harder for the agent to retrieve when needed. <br>
Mitigation: Verify archived content is searchable with memory_search and leave concise pointers to archive paths where appropriate. <br>


## Reference(s): <br>
- [Prompt Slimmer on ClawHub](https://clawhub.ai/xiaoyaner0201/prompt-slimmer) <br>
- [xiaoyaner0201 publisher profile](https://clawhub.ai/user/xiaoyaner0201) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and audit checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an actionable slim-down plan, before-and-after metrics, archive guidance, and verification steps; workspace edits are intended to be user-approved.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
