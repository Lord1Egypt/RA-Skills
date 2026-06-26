## Description: <br>
Analyzes user mood text with the mood CLI and returns a weather icon, emotion label, confidence score, and comforting copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanwan2qq](https://clawhub.ai/user/wanwan2qq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn short Chinese or English mood statements into a weather-themed emotional summary through a configured CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mood text may include sensitive personal or health-adjacent information and can be sent to a third-party AI service. <br>
Mitigation: Use a dedicated API key, avoid entering highly sensitive personal or medical details, and review the CLI's storage and deletion behavior before use. <br>
Risk: The install script installs an external npm package globally without a pinned version. <br>
Mitigation: Install only after trusting the mood-weather-cli package, and prefer reviewing or pinning the package version in controlled environments. <br>
Risk: Broad mood-related trigger phrases can activate the skill during ordinary conversation. <br>
Mitigation: Review trigger patterns before deployment and prefer explicit invocation where unintended mood analysis would be inappropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanwan2qq/mood-cli-release) <br>
- [mood-weather-cli npm package](https://www.npmjs.com/package/mood-weather-cli) <br>
- [DeepSeek platform](https://platform.deepseek.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text with a weather icon, emotion label, confidence score, and short supportive copy.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the mood CLI binary and DEEPSEEK_API_KEY; responses may fall back to local keyword matching when the external API is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, package.json, CHANGELOG, released 2026-03-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
