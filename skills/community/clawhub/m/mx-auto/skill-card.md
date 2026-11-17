## Description:

Local Runtime automation entrypoint for App triggers, read-only browser sandbox inspection, and local script execution. Use when the user wants to list or run Runtime triggers, inspect existing browser sandbox tabs/snapshots, or list/show/run local App scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiming1001](https://clawhub.ai/user/yiming1001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to route local Runtime automation requests for trigger execution, read-only browser sandbox inspection, and local App script listing or execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Runtime and cloud tokens and can send them to configurable URLs.

Mitigation: Use only trusted Runtime base URLs and stored preferences, avoid storing cloud tokens with the preference helper, and rotate any Runtime or cloud token that may have been used with an untrusted configured URL.

Risk: Trigger and script execution can perform local Runtime automation with side effects.

Mitigation: Review commands before execution, use exact trigger or script names, and do not fuzzy-match execution targets.

Risk: Browser sandbox inspection may expose content from already-open tabs.

Mitigation: Use the sandbox workflow only for read-only tab listing or snapshots of existing targets and avoid navigation, clicks, typing, or other browser state changes.

## Reference(s):

- [mx-auto Skill Page](https://clawhub.ai/yiming1001/skills/mx-auto)
- [mx-auto Learning Guide](references/learning-guide.md)
- [Sandbox Workflow](references/sandbox.md)
- [Scripts Workflow](references/scripts.md)
- [Trigger Workflow](references/triggers.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Text]

**Output Format:** [Markdown guidance with shell commands and text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Runtime trigger lists, trigger run results, browser tab or snapshot summaries, script catalog entries, script run results, and clear failure messages.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
