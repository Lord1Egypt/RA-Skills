## Description:

Browser automation CLI with Nstbrowser integration for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nstbrowserio](https://clawhub.ai/user/nstbrowserio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate browser sessions through Nstbrowser profiles, including profile management, proxy configuration, batch profile operations, and page interaction for automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled shell templates and mutable npm execution paths may run code that has not been reviewed for the target environment.

Mitigation: Review or avoid the bundled shell templates before installation and prefer a pinned nstbrowser-ai-agent version.

Risk: API keys or proxy passwords may be exposed when passed through commands that are logged or stored in shell history.

Mitigation: Use local configuration or environment variables for secrets and avoid placing real credentials directly in logged commands.

Risk: Delete, clear, and batch operations can affect multiple browser profiles.

Mitigation: Verify target profile IDs and batch scope before running destructive or bulk profile commands.

Risk: Eval-based shell templates may be unsafe with untrusted profile or proxy values.

Mitigation: Do not run eval-based templates with untrusted values until they are rewritten to use safe shell argument arrays.

## Reference(s):

- [NST API Reference](references/nst-api-reference.md)
- [Profile Management Guide](references/profile-management.md)
- [Proxy Configuration Guide](references/proxy-configuration.md)
- [Batch Operations Guide](references/batch-operations.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [Nstbrowser Website](https://www.nstbrowser.io/)
- [nstbrowser-ai-agent npm Package](https://www.npmjs.com/package/nstbrowser-ai-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may require a local Nstbrowser service and NST_API_KEY configuration.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
