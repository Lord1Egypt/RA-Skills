## Description:

Develop, test, or integrate the OpenClaw Tally Node.js library for task-level cost, complexity, and efficiency analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathanjing](https://clawhub.ai/user/jonathanjing)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to work with a local OpenClaw analytics library that detects task boundaries, attributes token costs, and computes task efficiency scores. It is intended for explicit plugin or operator-owned hook integrations, not automatic runtime activation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task intent, outcomes, session identifiers, model names, costs, and cron metadata may be stored locally in plaintext after integration.

Mitigation: Disclose the stored fields before enabling an integration, avoid passing raw user messages into summary fields, and add retention or deletion controls for the SQLite database.

Risk: A message-post hook integration could observe every message even though the skill does not auto-register hooks.

Mitigation: Enable processing only through an explicit plugin or operator-owned hook and document the event scope before activation.

Risk: Local analytics records may contain sensitive task metadata.

Mitigation: Use the default local database path where possible, restrict filesystem permissions, and limit test paths to controlled temporary locations.

Risk: The dependency set includes a native SQLite addon.

Mitigation: Update dependencies and run the test suite or CI before deployment.

## Reference(s):

- [OpenClaw Tally project homepage](https://github.com/JonathanJing/openclaw-tally)
- [OpenClaw Tally on ClawHub](https://clawhub.ai/jonathanjing/skills/openclaw-tally)
- [Product requirements document](PRD.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local integration guidance for Node.js, SQLite storage, tests, and explicit OpenClaw plugin or hook wiring.]

## Skill Version(s):

0.3.2 (source: frontmatter, package.json, skill.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
