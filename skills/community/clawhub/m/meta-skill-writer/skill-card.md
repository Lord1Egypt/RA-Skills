## Description: <br>
Guides an agent, in Chinese, through designing and writing an OpenClaw skill from a user's request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[54lynnn](https://clawhub.ai/user/54lynnn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to turn a request for a new skill into a scoped skill design, SKILL.md content, optional references, examples, evals, and deterministic helper scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may cause the skill to activate for requests that only loosely mention skill creation. <br>
Mitigation: Review and narrow generated skill descriptions so they match the intended user request and avoid accidental activation. <br>
Risk: The skill can help create scripts or install commands that may affect a user's environment. <br>
Mitigation: Review generated scripts and installation steps before use, and run deterministic checks such as openclaw skills check where applicable. <br>


## Reference(s): <br>
- [Skill template reference](artifact/references/skill-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/54lynnn/meta-skill-writer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance and generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce SKILL.md content, reference files, examples, eval definitions, and deterministic helper scripts depending on the requested skill.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
