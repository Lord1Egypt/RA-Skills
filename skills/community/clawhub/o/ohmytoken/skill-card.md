## Description: <br>
Tracks LLM token counts and visualizes model usage as real-time pixel art at ohmytoken.dev. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x5446](https://clawhub.ai/user/0x5446) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers using OpenClaw use this skill to send model names and token counts after LLM calls so they can view token usage visualizations, achievements, and usage summaries at ohmytoken.dev. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends model names and token counts to ohmytoken.dev after LLM calls. <br>
Mitigation: Install only where this usage metadata is acceptable to share, especially in workplaces with regulated or confidential model-usage data. <br>
Risk: The ohmytoken API key could be exposed if stored in committed configuration files. <br>
Mitigation: Use a dedicated ohmytoken API key and configure it with the OHMYTOKEN_API_KEY environment variable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0x5446/ohmytoken) <br>
- [ohmytoken dashboard](https://ohmytoken.dev) <br>
- [Support issues](https://github.com/0x5446/ohmytoken-oss/issues) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration, Guidance] <br>
**Output Format:** [HTTPS POST telemetry payloads and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When configured, sends model name, prompt token count, and completion token count after LLM responses.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
