## Description: <br>
Demonstration skill showcasing complete AgentSkills core architecture, including SKILL.md structure, main entry logic, tool integration patterns, error handling, and production-ready patterns for building new skills. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[wyblhl](https://clawhub.ai/user/wyblhl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this template to build, audit, teach, or extend AgentSkills with documented structure, tool integration patterns, error handling, validation, and publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example shell and publishing workflows may be copied into real projects without enough review. <br>
Mitigation: Review commands before execution, add dry-run and confirmation steps, and prefer argument-vector execution or safer APIs over shell string interpolation. <br>
Risk: State, report, cache, or memory files can expose sensitive details if adapted without controls. <br>
Mitigation: Avoid logging or storing secrets, restrict watch/API/report scopes, and scan generated files before sharing or publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wyblhl/l76-core-arch) <br>
- [AgentSkills Spec](https://github.com/OpenClaw/spec) <br>
- [ClawHub Documentation](https://clawhub.com/docs) <br>
- [Basic usage examples](references/examples.md) <br>
- [Advanced examples](references/examples-advanced.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Performance tuning](references/performance-tuning.md) <br>
- [Extension points](references/extension-points.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and optional Node.js execution output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js for the optional index.js runtime and validation workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
