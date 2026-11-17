## Description:

Automates verification that AI agents completed claimed tasks by checking expected files, system state, logs, and configurable quality gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kgapol](https://clawhub.ai/user/kgapol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to verify agent task outputs before downstream automation depends on them. It is suited for CI, scheduled monitoring, and manual checks where file content, freshness, logs, or process state must match an agent's completion claim.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found unsafe installation guidance in the documentation.

Mitigation: Inspect the scripts and use the local install command from SKILL.md instead of the README curl-to-bash installer.

Risk: Continuous watch mode can be under-scoped when scheduled directly.

Mitigation: Review the configured paths and avoid scheduling watch directly in cron until the monitoring behavior is validated for the target workspace.

Risk: Optional AI quality checks may send file excerpts to the configured Ollama environment.

Mitigation: Do not enable --ai-check on sensitive files unless that local AI environment and data handling are acceptable.

Risk: The security guidance says placeholder and AI verdict handling bugs prevent strict reliance as a completion gate.

Mitigation: Use results as a review aid until those issues are fixed, and keep a human or independent automated check for critical completions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kgapol/skills/proof-of-work)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text output and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns shell exit codes for pass, failure, configuration error, and missing file or directory outcomes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
