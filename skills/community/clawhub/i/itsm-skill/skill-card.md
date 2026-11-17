## Description:

Automates ITSM ticket submission through a local Chromium browser and Selenium for head-leg inquiries, tail-leg inquiries, batch queries, and issue feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tutututu2020](https://clawhub.ai/user/tutututu2020)

### License/Terms of Use:

MIT-0

## Use Case:

Operations or support users use this skill to fill and submit logistics-related ITSM tickets in an enterprise IT service management system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded ITSM credentials could expose account access if the package or logs are shared.

Mitigation: Remove hard-coded credentials, rotate the exposed account password, and pass secrets through a managed secret store or environment variables.

Risk: The automation can submit a live ITSM ticket without an explicit final approval step.

Mitigation: Add a confirmation prompt or dry-run mode before clicking the final submit action.

Risk: Automatic sudo, apt, pip, and bootstrap downloads can change the host environment during startup.

Mitigation: Install reviewed prerequisites in advance and disable network bootstrap installation in production environments.

Risk: Screenshots and debug output may capture usernames, ticket contents, attachment paths, or other sensitive service data.

Mitigation: Disable automatic screenshots and password logging, or store redacted screenshots with restricted retention and access controls.

Risk: A Chromium remote debugging port is opened for browser control during automation.

Mitigation: Bind browser debugging to local trusted contexts only and close the browser process after each controlled run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tutututu2020/skills/itsm-skill)
- [Publisher profile](https://clawhub.ai/user/tutututu2020)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration, guidance]

**Output Format:** [Terminal logs, browser actions, and screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit a live ITSM ticket and save local screenshots during execution.]

## Skill Version(s):

2.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
