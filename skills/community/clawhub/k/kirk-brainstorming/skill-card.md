## Description: <br>
Helps agents explore user intent, requirements, alternatives, and design details before implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to turn early feature or behavior-change ideas into validated designs before implementation. It guides the agent to inspect project context, ask one focused question at a time, compare approaches, and document the selected design. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can lead the agent to inspect repository context, create a design document, and commit it. <br>
Mitigation: Before use, tell the agent whether repository inspection, docs/plans file writes, and git commits are allowed; keep the design in chat if repository changes are not desired. <br>
Risk: A design produced from incomplete answers may encode incorrect assumptions or misleading implementation guidance. <br>
Mitigation: Review each design section, correct assumptions during incremental validation, and confirm requirements before using the design as an implementation plan. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Conversational text with optional Markdown design documentation and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a docs/plans design document after user validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
