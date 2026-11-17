## Description:

Deploys a three-agent adaptive AI tutoring setup with content-curator, tutor, and assessor roles for lesson delivery, learner assessment, and curriculum feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up a Pilot Protocol tutoring pipeline across three cooperating agents: a content curator, a tutor, and an assessor. The setup supports lesson-material delivery, learner-response routing, gap analysis, and curriculum adaptation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup exchanges learner responses, progress, and gap-analysis data among trusted agents.

Mitigation: Define consent, access control, retention, and cleanup practices before use, and avoid real learner identifiers in examples or test traffic.

Risk: The setup installs dependency skills and configures trust relationships through shell commands.

Mitigation: Review the named dependency skills, confirm trusted versions, and verify peer hostnames before initiating handshakes.

Risk: The hostname prefix and local setup manifest can affect agent identity and persisted setup state.

Mitigation: Use a simple validated prefix containing only letters, numbers, underscores, or hyphens, and review access permissions and cleanup for the ~/.pilot setup manifest.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-ai-tutoring-system-setup)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with bash commands and role-specific JSON manifest templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role setup instructions, hostname and handshake commands, dependency skill lists, and local Pilot setup manifest content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
