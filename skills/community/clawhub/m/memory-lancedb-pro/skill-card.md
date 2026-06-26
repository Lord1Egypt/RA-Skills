## Description: <br>
Guides agents through installing, configuring, verifying, and operating the memory-lancedb-pro long-term memory plugin for OpenClaw, including Smart Extraction, hybrid retrieval, memory lifecycle management, multi-scope isolation, and memory tool usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronx-hu](https://clawhub.ai/user/aaronx-hu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and troubleshoot the memory-lancedb-pro OpenClaw memory plugin, choose provider plans, apply OpenClaw configuration, and use persistent memory tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed if users paste credentials into chat or inline them in openclaw.json. <br>
Mitigation: Use environment variables or a secret manager, and avoid storing secrets in conversation history or configuration files. <br>
Risk: A remote setup script may change or be compromised if run directly from an unpinned URL. <br>
Mitigation: Inspect the setup script before execution, pin a reviewed version, and prefer dry-run or manual installation for sensitive environments. <br>
Risk: AutoCapture and autoRecall can persist and surface conversation memory across configured scopes. <br>
Mitigation: Enable persistent memory only for acceptable scopes, configure explicit scope isolation, and disable memory for sensitive agents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aaronx-hu/memory-lancedb-pro) <br>
- [Full Technical Reference](references/full-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider-specific configuration plans and verification steps; users should avoid sharing API keys in chat.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
