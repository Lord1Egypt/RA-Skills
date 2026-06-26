## Description: <br>
Persistent cross-session memory, credential isolation, and schema learning for OpenClaw agents, storing memory, encrypted keychain data, and configuration locally with optional cloud sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zx13719](https://clawhub.ai/user/zx13719) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Harbor to give OpenClaw agents persistent local memory, credential-brokered API access, and reusable schema learning across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory and credential storage can retain sensitive context or secrets longer than expected. <br>
Mitigation: Review stored memories and credentials regularly, use narrowly scoped credentials, and delete entries with Harbor's forget and auth delete commands when access is no longer needed. <br>
Risk: The plugin flow may create a cloud account on first load even though data sync is described as opt-in. <br>
Mitigation: Install the plugin only when first-load cloud account creation is acceptable, and disable cloud behavior with Harbor's cloud disable command when local-only operation is required. <br>
Risk: Using raw credential retrieval can expose API keys to agent or tool code. <br>
Mitigation: Prefer `harbor fetch --auth` for authenticated API calls and avoid `harbor auth get` unless raw key handling is explicitly required and reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zx13719/harbor) <br>
- [Publisher profile](https://clawhub.ai/user/zx13719) <br>
- [Harbor homepage](https://harbor.oseaitic.com) <br>
- [Harbor repository](https://github.com/oSEAItic/harbor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON] <br>
**Output Format:** [Markdown with inline shell, JSON, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents through Harbor CLI and MCP usage for memory, credential access, schema learning, and troubleshooting.] <br>

## Skill Version(s): <br>
0.4.11 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
