## Description:

Roboflow (roboflow.com). Use this skill for ANY Roboflow request — reading, creating, and updating data. Whenever a task involves Roboflow, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill through an OOMOL-connected account to inspect Roboflow projects and versions, run object detection or workflows, and retrieve workflow or inference-server information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup may run downloaded code without clearly limiting the resulting changes; the installers were unavailable for inspection.

Mitigation: Review and approve CLI installation separately using a fixed, verified release.

Risk: Automatic bundled-skill synchronization may change installed skill files.

Mitigation: Check or disable automatic bundled-skill synchronization.

Risk: Roboflow data supplied to the integration passes through OOMOL.

Mitigation: Account for this data flow when connecting and using Roboflow.

Risk: Workflow actions can change Roboflow state.

Mitigation: Confirm the exact payload and effect before running write actions; require explicit approval for destructive actions.

## Reference(s):

- [Roboflow](https://roboflow.com/)
- [Roboflow REST API documentation](https://docs.roboflow.com/developer/rest-api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-roboflow)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell command examples, JSON inputs, and action-dependent JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by action; workflow actions return serialized outputs.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
