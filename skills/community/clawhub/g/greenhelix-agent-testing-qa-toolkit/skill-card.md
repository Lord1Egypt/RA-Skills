## Description:

Provides a QA guide for multi-agent commerce systems covering integration, end-to-end, chaos, contract, performance, CI/CD, and canary testing strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and implement stronger QA for multi-agent commerce systems, including recorded integration tests, chaos tests, contract validation, performance benchmarks, CI/CD checks, and canary release controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-ready examples handle API keys and bearer headers.

Mitigation: Use sandbox-only, capped credentials; do not use production keys; validate and allowlist API hosts before adding bearer headers.

Risk: Recorded API cassettes may contain account, escrow, balance, transaction, or response-header data.

Mitigation: Redact cassette contents and response headers, review recordings before commit, and never commit unreviewed recordings.

Risk: Financial workflow examples may be adopted into CI without hardening.

Mitigation: Review and harden examples before use in CI, including redirect controls, host allowlists, and budget or credit limits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mirni/skills/greenhelix-agent-testing-qa-toolkit)
- [GreenHelix Sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API Documentation](https://api.greenhelix.net/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with Python, YAML, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide; real API examples may require GREENHELIX_API_KEY.]

## Skill Version(s):

1.3.1 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
