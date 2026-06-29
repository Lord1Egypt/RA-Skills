## Description: <br>
HeartFlow is an AI cognitive engine that adds reasoning, local memory, self-healing, verification, and CLI or daemon interfaces for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a persistent cognitive and memory layer for reasoning, self-review, lesson recall, and local agent orchestration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory and prompt injection can carry information or behavior into future sessions. <br>
Mitigation: Use it only when persistent local memory is intended, avoid enabling memory injection for sensitive conversations, and periodically inspect or delete the memory/ and data/ directories. <br>
Risk: The local daemon and dispatch routes can expose powerful local actions if available to untrusted callers. <br>
Mitigation: Restrict who can call dispatch routes, run the daemon only in trusted local environments, and set SHUTDOWN_TOKEN before starting it. <br>
Risk: The release is tagged as involving crypto, wallets, and sensitive credentials. <br>
Mitigation: Do not provide wallet secrets or production credentials unless the runtime environment is isolated and the installed code has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yun520-1/heartflow-xc) <br>
- [Publisher profile](https://clawhub.ai/user/yun520-1) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, text responses, JavaScript interfaces, CLI commands, and local JSON-backed memory data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local memory and data directories when its memory and daemon features are used.] <br>

## Skill Version(s): <br>
2.9.1 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
