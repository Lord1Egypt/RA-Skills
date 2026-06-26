## Description: <br>
Openclaw Cat lets OpenClaw users trigger a cat-status roleplay response from a configured LLM with a persistent randomly generated cat persona. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tony888880lang](https://clawhub.ai/user/tony888880lang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users configure a cat name and model API key, then use `/cat` or cat-status questions to receive a playful in-character response about what the cat is doing and thinking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an LLM API key and sends generated cat prompts, cat name, and cat profile details to the configured provider. <br>
Mitigation: Use a dedicated API key with spending limits and configure only providers you trust. <br>
Risk: A custom `base_url` can route requests to a non-default endpoint. <br>
Mitigation: Leave `base_url` empty unless the endpoint is trusted and expected for the selected model provider. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tony888880lang/openclaw-cat) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Plain text roleplay response with setup guidance in Markdown documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are generated through the user-configured LLM provider using the configured cat profile and current time.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
