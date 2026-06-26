## Description: <br>
引导梳理模糊想法，分三步完成需求澄清、方案对比和设计细化，适用于新功能规划和技术选型。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caspermoo](https://clawhub.ai/user/caspermoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product builders, and teams use this skill to turn unclear feature or system ideas into confirmed requirements, compared solution options, and actionable design documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may read relevant project files and use that context while shaping a design. <br>
Mitigation: Install only where that project access is acceptable, and review the resulting requirements and design before acting on them. <br>
Risk: The skill may create design documents and suggest git commits, branches, or implementation work. <br>
Mitigation: Review generated documents and explicitly approve any commit, branch creation, or coding step before allowing it to proceed. <br>


## Reference(s): <br>
- [Question Templates](references/question-templates.md) <br>
- [Design Patterns](references/design-patterns.md) <br>
- [Output Templates](references/output-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Conversational guidance and Markdown design documents, with optional code or shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create design documents under docs/plans and may suggest git commits, branches, or implementation steps after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
