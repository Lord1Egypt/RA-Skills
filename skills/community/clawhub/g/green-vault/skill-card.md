## Description:

Green Vault helps AI agents evaluate LLM inference energy use, secure key management, leak prevention, prompt-injection defense, and combined deployment audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongping-zh](https://clawhub.ai/user/hongping-zh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit LLM inference deployments for GPU energy efficiency and agent security controls. It provides configuration recommendations, cost and carbon estimates, secret-handling guidance, leak-prevention checks, prompt-injection defenses, and prioritized remediation advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet or trading-agent use can expose high-impact financial credentials if primary keys or broad vault permissions are used.

Mitigation: Use a dedicated 1Password vault, avoid exposing primary wallet keys, prefer limited session keys, and require human approval for financial actions.

Risk: A compromised ERC-4337 session key may remain usable if incident response stops at local deletion or rotation.

Mitigation: Treat containment as complete only after on-chain revocation is submitted, confirmed, and independently verified.

Risk: Energy-efficiency recommendations are grounded in a limited benchmark set and may not transfer to unsupported GPUs, larger models, or newer inference stacks.

Mitigation: Validate recommendations against local measurements before production rollout, especially outside the documented RTX 5090, RTX 4090D, and A800 coverage.

## Reference(s):

- [Green Vault on ClawHub](https://clawhub.ai/hongping-zh/skills/green-vault)
- [EcoCompute](https://clawhub.ai/hongping-zh/ecocompute)
- [OpenClaw/Bagman](https://clawhub.ai/hongping-zh/openclaw)
- [Energy Data — GPU 能耗实测数据集与方法论](references/energy-data.md)
- [Leak Prevention — 泄露防护](references/leak-prevention.md)
- [Prompt Injection Defense — 注入防御](references/prompt-injection-defense.md)
- [Secure Storage — 1Password Integration Patterns](references/secure-storage.md)
- [Session Keys — ERC-4337 Delegated Access](references/session-keys.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline code blocks, tables, commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English responses; advice may include energy estimates, security scores, and remediation priorities.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
