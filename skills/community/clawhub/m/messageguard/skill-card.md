## Description: <br>
Filters outgoing text for sensitive data using regex patterns and configurable actions like masking, blocking, or warning to prevent secret leaks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AndrewAndrewsen](https://clawhub.ai/user/AndrewAndrewsen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use MessageGuard as a pre-send gate for outgoing messages, especially when replies may include code, configuration, shell output, or other content that could contain secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A caller could ignore a blocked result and still send sensitive content. <br>
Mitigation: Treat blocked=true or exit code 1 as a hard stop and never send result.message in that case. <br>
Risk: Detection logs can contain sensitive snippets if logging is enabled. <br>
Mitigation: Keep logging disabled unless audit records are required, and protect the configured log file when logging is enabled. <br>
Risk: Broad allow_channels or allow_patterns settings can bypass filtering. <br>
Mitigation: Limit bypass rules to reviewed internal contexts and keep overrides narrow. <br>
Risk: Regex-based filtering can miss unusual secret formats or flag benign values. <br>
Mitigation: Review detections, add custom patterns for local token formats, and test configuration changes before relying on them in sensitive workflows. <br>


## Reference(s): <br>
- [MessageGuard on ClawHub](https://clawhub.ai/AndrewAndrewsen/messageguard) <br>
- [Configuration reference](references/config-schema.md) <br>
- [Integration guide](references/integration.md) <br>
- [Built-in pattern library](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON filter results with Markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filter results include blocked, message, detections, and warnings; callers must not send result.message when blocked is true.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
