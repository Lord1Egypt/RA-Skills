## Description:

Compares a company's goal with its Cargo workspace each week and proposes up to five missing catalog pipelines for human review in a pull request and Slack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Revenue leaders and GTM engineering teams use this skill to identify catalog pipelines missing from their Cargo workspace and review prioritized suggestions through a pull request and Slack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flagged an unpinned command that can download and run a package.

Mitigation: Review the CLI package and pin the package-running command to an approved version before installation.

Risk: Some referenced content was only partly inspected; the scan covered 10 of 11 components.

Mitigation: Review the remaining referenced content before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cargo-ai/skills/goal-coverage)
- [Project homepage listed in release metadata](https://github.com/getcargohq/gtm-skills/tree/main/goal-coverage)
- [Published pipeline catalog](https://raw.githubusercontent.com/getcargohq/gtm-skills/main/catalog.json)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [A weekly Markdown coverage report opened as a pull request and a matching Slack post.]

**Output Parameters:** [Up to five pipeline suggestions per weekly run.]

**Other Properties Related to Output:** [Suggestions are grounded in workspace observations and require human review; the skill does not install pipelines.]

## Skill Version(s):

0.2.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
