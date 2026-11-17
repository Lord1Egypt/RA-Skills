## Description:

Use Cyberimpact to read, create, update, and delete account data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Cyberimpact members, groups, and email templates through an already connected OOMOL account. It supports retrieval and approved creation, updates, and deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the agent to run a remote CLI installer whose behavior has not been verified.

Mitigation: Review CLI installation separately, use a pinned and verified release, and check the CLI's broader skill-installation behavior before running it.

Risk: Connecting Cyberimpact authorizes OOMOL-mediated account access, and write or delete actions can change account data.

Mitigation: Retain user approval for changes and deletions, and review the exact payload and target before execution.

## Reference(s):

- [Cyberimpact API documentation](https://api.cyberimpact.com/docs)
- [Cyberimpact](https://www.cyberimpact.com/)
- [oo CLI source and documentation](https://github.com/oomol-lab/oo-cli)
- [Cyberimpact skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-cyberimpact)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON payloads and structured connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses action-specific schemas; state-changing operations require user approval.]

## Skill Version(s):

1.0.5 (source: skill frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
