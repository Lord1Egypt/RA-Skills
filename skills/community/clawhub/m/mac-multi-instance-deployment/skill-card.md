## Description: <br>
Public-safe Mac multi-instance deployment skill for generic OpenClaw-style workspace layout, boundary notes, sample config, and pack validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoma970](https://clawhub.ai/user/guoma970) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to organize generic Mac multi-instance OpenClaw-style workspaces, keep private runtime state out of public releases, and validate public-safe packs before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose repository commands, workspace changes, or public-pack generation steps that affect local project state. <br>
Mitigation: Review the proposed plan and commands before execution, especially validation, packaging, or configuration changes. <br>
Risk: Private paths, runtime state, secrets, or account data could be accidentally included when adapting a multi-instance layout. <br>
Mitigation: Use placeholder paths, keep private runtime state local, and run public-pack validation before release. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guoma970/mac-multi-instance-deployment) <br>
- [Publisher Profile](https://clawhub.ai/user/guoma970) <br>
- [README](README.md) <br>
- [Publishing Summary](PUBLISHING.md) <br>
- [Customization Guide](CUSTOMIZATION.md) <br>
- [Quickstart Example](examples/quickstart.md) <br>
- [Setup Example](examples/setup-example.md) <br>
- [Validation Example](examples/validation-example.md) <br>
- [Release Notes v1.0.4](releases/1.0.4.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses generic placeholder paths and public-safe boundary guidance.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter, release evidence, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
