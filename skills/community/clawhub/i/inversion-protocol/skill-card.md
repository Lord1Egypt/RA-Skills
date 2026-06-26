## Description: <br>
Meta-cognitive reasoning skill that improves agent decision-making by applying inversion, premortem reasoning, and via negativa checks before consequential actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, researchers, and other agent users use this skill to add a short reasoning checkpoint before code changes, commands, debugging, architecture decisions, and high-accuracy answers where preventable mistakes matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security evidence marks the release suspicious and notes a maintainer workflow risk involving a nested reviewer with broad unsandboxed access by default. <br>
Mitigation: Install only if that workflow risk is acceptable; prefer safer review settings such as disabling default full-access behavior unless explicitly intended. <br>
Risk: The skill can influence consequential agent decisions but is not itself a safety filter or policy enforcement layer. <br>
Mitigation: Use it as an additional reasoning checkpoint and keep normal review, scanning, sandboxing, and approval controls in place for sensitive actions. <br>


## Reference(s): <br>
- [Mental Models Behind the Inversion Protocol](references/mental-models.md) <br>
- [Coding Scenarios](examples/coding-scenarios.md) <br>
- [General Agent Scenarios](examples/general-scenarios.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jcools1977/inversion-protocol) <br>
- [Project Homepage](https://github.com/jcools1977/Opensaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Markdown, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with structured reasoning checkpoints and optional inline code or shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No runtime dependencies, APIs, binaries, environment variables, or external services are described by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
