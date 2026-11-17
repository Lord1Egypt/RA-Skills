## Description:

Picoclaw-only local posture-review skill focused on read-only findings and safe operator remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

AGPL-3.0-or-later

## Use Case:

Developers and operators use this skill to run local, read-only posture checks against an existing Picoclaw profile and review severity-ranked findings before taking remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected posture profile may contain sensitive local configuration details.

Mitigation: Run the skill only on profiles intentionally selected for review and protect profile files and generated findings as sensitive operational data.

Risk: Standalone installs could be exposed to tampered release assets if the archive is trusted before verification.

Mitigation: Follow the signed-release verification steps for checksums, signature, public key fingerprint, archive hash, SKILL.md, and skill.json before installing or extracting the archive.

Risk: Security findings are operator guidance and may require context before remediation.

Mitigation: Review each finding and obtain explicit operator approval before making configuration changes.

## Reference(s):

- [ClawSec homepage](https://clawsec.prompt.security)
- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/picoclaw-self-pen-testing)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [Deterministic JSON containing a summary object and severity-ranked findings with recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a selected local Picoclaw posture profile and performs no network egress according to the release metadata.]

## Skill Version(s):

0.0.2 (source: frontmatter, skill.json, CHANGELOG, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
