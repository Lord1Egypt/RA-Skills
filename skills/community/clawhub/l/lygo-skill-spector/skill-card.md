## Description:

LYGO SkillSpector is a local static risk scanner for ClawHub and OpenClaw skill packages that can scan, gate CI checks, batch-check skill folders, and produce reports for execution, network, secret-like, destructive-action, and permission-claim mismatch signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and security reviewers use this skill to audit ClawHub/OpenClaw skill folders before installation, enforce CI risk gates, batch-check skill roots, and generate local risk reports for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner reports can include snippets from scanned files, including secrets that were already present in those files.

Mitigation: Scan only intended directories and review or redact reports before sharing them or storing them in public logs.

Risk: Using @latest during installation can resolve to a different package version over time.

Mitigation: Pin the intended release version or independently verify the package before use in high-assurance environments.

Risk: Static scanner findings may include false positives, and a clean result is not a guarantee that code is safe.

Mitigation: Treat findings as review guidance and inspect the flagged source paths before installing or approving a skill.

Risk: The separate SkillHub FULL builder pack is outside the public ClawHub artifact reviewed here.

Mitigation: Review and scan the FULL builder package independently before using it.

## Reference(s):

- [SkillSpector quickstart](examples/quickstart.md)
- [Security notes](references/SECURITY.md)
- [SkillSpector audit response](references/SKILLSPECTOR_AUDIT.md)
- [LYGO SkillSpector homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-skill-spector)
- [LYGO SkillSpector ClawHub page](https://clawhub.ai/deepseekoracle/skills/lygo-skill-spector)
- [SkillHub FULL LYGO builder pack](https://chatagent.ca/lygoskillhub.html#full-lygo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON scanner reports with CLI exit codes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are local; file writes are intended for state/ only when --i-consent is provided.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, claw.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
