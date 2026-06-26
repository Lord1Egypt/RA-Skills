## Description: <br>
Provides an OpenClaw fallback that replaces weak local-model responses with replies from a configured cloud chat-completions API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dream458268696](https://clawhub.ai/user/dream458268696) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users configure this skill to route weak, empty, generic, or failed local responses to a cloud model so the agent can return a substitute answer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The fallback gate can send ordinary prompts and recent chat context to the configured API, not only failed or low-confidence responses. <br>
Mitigation: Fix and review the fallback logic before deployment, disclose external data handling, and limit the prompt history and metadata sent to approved endpoints. <br>
Risk: The bundle includes an API-key-like value in configuration. <br>
Mitigation: Replace the bundled configuration before use, rotate the value if it was real, and avoid publishing secrets in release artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dream458268696/openclaw-fallback-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, API calls] <br>
**Output Format:** [Plain text or streamed chat response from the configured cloud model API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include fallback error guidance when the configured API call fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
