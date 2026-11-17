## Description:

Prepare, snapshot, run, rerun, debug, or interpret OpenClaw Parallels guest install, onboarding, gateway smoke, and upgrade checks across macOS, Windows, and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to run and interpret OpenClaw install, onboarding, gateway, and update smoke checks in Parallels guests across macOS, Windows, and Linux.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that guest installation may use an unauthenticated HTTP package source, which could allow a substituted package to run.

Mitigation: Use a package source you trust and verify the package independently before installation.

Risk: The security evidence says analysis is incomplete because local path-like references could not be resolved.

Mitigation: Review the complete skill package and resolve referenced files before relying on the guidance.

## Reference(s):

- [Openclaw Parallels Smoke on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-parallels-smoke)
- [Publisher profile: hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Analysis]

**Output Format:** [Markdown guidance with shell commands and JSON smoke summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations vary by guest operating system, package version, and smoke workflow.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
