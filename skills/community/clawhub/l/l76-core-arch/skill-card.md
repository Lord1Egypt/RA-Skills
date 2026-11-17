## Description:

Demonstration skill showcasing complete AgentSkills core architecture, including SKILL.md structure, main entry logic, tool integration patterns, error handling, and production-ready patterns as a template for building new skills.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[wyblhl](https://clawhub.ai/user/wyblhl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a reference template for creating, auditing, teaching, debugging, extending, and validating AgentSkills architecture and publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advanced examples include shell-string execution, file changes, Git mutations, and external API calls that may be unsafe if copied directly into a real skill.

Mitigation: Use the package only as a reference after manual review; replace shell-string execution with safer APIs and require explicit confirmation before file or Git mutations.

Risk: State, cache, report, and memory outputs may persist sensitive data.

Mitigation: Redact logs and reports, review persisted artifacts before sharing, and treat generated state or memory files as sensitive.

Risk: Template guidance may be incomplete or misleading for a production skill without additional review.

Mitigation: Review and scan any derived skill before deployment, and adapt the examples to the target environment and security policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wyblhl/skills/l76-core-arch)
- [AgentSkills Spec](https://github.com/OpenClaw/spec)
- [ClawHub Documentation](https://clawhub.com/docs)
- [L76 Core Architecture - Usage Examples](references/examples.md)
- [L76 Core Architecture - Advanced Examples](references/examples-advanced.md)
- [L76 Core Architecture - Troubleshooting Guide](references/troubleshooting.md)
- [L76 Core Architecture - Performance Tuning Guide](references/performance-tuning.md)
- [L76 Core Architecture - Extension Points Guide](references/extension-points.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code blocks and optional command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js for the bundled executable example and validation workflow.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
