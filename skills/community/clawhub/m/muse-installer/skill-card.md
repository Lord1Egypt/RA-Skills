## Description:

Muse Installer helps an agent install Muse, start its local service, guide onboarding, collect three profile answers, analyze creator-platform content when provided, and sync the resulting creator DNA to the Muse dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevph2026](https://clawhub.ai/user/kevph2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent install Muse locally, launch its service, load the browser extension, and complete onboarding for Muse's creator-DNA workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs code downloaded from a repository at execution time.

Mitigation: Review the downloaded code before execution and use the skill only when the repository and current branch are trusted.

Risk: The skill instructs users to sideload a browser extension.

Mitigation: Review the extension permissions and source files before loading the unpacked extension into Chrome.

Risk: The Telegram Bot setup asks for a bot token in chat.

Mitigation: Avoid sharing tokens in chat; set secrets directly in the local environment and rotate any token that was exposed.

Risk: The skill starts a local background service and stores onboarding profile data.

Mitigation: Confirm stop, uninstall, and data deletion steps before using the service or profile features.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevph2026/skills/muse-installer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and conversational onboarding prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local service URLs, browser extension loading steps, profile analysis text, and token-handling guidance.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
