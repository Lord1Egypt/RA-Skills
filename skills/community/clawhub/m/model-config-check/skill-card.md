## Description: <br>
Checks OpenClaw model provider configuration, connectivity, authentication, and model responses, and can help configure a provider when given a model name and API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonzhang2015](https://clawhub.ai/user/jasonzhang2015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to validate OpenClaw model provider settings after configuration changes or updates. It reports whether configured providers and models are reachable, authenticated, and returning usable content, with troubleshooting guidance for failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify OpenClaw model provider settings and restart the gateway. <br>
Mitigation: Review planned configuration changes, confirm provider base URLs, and keep a backup or rollback path before applying changes. <br>
Risk: The skill can store API keys and send live authenticated requests to configured model endpoints, which may consume quota. <br>
Mitigation: Use limited-scope or disposable API keys where possible, and confirm live test calls are acceptable for the target account. <br>
Risk: The security scan verdict is suspicious because automatic diagnostics may run without a clear consent gate. <br>
Mitigation: Install only where automatic model diagnostics are expected, and require operator approval for configuration changes and live calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jasonzhang2015/model-config-check) <br>
- [Publisher profile](https://clawhub.ai/user/jasonzhang2015) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with shell command results and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute live provider connectivity and model response checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
