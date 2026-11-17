## Description:

Inspect, patch, validate, publish, or confirm OpenClaw GHSA security advisories and private-fork state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect and manage OpenClaw GitHub Security Advisories, verify private-fork state, and prepare advisory updates for review and publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reported incomplete coverage because the referenced SECURITY.md could not be resolved.

Mitigation: Read and follow the repository's SECURITY.md before reviewing or publishing an advisory, as required by the skill.

Risk: Publishing an advisory before confirming its state and private-fork PR status could lead to an invalid or premature release.

Mitigation: Inspect the current advisory and verify that its private fork has no open PRs; obtain permission before any publish action.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/hillstreet-ph/skills/oc-ghsa-maintainer)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, API calls]

**Output Format:** [Markdown guidance with shell command examples and JSON payload patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare advisory content and API payloads for a specified GHSA.]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
