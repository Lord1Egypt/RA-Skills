## Description:

JoeVault helps agents audit, classify, and quarantine stale filesystem paths after profile switches, account migrations, resets, or workspace moves without disrupting active state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeproai](https://clawhub.ai/user/joeproai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical operators use JoeVault to inspect stale profile, account, home-directory, and workspace paths before deciding whether to keep, inventory, or quarantine them. It is intended for conservative local cleanup where inactive state should be archived without breaking active configs, symlinks, or services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quarantine script can move data outside the intended archive path if given an unsafe label.

Mitigation: Use only audited source paths and simple label names with no slashes or '..', review the script before broad use, and keep backups before moving data.

Risk: Large or recently active stale workspaces may contain important work, model assets, media, or repositories that should not be moved blindly.

Mitigation: Audit first, inventory large trees and recent activity, and quarantine only small, clearly inactive paths that are not referenced by active configuration.

## Reference(s):

- [Classification guide](references/classification.md)
- [ClawHub skill page](https://clawhub.ai/joeproai/skills/joevault)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON reports, Markdown]

**Output Format:** [Markdown guidance with bash commands, JSON audit output, and Markdown archive manifest entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quarantine commands can perform persistent filesystem moves and should be run only after reviewing the audit results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
