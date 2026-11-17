## Description:

Google Workspace CLI for Gmail, Calendar, and Auth (restricted via security wrapper).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cettoana](https://clawhub.ai/user/cettoana)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to interact with Google Workspace through the gog-restricted wrapper for Gmail, Calendar, and auth workflows while following documented command restrictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports that the Google Workspace safety wrapper appears vulnerable to an argument-parsing bypass that could undermine blocked Gmail or Calendar actions.

Mitigation: Install only with accounts where this risk is acceptable, and verify the wrapper parses and executes the same normalized arguments before using it with sensitive accounts.

Risk: The wrapper uses the Google account already authorized for gog.

Mitigation: Prefer a profile-isolated install directory and avoid connecting accounts that contain sensitive mail or calendar data until the wrapper security issue is resolved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cettoana/skills/gog-restricted)
- [Publisher profile](https://clawhub.ai/user/cettoana)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog-restricted binary and a Google account already authorized for gog.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
