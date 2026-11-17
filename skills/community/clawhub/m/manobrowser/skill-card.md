## Description:

ManoBrowser operates a user's own Chrome browser with logged-in sessions to extract login-gated web data, reverse-engineer website APIs into reusable skills, and automate browser workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sophie-xin9](https://clawhub.ai/user/sophie-xin9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use ManoBrowser to operate a real Chrome session for browser automation, structured page extraction, platform exploration, API data skill generation, and reusable workflow creation for sites that may require login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access private data through a real logged-in Chrome session.

Mitigation: Use a separate browser profile or test account and avoid running it on sensitive sites unless the publisher and workflow are trusted.

Risk: The DEVICE_ID token can grant access to the connected browser service if exposed.

Mitigation: Store the token outside chats, prefer environment variables or a secrets-aware configuration path, and rotate or revoke it if it is exposed.

Risk: Browser data may pass through external services during MCP operation.

Mitigation: Review the connection endpoint and only connect accounts or browser profiles appropriate for the data-sharing risk.

Risk: Workflow logs, /tmp cookie files, TOOLS.md changes, or generated skills may persist sensitive data or agent behavior changes after use.

Mitigation: Review and remove those files or changes after execution, especially before sharing the workspace or generated skills.

## Reference(s):

- [ManoBrowser ClawHub Page](https://clawhub.ai/sophie-xin9/skills/manobrowser)
- [ManoBrowser Homepage](https://github.com/ClawCap/ManoBrowser)
- [ManoBrowser Chrome Web Store Listing](https://chromewebstore.google.com/detail/manobrowser/ihlggihggghoiijfcmgkapojamifohfh)
- [Browser Automation Module](browser-automation/SKILL.md)
- [Web Data Extractor Module](web-data-extractor/SKILL.md)
- [Platform Data Explorer Module](platform-data-explorer/SKILL.md)
- [API Skill Builder Module](api-skill-builder/SKILL.md)
- [Chrome Workflow Builder Module](chrome-workflow-build/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, code, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce generated skill files, workflow definitions, browser-extracted JSON, and configuration snippets depending on the selected module.]

## Skill Version(s):

2.2.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
