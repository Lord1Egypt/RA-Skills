## Description:

Make OpenClaw launch the Ashen Era CLI build, play a real run, and deliver a complete first-person play report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssochi](https://clawhub.ai/user/ssochi)

### License/Terms of Use:

MIT-0

## Use Case:

Players, developers, and reviewers use this skill to have an agent run one real Ashen Era CLI session, then produce a grounded first-person play report covering setup, decisions, combat, outcome, and retrospective.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches a local CLI game executable selected for the current platform.

Mitigation: Install only when local game execution is acceptable, and use the documented launcher flow rather than arbitrary subcommands.

Risk: The inspected package did not include the release archives the skill says it bundles, so the launcher may fail at runtime.

Mitigation: Confirm the expected platform archive is present before relying on the skill for a play report.

Risk: Debug or non-play commands could produce a report that is not based on a genuine run.

Mitigation: Use the documented `play` flow and avoid `autoplay`, `scout`, `whoisyourdad`, and debug commands.

## Reference(s):

- [CLI Surface](references/cli-surface.md)
- [Report Contract](references/report-contract.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown narrative report with inline shell command details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report should reflect a real completed CLI run and avoid strategy guidance, design critique, suggestions, and bug-triage lists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
