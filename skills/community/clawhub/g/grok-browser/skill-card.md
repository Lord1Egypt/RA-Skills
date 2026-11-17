## Description:

Query Grok AI via browser automation. Use when you need to ask Grok questions, get AI responses, or use Grok's DeepSearch/Think features. Copies response text instead of using screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easonc13](https://clawhub.ai/user/easonc13)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to query Grok through a Chrome browser session, submit prompts, enable DeepSearch or Think workflows, and copy completed responses from the page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives the agent control of a real Chrome Grok session.

Mitigation: Use a dedicated browser profile with no unrelated tabs or sensitive accounts.

Risk: Prompt text is inserted through JavaScript evaluate templates.

Mitigation: Serialize untrusted prompt text safely before evaluation.

Risk: Clipboard reads may expose content copied before the skill runs.

Mitigation: Clear or inspect the clipboard before using the skill and treat copied output as sensitive.

## Reference(s):

- [Grok](https://grok.com)
- [ClawHub skill page](https://clawhub.ai/easonc13/skills/grok-browser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with browser automation and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces copied Grok response text from an existing browser session.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
