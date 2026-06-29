## Description: <br>
Evaluate Claude skill quality through auditing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit Claude skills for structure, content quality, token efficiency, activation reliability, and tool integration. It guides improvement planning, validation, and performance benchmarking for skill releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to run audit or benchmark commands from third-party skills without clear sandboxing or approval boundaries. <br>
Mitigation: Review commands before execution, treat audited third-party skills as untrusted, and prefer sandboxed or allowlisted execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/athola/skills/nm-abstract-skills-eval) <br>
- [Source homepage from release metadata](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides skill audits, improvement plans, verification steps, and performance checks; users should review commands before execution.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
