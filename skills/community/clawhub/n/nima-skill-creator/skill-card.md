## Description: <br>
Create, refactor, and improve Codex-compatible skills through gated requirement discovery, reusable resource planning, executable scaffolding scripts, and validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NimaChu](https://clawhub.ai/user/NimaChu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to design, scaffold, review, validate, and package Codex-compatible skills with structured discovery and reusable resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or modify local skill folders and package archives, which may include unintended content if the target directory is wrong. <br>
Mitigation: Confirm the target directory before generation and inspect packaged archives before enabling or sharing them. <br>
Risk: Generated or revised skills may contain incorrect workflow guidance or incomplete validation coverage. <br>
Mitigation: Review generated skills before enabling them and run the bundled validation script on the skill directory. <br>
Risk: The workflow may ask Chinese discovery prompts when requirements are underspecified. <br>
Mitigation: Tell the agent the preferred interaction language if Chinese prompts are not desired. <br>


## Reference(s): <br>
- [Nima Skill Creator on ClawHub](https://clawhub.ai/NimaChu/nima-skill-creator) <br>
- [Best Practices](references/best-practices.md) <br>
- [Skill Design Patterns](references/design-patterns.md) <br>
- [Chinese Discovery Prompts](references/interaction-guide.md) <br>
- [Output Patterns](references/output-patterns.md) <br>
- [Workflow Patterns](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, and generated skill files or configuration when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local skill folders, scripts, reference files, OpenAI agent interface YAML, and packaged skill archives when directed by the user.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
