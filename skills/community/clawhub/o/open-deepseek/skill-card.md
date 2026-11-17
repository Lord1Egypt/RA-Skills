## Description:

Opens Brave browser and navigates to DeepSeek website. Use when user says 'open deepseek' or 'go to deepseek'.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Users invoke this skill when they want an agent to open DeepSeek Chat in the Brave browser for manual prompting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches Brave locally and opens an external website.

Mitigation: Install only when local browser launch is acceptable, and review the configured destination before execution.

Risk: The Windows Python path invokes the platform launcher with shell=True.

Mitigation: Prefer a version that uses Python's webbrowser module or otherwise avoids shell=True on Windows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/open-deepseek)
- [DeepSeek Chat](https://chat.deepseek.com)
- [Brave Browser](https://brave.com)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Text status messages from a local browser-launch script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Brave browser to be installed locally.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
