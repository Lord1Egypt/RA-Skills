## Description:

Operate Render through an OOMOL-connected account to inspect resources and manage services and deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and service operators use this skill to inspect Render users, workspaces, services, and deploys, and to manage service and deployment state through their connected Render account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run unpinned downloaded code and add bundled agent skills without clearly requesting approval.

Mitigation: Review setup before installation, approve CLI installation separately, verify the selected release, and review or disable automatic bundled-skill synchronization.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Render](https://render.com)
- [Render API documentation](https://render.com/docs/api)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-render)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, JSON, Shell commands]

**Output Format:** [Markdown guidance, oo CLI commands, and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read Render data or change service and deployment state; user confirmation is required for writes and destructive actions.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
