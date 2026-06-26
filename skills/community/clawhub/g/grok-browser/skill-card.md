## Description: <br>
Query Grok AI via browser automation. Use when you need to ask Grok questions, get AI responses, or use Grok's DeepSearch/Think features. Copies response text instead of using screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EasonC13](https://clawhub.ai/user/EasonC13) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to operate a Chrome session against grok.com, submit prompts to Grok, optionally use DeepSearch or Think features, and copy response text from the browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to operate a real Chrome session for Grok through an external relay and raw browser JavaScript. <br>
Mitigation: Use a dedicated Chrome profile with only the required Grok account, verify the Browser Relay extension and attach script before use, and confirm browser actions target grok.com. <br>
Risk: Copied Grok responses and browser clipboard contents may expose sensitive information. <br>
Mitigation: Avoid keeping secrets on the clipboard and review copied response text before reusing or sharing it. <br>


## Reference(s): <br>
- [Grok](https://grok.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell and browser automation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Chrome profile, Browser Relay extension, and clipboard access to copy Grok responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
