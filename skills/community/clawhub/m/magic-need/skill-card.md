## Description:

Magic Need lets agents register missing tools, APIs, or data sources during task execution so teams can review categorized needs and plan integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guim4dev](https://clawhub.ai/user/guim4dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Magic Need to capture missing-tool and missing-data requests from agents, categorize them, and review reports that inform an integration roadmap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may record sensitive need descriptions, such as secrets, personal data, incident details, or confidential system names, in a local JSON file.

Mitigation: Instruct agents and reviewers not to enter sensitive data, and review ~/.magic-need/needs.json before retaining or sharing reports.

Risk: Generated reports may expose locally retained unmet-tool requests beyond the intended audience.

Mitigation: Review report contents before sending them to notification systems or roadmap-tracking workflows.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/guim4dev/skills/magic-need)
- [OpenClaw](https://openclaw.ai)
- [Sonarly](https://www.sonary.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [CLI text confirmations, Markdown reports, and JSON records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes need records to ~/.magic-need/needs.json and reports pending needs grouped by category.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
