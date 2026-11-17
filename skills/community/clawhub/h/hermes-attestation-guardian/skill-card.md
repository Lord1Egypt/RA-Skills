## Description:

Hermes-only runtime security attestation and drift detection skill for operator-managed Hermes infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate deterministic Hermes posture attestations, verify attestation integrity fail-closed, compare authenticated baseline drift, and run advisory-aware guarded verification for Hermes-managed infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Attestations may expose watched file paths, trust anchor paths, and hashes from Hermes security state.

Mitigation: Review watch_files and trust_anchor_files before use, protect ~/.hermes, and limit access to generated attestation artifacts.

Risk: Recurring scheduler setup can mutate the current user's cron state when --apply is used.

Mitigation: Preview scheduler entries with --print-only, avoid running scheduled jobs as root, and apply only the managed Hermes schedule blocks intentionally.

Risk: Unsigned advisory feed bypass weakens fail-closed verification.

Mitigation: Use --allow-unsigned only during a short audited emergency window and remove it immediately after recovery.

Risk: Using the skill outside Hermes infrastructure can produce unsupported trust and attestation assumptions.

Mitigation: Install and operate the skill only for Hermes CLI, Gateway, or profile-managed deployments.

## Reference(s):

- [ClawSec Homepage](https://clawsec.prompt.security)
- [ClawHub Skill Page](https://clawhub.ai/davida-ps/skills/hermes-attestation-guardian)
- [Skill Operator Playbook](artifact/SKILL.md)
- [Capability Overview](artifact/README.md)
- [Release Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Hermes attestation JSON files, optional sha256 sidecar files, advisory feed verification state, and optional managed cron entries when explicitly applied.]

## Skill Version(s):

0.1.3 (source: frontmatter, changelog, server release evidence; released 2026-05-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
