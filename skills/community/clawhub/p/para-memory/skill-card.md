## Description: <br>
Sets up and maintains a three-layer PARA memory system for OpenClaw agents using daily notes, structured project knowledge, and tacit knowledge extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisoftgg](https://clawhub.ai/user/aisoftgg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to give agents persistent workspace memory across sessions, organize durable knowledge, and consolidate session notes into project and preference files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to store and reread personal context across sessions, which can preserve sensitive or unwanted information if memory rules are not explicit. <br>
Mitigation: Review and edit the AGENTS.md template before installing, including clear rules for what may be saved, what must never be saved, and how memory can be reviewed or deleted. <br>
Risk: The template encourages automatic startup reads and consolidation workflows that may broaden local file access beyond the user's intended scope. <br>
Mitigation: Require explicit approval or narrow rules for calendar checks, broad file exploration, external lookups, and automatic consolidation unless those privileges are intentionally enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aisoftgg/para-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory-system setup instructions and reusable Markdown templates for AGENTS.md, daily notes, and tacit knowledge.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
