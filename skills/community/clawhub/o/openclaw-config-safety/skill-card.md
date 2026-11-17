## Description:

Validate, normalize, export, and import openclaw.json configs safely with automatic backups and schema checks before applying changes or upgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ether-btc](https://clawhub.ai/user/ether-btc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when editing OpenClaw configuration, changing model or gateway settings, running doctor or upgrade workflows, and exporting or importing config tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported mrconf:v1 tokens may expose sensitive values if the decoded payload contains plaintext secrets.

Mitigation: Before sharing a token, decode and review the payload and share only tokens whose credentials are references rather than plaintext secret values.

Risk: Validator, import, or normalize flows may unexpectedly change a live OpenClaw configuration.

Mitigation: Run checks on a candidate file when possible, keep a timestamped backup, and manually review changes before applying them to the live config.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ether-btc/skills/openclaw-config-safety)
- [Protocol: openclaw.json Config Edits](references/CONFIG-EDIT.md)
- [Export/Import Token Spec](references/EXPORT-TOKEN-SPEC.md)
- [Config Normalization Spec](references/NORMALIZATION-SPEC.md)
- [Onboarding Wizard Spec](references/ONBOARDING-SPEC.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce mrconf:v1 config tokens and backup or restore guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
