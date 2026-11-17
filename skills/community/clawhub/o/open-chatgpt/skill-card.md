## Description:

Opens Brave browser directly to ChatGPT for instant AI conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to quickly open ChatGPT in Brave from a voice or typed trigger when they want fast access to the chat interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches Brave locally and opens an external ChatGPT URL, so it may fail or surprise users if Brave is absent or a browser launch is not expected.

Mitigation: Confirm Brave is installed and that local browser launch behavior is acceptable before enabling the skill.

Risk: The Windows launch path uses shell=True.

Mitigation: Keep the URL fixed and review any future command changes before release; prefer an implementation that avoids shell=True on Windows.

## Reference(s):

- [ChatGPT](https://chat.openai.com)
- [ClawHub open-chatgpt skill page](https://clawhub.ai/ruchir17-cmd/skills/open-chatgpt)

## Skill Output:

**Output Type(s):** [Shell commands, Text]

**Output Format:** [Local browser launch plus a short status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Brave browser, internet access, and a ChatGPT account.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
