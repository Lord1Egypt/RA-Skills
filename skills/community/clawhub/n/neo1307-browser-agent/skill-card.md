## Description:

Browser Agent uses Playwright to open pages, take screenshots, extract titles or selector text, click and fill selectors, and save or load browser session state for deterministic web UI automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neo1307](https://clawhub.ai/user/neo1307)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to smoke-test web pages, gather DOM or screenshot evidence, and automate straightforward browser flows with explicit selectors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Typed form values can be exposed in command output.

Mitigation: Do not pass passwords, tokens, payment details, or other secrets through --fill.

Risk: Saved browser session state can preserve account access.

Mitigation: Treat saved session files as secrets, keep them in protected locations, avoid sharing them, and only load session state for known accounts and sites.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration]

**Output Format:** [JSON command results with optional PNG screenshots and browser storage-state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit URLs and selectors; saved session state should be protected as sensitive data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
