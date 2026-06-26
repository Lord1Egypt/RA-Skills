## Description: <br>
Create low-fidelity, text-based wireframes using the Markdown-UI Domain Specific Language (DSL). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MegaByteMark](https://clawhub.ai/user/MegaByteMark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and UI/UX practitioners use this skill to draft low-fidelity Markdown-UI DSL wireframes and, when explicitly requested, translate .ui.md specs into frontend code aligned to declared framework and theme metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt-controlled synchronization can overwrite linked code or wireframe specs without confirmation when autonomous or force-sync wording is used. <br>
Mitigation: Use the skill in version-controlled projects, avoid autonomous or force-sync wording on untrusted specs, and require a diff plus explicit confirmation before file updates. <br>
Risk: Generated UI specs or translated code may reflect ambiguous layout hints incorrectly. <br>
Mitigation: Review generated DSL and code against the intended design system and target framework before merging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MegaByteMark/markdown-ui-dsl) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Guidance, Configuration] <br>
**Output Format:** [Markdown-UI DSL, optional YAML frontmatter, or framework-specific code when translation is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or perform linked .ui.md and component file synchronization according to the user's confirmation posture.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
