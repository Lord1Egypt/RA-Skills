## Description: <br>
Grill With Docs guides an agent through a design-grilling session that resolves domain language and architectural decisions, then produces CONTEXT.md glossary content and ADR files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genortg](https://clawhub.ai/user/genortg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to pressure-test a design, align on precise domain terminology, and capture durable documentation as a glossary and architecture decision records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or edit glossary and ADR files in the wrong project context or path. <br>
Mitigation: Confirm the target CONTEXT.md and docs/adr paths before writing, especially when a repository has CONTEXT-MAP.md or multiple bounded contexts. <br>
Risk: Resolved terms or ADRs may misrepresent the codebase or the team's intended design. <br>
Mitigation: Preview diffs and have the relevant project owner review proposed documentation changes before accepting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/genortg/grill-docs) <br>
- [Publisher profile](https://clawhub.ai/user/genortg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown files and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or edit CONTEXT.md and docs/adr files when the session resolves terms or decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
