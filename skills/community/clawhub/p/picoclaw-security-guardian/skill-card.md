## Description:

Picoclaw security posture skill with advisory awareness, configuration drift detection, and supply-chain verification guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

AGPL-3.0-or-later

## Use Case:

Developers and operators use this skill to review Picoclaw gateway security posture, compare local configuration drift, check Picoclaw-relevant advisories, and verify release artifacts before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated profile and drift reports can expose sensitive operational details such as local paths, file hashes, file modes, and security-marker counts.

Mitigation: Treat generated reports as sensitive operational records and keep them in restricted Picoclaw security storage.

Risk: Standalone installs can be unsafe if release artifacts are trusted before source and signing checks complete.

Mitigation: Verify the release source, pinned signing key, checksum manifest, archive hash, and detached signature before extracting or installing artifacts.

Risk: Unsigned or unverified advisory feed state can weaken advisory results.

Mitigation: Use verified feed state for normal operation and reserve unsigned advisory mode for short, documented emergency or offline windows.

Risk: The skill is scoped to Picoclaw environments and may not reflect different gateway or wrapper trust boundaries.

Mitigation: Use it only for Picoclaw deployments and review third-party wrappers or adjacent gateway components separately.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davida-ps/skills/picoclaw-security-guardian)
- [ClawSec Homepage](https://clawsec.prompt.security)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [CHANGELOG.md](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON profile, drift, advisory, and supply-chain verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [On-demand outputs may include local paths, file hashes, file modes, advisory records, and security-marker counts.]

## Skill Version(s):

0.0.3 (source: SKILL.md frontmatter, skill.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
