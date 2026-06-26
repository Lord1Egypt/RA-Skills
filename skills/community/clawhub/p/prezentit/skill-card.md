## Description: <br>
Generate AI-powered presentations with themes, custom design prompts, outlines, speaker notes, and downloadable results through the Prezentit API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VeGoVeVO](https://clawhub.ai/user/VeGoVeVO) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to help users create professional slide decks from a topic, outline, theme selection, or custom design prompt. It is intended for users who want the agent to check credits, call the Prezentit API, and return presentation links or download options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation topics, outlines, design prompts, and related content are sent to Prezentit. <br>
Mitigation: Avoid submitting secrets or regulated data unless approved for that use. <br>
Risk: The skill requires a Prezentit API key for authenticated API calls. <br>
Mitigation: Use a Prezentit-specific API key and keep it in the PREZENTIT_API_KEY environment variable. <br>
Risk: Presentation generation consumes account credits. <br>
Mitigation: Check available credits and expected cost before generating slides. <br>


## Reference(s): <br>
- [Prezentit website](https://prezentit.net) <br>
- [Prezentit API key management](https://prezentit.net/api-keys) <br>
- [ClawHub Prezentit skill page](https://clawhub.ai/VeGoVeVO/prezentit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP and JSON examples, generated presentation URLs, and optional download instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PREZENTIT_API_KEY and network access to https://prezentit.net/api/v1/*.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
