## Description:

Tracks Monkeytype typing statistics, analyzes history and progress, looks up leaderboards, and provides improvement tips using the user's Monkeytype ApeKey.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qrucio](https://clawhub.ai/user/qrucio)

### License/Terms of Use:


## Use Case:

External users use this skill to connect their Monkeytype account, view typing stats and personal bests, compare recent performance, and receive typing improvement suggestions or optional reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Monkeytype ApeKey and may store it in a local plaintext configuration file.

Mitigation: Prefer setting MONKEYTYPE_APE_KEY directly and avoid pasting the ApeKey into chat or storing plaintext config on shared machines.

Risk: Optional automated reports can create scheduled jobs that persist after setup.

Mitigation: Enable automated reports only when cron-based persistence is acceptable and confirm how to remove the jobs later.

## Reference(s):

- [Monkeytype API](https://api.monkeytype.com)
- [ClawHub skill page](https://clawhub.ai/qrucio/skills/monkeytype-tracker)
- [ClawHub publisher profile](https://clawhub.ai/user/qrucio)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Monkeytype configuration and optional scheduled reports when the user enables automation.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
