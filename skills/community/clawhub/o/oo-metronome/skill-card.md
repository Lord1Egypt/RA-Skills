## Description:

Search and read Metronome data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and billing teams can retrieve Metronome customer, invoice, and billable metric data through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup executes unverified software downloaded from the internet, and its exact local effects are uncertain.

Mitigation: Review setup before installing; prefer a reviewed, version-pinned CLI installation and require approval for local installation or agent-skill changes.

Risk: Connecting Metronome gives OOMOL access to sensitive billing information.

Mitigation: Connect only an account authorized to share the relevant billing data, and review the setup before connecting.

## Reference(s):

- [Metronome API documentation](https://docs.metronome.com/)
- [Metronome](https://metronome.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON data]

**Output Format:** [JSON data and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only customer, invoice, and billable metric results.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
