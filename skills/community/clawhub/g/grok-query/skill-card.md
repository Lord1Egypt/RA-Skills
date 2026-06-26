## Description: <br>
Query Grok AI (grok.com) for real-time information via browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[InphinitiZ](https://clawhub.ai/user/InphinitiZ) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to query Grok through an authenticated OpenClaw browser session for current information, fact checks, news, and multi-turn research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent uses the user's logged-in Grok browser session and sends prompts to Grok. <br>
Mitigation: Use only with prompts and context that the user intends Grok to receive; avoid passwords, private documents, regulated data, and other sensitive content. <br>
Risk: Browser automation can be blocked by login prompts, CAPTCHA, popups, quota limits, or Grok UI changes. <br>
Mitigation: Require the user to complete login or human verification manually, refresh page state with browser snapshots, and stop with a clear user-facing message when quota or timeout limits are reached. <br>


## Reference(s): <br>
- [Grok](https://grok.com) <br>
- [ClawHub release page](https://clawhub.ai/InphinitiZ/grok-query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and browser workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenClaw browser session already logged in to Grok; responses are subject to Grok availability, UI state, account limits, and user-entered prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
