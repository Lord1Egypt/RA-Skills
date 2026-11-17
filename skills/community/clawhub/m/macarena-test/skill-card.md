## Description:

Security audit and threat model for OpenClaw gateway hosts. Use to verify OpenClaw configuration, exposure, skills/plugins, filesystem hygiene, and to produce an OK/VULNERABLE report with evidence and fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misirov](https://clawhub.ai/user/misirov)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to audit OpenClaw gateway hosts for configuration exposure, skill/plugin supply-chain issues, filesystem hygiene, and likely attack paths, then produce an evidence-backed OK/VULNERABLE report with recommended fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to run a local collection script immediately and without a consent prompt, while that script is not bundled in the artifact.

Mitigation: Review or provide the collection script, allowlist, and report references before installation, and require explicit user confirmation before collection on sensitive hosts.

Risk: Host audit evidence can include sensitive local configuration or credential-adjacent data.

Mitigation: Use the skill only where local collection is acceptable, redact secrets from evidence excerpts, and review generated findings before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/misirov/skills/macarena-test)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with evidence excerpts, findings, severity labels, and fix guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference a local verified-bundle.json evidence file and redacted host details when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
