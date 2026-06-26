## Description: <br>
Integrates AIN providers into OpenClaw with intelligent model routing and tools for prompt execution and task classification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felipematos](https://clawhub.ai/user/felipematos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this OpenClaw plugin to expose AIN-configured model providers, execute prompts through AIN, classify tasks, and optionally route model selection according to AIN policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be routed through any configured AIN provider when routing or tools are enabled. <br>
Mitigation: Review configured AIN providers before enabling the plugin, and disable enableRouting or exposeTools when automatic routing or tool access is not needed. <br>
Risk: The documented configPath scoping option is not honored in the artifact behavior reflected by the security guidance. <br>
Mitigation: Do not rely on configPath to constrain provider or credential use until that behavior is fixed or independently confirmed. <br>
Risk: Runtime behavior depends on the third-party @felipematos/ain-cli dependency. <br>
Mitigation: Install only in environments where the dependency and AIN configuration are trusted and reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/felipematos/openclaw-plugin-ain) <br>
- [AIN project](https://github.com/felipematos/ain) <br>
- [@felipematos/ain-cli package](https://www.npmjs.com/package/@felipematos/ain-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, configuration, guidance] <br>
**Output Format:** [OpenClaw provider responses and tool results, including text responses and JSON objects for execution, usage, parsed output, task type, and complexity.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on configured AIN providers, selected model, routing policy, prompt, optional JSON mode, optional schema, system prompt, and temperature.] <br>

## Skill Version(s): <br>
0.11.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
