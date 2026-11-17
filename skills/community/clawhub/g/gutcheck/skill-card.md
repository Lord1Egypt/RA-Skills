## Description:

GutCheck is a digestive health tracking application that provides personalized insights and data-driven recommendations to help users understand food sensitivities and optimize gut wellness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allen566](https://clawhub.ai/user/allen566)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to install and operate a digestive health tracker for meal logging, digestive response tracking, food sensitivity pattern review, and personalized wellness recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs code from a mutable remote GitHub repository and resolves npm dependencies at install time.

Mitigation: Review the current repository state before installation, prefer a release pinned to a specific commit, and use committed lockfiles with npm ci where available.

Risk: The skill handles digestive health data and may present wellness recommendations.

Mitigation: Review privacy and medical-safety limits before use, avoid treating outputs as medical advice, and consult qualified healthcare professionals for diagnosis or treatment decisions.

Risk: The package includes a publishing script that executes ClawHub CLI commands.

Mitigation: Do not run publishing commands unless you intend to publish the skill and have reviewed the target account, package contents, and command arguments.

## Reference(s):

- [GutCheck ClawHub Skill Page](https://clawhub.ai/allen566/skills/gutcheck)
- [GutCheck Repository](https://github.com/openclaw/gutcheck.git)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, MongoDB configuration, and local environment variables for the installed application.]

## Skill Version(s):

1.0.0 (source: package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
