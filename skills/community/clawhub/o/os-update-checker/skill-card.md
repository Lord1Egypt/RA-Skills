## Description:

Checks available OS and global npm package updates with per-package changelog summaries and risk classification across apt, dnf, yum, pacman, zypper, apk, brew, and npm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and operations teams use this skill to check system and global npm update status, review version deltas and changelog context, and decide whether to approve or defer upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package names and installed tooling may be exposed to external changelog services or package registries when changelog lookup is enabled.

Mitigation: Use --no-changelog to reduce network activity, and avoid running the skill in environments where installed package names are sensitive.

Risk: Reports can reveal system software inventory, package versions, and update posture.

Mitigation: Review text or JSON output before sharing it outside the intended operations or security team.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pfrederiksen/skills/os-update-checker)
- [Publisher Profile](https://clawhub.ai/user/pfrederiksen)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text report or JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports package names, current and target versions, source, risk label, and changelog summary when available; --no-changelog reduces network activity.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter and README show 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
