## Description:

Reports which delegation CLIs are installed and authenticated, and installs missing ones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check which delegation providers are installed and authenticated, identify providers ready to take work, and install missing provider CLIs before delegating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete because several referenced local paths were missing from the scan.

Mitigation: Review the complete skill package and rescan the missing referenced files before relying on the security verdict.

Risk: Installing a provider CLI changes the local environment.

Mitigation: Review each provider and its proposed installation, then confirm the skill's installation prompt only for providers you want.

## Reference(s):

- [Claude Night Market Conjure project (metadata homepage)](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)
- [ClawHub provider-setup release page](https://clawhub.ai/athola/skills/nm-conjure-provider-setup)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown table and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports provider binary, version, installation and authentication state, with remediation guidance.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
