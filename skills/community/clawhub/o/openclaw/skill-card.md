## Description: <br>
Secure key management for AI agents handling private keys, API secrets, wallet credentials, and agent-controlled funds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zscole](https://clawhub.ai/user/zscole) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design agent workflows that access private keys, API secrets, wallet credentials, and on-chain funds with reduced leakage and prompt-injection risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet, session-key, environment-variable, and git history-rewrite snippets can cause loss of funds, credential exposure, or repository disruption if copied without adaptation. <br>
Mitigation: Adapt snippets in a test environment first, use test funds, short-lived least-privilege credentials, human approval for transfers, monitoring, and coordinated incident-response procedures. <br>
Risk: The skill discusses agent access to private keys, API secrets, wallet credentials, and on-chain funds, which are high-impact assets if exposed or misused. <br>
Mitigation: Use delegated session keys instead of master keys, retrieve secrets at runtime through 1Password CLI, sanitize outputs, and isolate wallet operations from conversation context. <br>


## Reference(s): <br>
- [Openclaw ClawHub listing](https://clawhub.ai/zscole/openclaw) <br>
- [Publisher profile](https://clawhub.ai/user/zscole) <br>
- [Secure Storage Patterns for Agent Secrets](references/secure-storage.md) <br>
- [Session Keys for Agent Wallet Access](references/session-keys.md) <br>
- [Leak Prevention for Agent Secrets](references/leak-prevention.md) <br>
- [Prompt Injection Defense for Agent Key Operations](references/prompt-injection-defense.md) <br>
- [Project homepage](https://numbergroup.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance requiring the 1Password CLI for the primary secure-storage workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
