## Description: <br>
HeartFlow 心虫 is a cognitive engine for agent reasoning, three-layer memory, self-healing feedback, judgment checks, and reflective guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mark-heartflow](https://clawhub.ai/user/mark-heartflow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add a local cognitive layer for structured reasoning, persistent memory, reflection, verification, and self-improvement workflows. It is intended for agents that need text guidance, code-facing interfaces, local memory operations, and command-line tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad persistent memory and prompt injection behavior can retain or surface sensitive conversation content. <br>
Mitigation: Avoid storing secrets or sensitive conversations, review memory files regularly, and restrict memory injection to trusted local workspaces. <br>
Risk: Daemon, socket, network-capable verification, and local code execution capabilities increase local execution and data exposure risk. <br>
Mitigation: Disable or remove daemon, socket, verification, code execution, and self-initiator routes unless they are required for a reviewed deployment. <br>
Risk: Security evidence flags the release as suspicious because the packaged behavior is broader than the stated purpose. <br>
Mitigation: Install only when a broad local cognitive layer is intended, scan the package before deployment, and apply least-privilege filesystem and runtime controls. <br>
Risk: Crisis-handling behavior may include an unsafe self-harm silence path. <br>
Mitigation: Do not rely on this skill for crisis handling without review and remediation of the self-harm silence behavior. <br>
Risk: The release is tagged as requiring wallet and sensitive credentials capabilities. <br>
Mitigation: Do not provide wallet material, credentials, API keys, or other secrets unless the specific route has been reviewed and isolated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mark-heartflow/heartflow-v1) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>
- [audit-zombie.js](artifact/references/audit-zombie.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples; runtime interfaces may return text, JSON memory records, and status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local memory read/write behavior, daemon and CLI flows, and code-facing reasoning interfaces.] <br>

## Skill Version(s): <br>
2.9.0 (source: frontmatter, package.json, changelog, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
