## Description:

Use this skill for Fundable requests to read, create, and update data through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People with a connected Fundable account can search and review company, deal, investor, and person data, retrieve alerts, and request verified contact details when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup runs a remote installer whose contents were unavailable for inspection, so its exact local changes are unknown.

Mitigation: Prefer a reviewed, version-pinned oo CLI installation and check its automatic skill synchronization settings before proceeding.

Risk: Verified email and phone lookups unlock contact information and may consume credits.

Mitigation: Use these lookups only when explicitly needed and confirm the intended Fundable account and paid unlock before running them.

## Reference(s):

- [Fundable](https://www.tryfundable.ai)
- [Fundable API documentation](https://docs.tryfundable.ai/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON payloads; connector responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses include data and execution metadata.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
