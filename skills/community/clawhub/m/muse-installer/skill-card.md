## Description: <br>
Muse Installer helps an agent install Muse, start the local dashboard service, guide onboarding, collect creator DNA responses, analyze recent creator-platform content, and sync the profile to the dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevph2026](https://clawhub.ai/user/kevph2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent install and launch Muse locally, load the browser extension, and guide onboarding that creates a creator DNA profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill pulls and runs remote code as a background local service. <br>
Mitigation: Review the repository and commands before running the installer, and run it only in an environment where a local background service is acceptable. <br>
Risk: The optional Telegram setup asks the user to provide a bot token. <br>
Mitigation: Treat Telegram bot tokens as secrets, avoid sharing real tokens in ordinary chat, and rotate any token that may have been exposed. <br>
Risk: The onboarding flow stores interests, occupation, creator links, and inferred profile data in the local Muse dashboard. <br>
Mitigation: Share only profile details that are appropriate for the local dashboard and review the stored profile before relying on it. <br>


## Reference(s): <br>
- [Muse Installer on ClawHub](https://clawhub.ai/kevph2026/skills/muse-installer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local service setup, onboarding prompts, browser extension loading, optional Telegram bot configuration, and profile sync.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
