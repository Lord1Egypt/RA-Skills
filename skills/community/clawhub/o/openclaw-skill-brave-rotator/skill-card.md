## Description: <br>
Brave Search API helper with automatic key rotation across multiple API keys to maximize free tier limits and fall back when rate limits are reached. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrnsmh](https://clawhub.ai/user/mrnsmh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to call Brave Search for web, news, or image results while rotating across user-provided API keys and retrying after rate-limit or forbidden responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Brave API keys supplied through BRAVE_API_KEYS. <br>
Mitigation: Use dedicated Brave API keys for this skill and avoid sharing them outside the intended agent runtime. <br>
Risk: The skill writes local rotation state that records per-key usage and cooldown information. <br>
Mitigation: Keep BRAVE_KEY_STATE_FILE on a protected local path and avoid sensitive or shared locations. <br>
Risk: The skill makes outbound requests to Brave Search endpoints. <br>
Mitigation: Install it only in environments where Brave Search API access is expected and allowed. <br>


## Reference(s): <br>
- [Brave Search API Reference](references/brave-api.md) <br>
- [Brave Search API Base URL](https://api.search.brave.com/res/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/mrnsmh/openclaw-skill-brave-rotator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, Python examples, and JSON search responses when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are formatted from Brave web, news, or image API responses; local state tracks per-key usage and cooldowns.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
