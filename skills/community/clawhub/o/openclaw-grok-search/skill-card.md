## Description: <br>
Cross-platform real-time web research and search via an OpenAI-compatible Grok endpoint, returning JSON with content and sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moxunjinmu](https://clawhub.ai/user/moxunjinmu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform current web research, verify versions and documentation, troubleshoot issues, and return concise source-backed results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled config includes a third-party endpoint and live-looking API key that users may unintentionally use. <br>
Mitigation: Review config.json before use, remove the bundled key and endpoint, and configure a trusted endpoint through environment variables or config.local.json. <br>
Risk: Search queries are sent to the configured external endpoint and may expose sensitive project details. <br>
Mitigation: Do not submit private code, credentials, logs, regulated data, or confidential business information in search queries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/moxunjinmu/openclaw-grok-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON object with ok, content, sources, raw, and related request metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search requests are sent to the configured OpenAI-compatible Grok endpoint and may include user query text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
