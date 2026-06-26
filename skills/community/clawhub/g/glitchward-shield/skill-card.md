## Description: <br>
Scan prompts for prompt injection attacks before sending them to any LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eyeskiller](https://clawhub.ai/user/eyeskiller) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to validate user prompts, external content, and agent workflow outputs with the Glitchward Shield API before passing them to an LLM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, documents, emails, web content, and agent workflow outputs may be sent to Glitchward for scanning. <br>
Mitigation: Use the skill only for data your organization has approved for the provider, and avoid regulated, secret, or sensitive content unless the provider terms have been reviewed. <br>
Risk: A Shield API token is required for all requests. <br>
Mitigation: Use a dedicated token stored in GLITCHWARD_SHIELD_TOKEN and rotate or revoke it if exposure is suspected. <br>
Risk: Examples pass user-controlled text through shell commands. <br>
Mitigation: Construct JSON safely instead of interpolating raw user text into shell command strings. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/eyeskiller/glitchward-shield) <br>
- [Glitchward Shield](https://glitchward.com/shield) <br>
- [LLMPI Database](https://glitchward.com/llmpi) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/eyeskiller) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and GLITCHWARD_SHIELD_TOKEN; API responses include block decisions, risk scores, and match details.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
