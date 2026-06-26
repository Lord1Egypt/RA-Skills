## Description: <br>
Long-term episodic memory for OpenClaw with append-only hash-chained local layers, daily dream-cycle consolidation, AES-GCM encrypted Algorand anchoring, and post-anchor recoverability validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pitertxus](https://clawhub.ai/user/pitertxus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to capture episodic memory, consolidate recurring patterns, encrypt daily memory payloads, anchor them to Algorand, validate recoverability, and reconstruct memory for a selected date. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to an Algorand anchoring wallet and an AES note key. <br>
Mitigation: Use a dedicated low-balance wallet, keep secrets in protected environment variables, and avoid reusing a main operations wallet. <br>
Risk: Local fallback secret files can expose wallet or key material if filesystem permissions are weak. <br>
Mitigation: Prefer environment variables; if fallback files are used for local development, secure the .secrets directory and never commit it. <br>
Risk: Encrypted memory written on-chain is effectively permanent if the note key is later exposed. <br>
Mitigation: Protect the AES note key as sensitive long-term material and anchor only encrypted payloads. <br>
Risk: Recovery claims can be misleading if validation fails or is skipped. <br>
Mitigation: Treat pensieve_validate failures as blocking and rely on recovery claims only when validation returns ok=true. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pitertxus/openclaw-memory-pensieve-algorand) <br>
- [Architecture](references/architecture.md) <br>
- [Hardening v2.1 policy](references/hardening-v21.md) <br>
- [Ops runbook](references/ops-runbook.md) <br>
- [Security & prerequisites](references/security-prereqs.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Configuration instructions, Guidance] <br>
**Output Format:** [JSON MCP tool responses, JSONL memory files, and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Anchoring may submit encrypted Algorand transactions when wallet, key, and network configuration are provided.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
