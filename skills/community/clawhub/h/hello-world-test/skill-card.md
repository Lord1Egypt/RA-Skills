## Description:

Hello World helps an agent respond to greeting and setup-test requests by calling a simple hello tool.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[kevin-li-okg](https://clawhub.ai/user/kevin-li-okg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and testers use this skill to confirm that the hello-world OpenClaw plugin is installed, enabled, and able to return a greeting. It routes hello, hi, and named greeting requests to the plugin's hello tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may respond to ordinary greetings by calling the hello tool.

Mitigation: Enable the plugin only in environments where greeting requests are expected to exercise the hello-world tool.

Risk: Strict reproducible builds may be affected by unpinned dependency ranges.

Mitigation: Pin dependency versions before using the package in production-like validation workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kevin-li-okg/skills/hello-world-test)
- [Artifact README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)
- [Plugin Manifest](artifact/openclaw.plugin.json)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text greeting returned by the plugin, with Markdown skill guidance for the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts an optional name parameter; defaults to world when no name is supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
