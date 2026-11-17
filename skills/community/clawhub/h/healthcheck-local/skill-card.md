## Description:

Track water and sleep with JSON file storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larry-at](https://clawhub.ai/user/larry-at)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent record water intake, sleep, wake events, and simple health statistics in a local JSON file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Water-count commands can insert user input into executable JavaScript.

Mitigation: Review before installation, validate cup counts as bounded numbers, and pass values as arguments instead of interpolating them into source code.

Risk: Update and delete commands modify local health history.

Mitigation: Review command behavior before use and keep backups or recovery controls for {baseDir}/health-data.json when records matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/larry-at/skills/healthcheck-local)
- [Publisher profile](https://clawhub.ai/user/larry-at)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and local JSON file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js built-in modules and writes health records to {baseDir}/health-data.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
