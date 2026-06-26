## Description: <br>
AI Agent 安全与绿色运维顾问，combining GPU energy optimization for LLM inference with secure key management, leak prevention, and prompt-injection defense guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongping-zh](https://clawhub.ai/user/hongping-zh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to review LLM inference deployments for GPU energy efficiency, expected operating cost, secret handling, wallet session-key design, leak prevention, and prompt-injection defenses. It is advisory and produces prioritized recommendations plus executable examples for the operator to review before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential, wallet, deletion, and hook-installation snippets could affect sensitive systems if run without checking local vaults and item names. <br>
Mitigation: Confirm vault and item names before running snippets, prefer limited session keys over master private keys, and keep human approval in the execution path. <br>
Risk: Secret-management examples can expose sensitive values if operators print, log, or persist retrieved credentials. <br>
Mitigation: Route secrets through a dedicated manager at runtime, avoid logging retrieved values, and apply output sanitization before responses are sent. <br>
Risk: Energy recommendations are based on the skill's stated measurement coverage and may not generalize to unmeasured GPUs, model sizes, sequence lengths, or library versions. <br>
Mitigation: Treat recommendations as starting points and validate with local measurements before production rollout. <br>


## Reference(s): <br>
- [Green Vault ClawHub release](https://clawhub.ai/hongping-zh/green-vault) <br>
- [EcoCompute](https://clawhub.ai/hongping-zh/ecocompute) <br>
- [OpenClaw/Bagman](https://clawhub.ai/hongping-zh/openclaw) <br>
- [Energy Data — GPU 能耗实测数据集与方法论](references/energy-data.md) <br>
- [Secure Storage — 1Password Integration Patterns](references/secure-storage.md) <br>
- [Session Keys — ERC-4337 Delegated Access](references/session-keys.md) <br>
- [Leak Prevention — 泄露防护](references/leak-prevention.md) <br>
- [Prompt Injection Defense — 注入防御](references/prompt-injection-defense.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with tables and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include energy and cost estimates, security findings, prioritized remediation steps, and snippets that require operator review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
