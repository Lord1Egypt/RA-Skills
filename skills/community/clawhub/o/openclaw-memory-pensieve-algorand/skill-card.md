## Description:

Long-term episodic memory for OpenClaw with append-only hash-chained local layers, daily dream-cycle consolidation, AES-GCM encrypted Algorand anchoring, and post-anchor recoverability validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pitertxus](https://clawhub.ai/user/pitertxus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to capture episodic memory, consolidate recurring patterns, encrypt daily memory events, anchor them to Algorand, validate recoverability, and recover anchored memory for a selected date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recovery validation can overstate whether memory is truly recoverable from the blockchain.

Mitigation: Do not treat ok=true validation as proof of disaster recovery unless confirmed on-chain retrieval is required and succeeds.

Risk: The local MCP server has access to a wallet mnemonic, an AES encryption key, and OpenClaw memory files.

Mitigation: Use a dedicated low-balance wallet, isolate the workspace and secrets, prefer environment variables, and apply restrictive permissions to any local secret fallback files.

Risk: Unpinned dependencies can change behavior across installs.

Mitigation: Pin and review mcp, algosdk, and cryptography versions before deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pitertxus/skills/openclaw-memory-pensieve-algorand)
- [Architecture](artifact/references/architecture.md)
- [Hardening v2.1 policy](artifact/references/hardening-v21.md)
- [Ops runbook](artifact/references/ops-runbook.md)
- [Security and prerequisites](artifact/references/security-prereqs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON configuration, shell commands, MCP tool calls, MCP tool result JSON, and local JSONL files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write append-only memory JSONL files, recovered JSONL files, local anchor records, and Algorand anchoring transactions when configured with wallet credentials.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
