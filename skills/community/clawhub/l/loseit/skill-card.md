## Description:

Retrieves a user's Lose It! nutrition data and emits daily nutrition and meal breakdowns as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stozo04](https://clawhub.ai/user/stozo04)

### License/Terms of Use:

MIT

## Use Case:

Individuals and personal assistant agents use the skill to retrieve a user's Lose It! nutrition history for review or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configuration file can contain a plaintext Lose It! password, and the cached session token is a reusable credential that can expose nutrition data if accessed by others.

Mitigation: On shared machines, prefer LOSEIT_EMAIL and LOSEIT_PASSWORD environment variables; keep configuration and token files in owner-only locations and do not share or back them up.

Risk: Nutrition data is retrieved from the account export and printed for the calling agent to use.

Mitigation: Use the skill only in a trusted agent environment and limit downstream handling or sharing to the nutrition data the user intends to disclose.

## Reference(s):

- [Lose It CLI project](https://github.com/stozo04/loseit-cli)
- [Lose It CLI releases](https://github.com/stozo04/loseit-cli/releases)
- [Machine contract and exit codes](https://github.com/stozo04/loseit-cli/blob/main/docs/MACHINE_CONTRACT.md)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON keyed by date with nutrition totals and meal details; the CLI can also print a human-readable table.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only nutrition data is printed to stdout; login may save a session token locally.]

## Skill Version(s):

1.0.9 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
