## Description:

Operate Framejet through an OOMOL-connected account to create signed capture URLs and capture public web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to request Framejet page captures or create signed capture URLs through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, the setup path may run an unverified online installer without separate user approval.

Mitigation: Review the setup path before enabling the skill; install a reviewed, version-pinned CLI yourself and require approval before any installer or bundled-skill changes run.

## Reference(s):

- [Framejet integrations documentation](https://framejet.dev/integrations)
- [Framejet](https://framejet.dev)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-framejet)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Markdown, Shell commands]

**Output Format:** [Framejet action results in JSON, summarized as text or Markdown; shell commands are used to invoke actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the live Framejet action schema and connected account.]

## Skill Version(s):

1.0.2 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
