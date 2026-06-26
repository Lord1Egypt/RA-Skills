## Description: <br>
Design and land persona-driven agents by matching role, work identity, cognitive structure, personality grounding, identity-binding, and file skeleton into one coherent agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[child2d](https://clawhub.ai/user/child2d) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent designers use this skill to create, reshape, and land persona-driven agents with a clear work identity, stable cognitive structure, identity-binding sentence, file skeleton, and testing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or modified agent files may retain information the user does not want persisted. <br>
Mitigation: Review the target directory, generated files, and any persistent memory or session files before allowing writes or keeping the generated agent. <br>
Risk: Runtime registration changes can affect central agent configuration. <br>
Mitigation: Prefer user-applied OpenClaw configuration snippets and validate configuration syntax after insertion. <br>
Risk: A persona can drift into roleplay without stable work ownership or testing. <br>
Mitigation: Use the included failure-mode checks, identity-binding sentence, and first-round real-task validation before relying on the agent. <br>


## Reference(s): <br>
- [Agent Architect Methodology](references/methodology.md) <br>
- [Agent Architect Failure Modes](references/failure-modes.md) <br>
- [Character Texture for Persona-Driven Agents](references/character-texture.md) <br>
- [Agent Architect Output Template](references/output-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/child2d/ollivanders-agent-shop) <br>
- [Publisher Profile](https://clawhub.ai/user/child2d) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with file skeletons, draft agent content, command or configuration snippets, and testing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include user-applied runtime registration snippets instead of directly editing central configuration.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
