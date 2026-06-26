## Description: <br>
Performs structured audits of OpenClaw skills for format, content quality, functional correctness, and adherence to best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YKaiXu](https://clawhub.ai/user/YKaiXu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill maintainers use this skill to review OpenClaw skills before publishing or deployment, checking package format, documentation quality, functional behavior, and OpenClaw specification alignment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The review workflow can lead an agent to run scripts from skills being reviewed. <br>
Mitigation: Inspect scripts first and run them only with explicit approval in a sandbox or disposable workspace. <br>
Risk: The skill includes hardcoded OpenClaw paths that may not match the user's environment. <br>
Mitigation: Verify and replace local OpenClaw paths before using the commands. <br>


## Reference(s): <br>
- [Skill Design Best Practices](references/best-practices.md) <br>
- [OpenClaw Specifications](references/openclaw-specs.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with checklists and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to inspect skill files, compare outputs against OpenClaw specifications, and report review findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
