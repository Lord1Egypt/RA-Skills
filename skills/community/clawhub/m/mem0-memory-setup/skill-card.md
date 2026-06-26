## Description: <br>
Configures a Mem0 external memory layer for Hermes Agent, including package installation, Agent Mode registration, API key setup, Hermes provider configuration, verification, account claiming, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[publieople](https://clawhub.ai/user/publieople) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect Hermes Agent to Mem0 cloud memory for persistent cross-session memory, semantic search, and troubleshooting of common installation or shell environment issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mem0 API keys may be exposed through chat, logs, shell history, or committed configuration files. <br>
Mitigation: Avoid pasting the key into chat or logs, restrict permissions on ~/.mem0/config.json and ~/.hermes/.env, and do not commit those files. <br>
Risk: Hermes will use Mem0 cloud memory after setup, so user facts may be stored outside the local agent environment. <br>
Mitigation: Install only when Mem0 cloud memory is intended; review account claiming and memory-management steps, or use the documented self-hosted option when appropriate. <br>
Risk: Changing npm prefix and PATH can affect where global npm packages are installed and resolved. <br>
Mitigation: Review the npm prefix and shell PATH changes before applying them, especially on systems with existing global npm tooling. <br>


## Reference(s): <br>
- [Mem0 Documentation](https://docs.mem0.ai) <br>
- [Hermes Memory Providers Documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers) <br>
- [Mem0 GitHub Repository](https://github.com/mem0ai/mem0) <br>
- [Mem0 Self-Hosted Documentation](https://docs.mem0.ai/open-source/overview) <br>
- [ClawHub Skill Page](https://clawhub.ai/publieople/mem0-memory-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guide with inline shell commands, configuration snippets, and troubleshooting notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credential setup guidance for MEM0_API_KEY and shell PATH configuration steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
