## Description:

Discover, compare, inspect, preview, call, and integrate curated public APIs with Pontx Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Pontx Hub to discover curated public APIs, inspect current endpoint and schema metadata, preview requests safely, install provider-specific product Skills with approval, and generate code with published Pontx SDK packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dynamic installs or product Skill selection could add untrusted or unintended package behavior.

Mitigation: Install only after checking the package or skill identity, publisher, and version and obtaining user approval.

Risk: Mutation endpoints can create, update, or delete provider data if called with incorrect method, host, path, parameters, or body.

Mitigation: Preview the exact request first, present the resolved side effect, and require explicit confirmation before running the unchanged request with execution enabled.

Risk: Credentials could be exposed if copied into commands, source files, examples, logs, or chat messages.

Mitigation: Use only the environment variables declared by the catalog and keep secret values out of command arguments and generated content.

## Reference(s):

- [Authentication and mutation safety](references/auth-and-safety.md)
- [Pontx Hub on ClawHub](https://clawhub.ai/pontjs/skills/pontx-hub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON-oriented CLI guidance, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May preview API requests, report machine-readable errors, and generate SDK installation or integration instructions without exposing credentials.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
