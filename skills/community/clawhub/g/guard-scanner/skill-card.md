## Description:

Guard Scanner helps agents and developers scan OpenClaw skills, MCP servers, and AI-agent workflows for prompt injection, identity hijacking, memory poisoning, A2A contagion, secret leaks, supply-chain abuse, and risky tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koatora20](https://clawhub.ai/user/koatora20)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use Guard Scanner to review skills before installation, scan workspaces in CI, audit public assets for credential exposure, run watch-mode checks during development, expose scanner tools over MCP, and enforce OpenClaw before_tool_call policy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted ClawHub audit query may trigger local shell command execution in one audit path.

Mitigation: Review or fix the audit command-injection issue before using Guard Scanner with untrusted audit input.

Risk: The artifact includes intentionally malicious fixture files used as scanner test samples.

Mitigation: Treat fixture files as hazardous test data and do not execute them directly.

Risk: The source artifact did not include the compiled plugin and launcher files referenced by package metadata.

Mitigation: Verify a built package or tarball before installing or deploying the runtime plugin.

## Reference(s):

- [ClawHub Guard Scanner listing](https://clawhub.ai/koatora20/skills/guard-scanner)
- [Guard Scanner README](artifact/README.md)
- [Capability specification](artifact/docs/spec/capabilities.json)
- [Finding schema](artifact/docs/spec/finding.schema.json)
- [Threat taxonomy](artifact/docs/THREAT_TAXONOMY.md)
- [Security policy](artifact/SECURITY.md)
- [npm package](https://www.npmjs.com/package/@guava-parity/guard-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON/SARIF/HTML report references, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce CLI, MCP, CI, audit, and runtime-policy outputs; reports may include finding metadata such as layer, OWASP ASI mapping, protocol surface, severity, rationale, and remediation.]

## Skill Version(s):

16.0.2 (source: server release metadata and package.json; changelog top entry is 16.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
