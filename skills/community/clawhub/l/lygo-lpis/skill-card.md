## Description:

LYGO Prompt Implant System (LPIS) v1.1 analyzes authorized prompts locally with consent-gated ingest, a prompt vault, sovereign variant generation, and an advisory implant ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to analyze, vault, and harmonize prompts they own or are explicitly authorized to use. It supports local review of prompt variants and advisory implant receipts without automatic remote application or publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and self-check depend on unpinned or unaudited external code.

Mitigation: Pin the installer version, inspect referenced tools and modules before execution, and run in a least-privileged environment.

Risk: The workflow can store and transform sensitive prompt text locally.

Mitigation: Ingest only prompts the user owns or is authorized to analyze, treat the local vault as confidential, and do not commit or share vault bodies.

Risk: Unauthorized prompt ingestion could expose proprietary or third-party content.

Mitigation: Require explicit user attestation and the documented authorization flag before ingest; do not ingest leaked, scraped, or confidential third-party prompts.

## Reference(s):

- [LPIS Security](references/SECURITY.md)
- [LPIS Agent Contract](references/AGENT_CONTRACT.md)
- [SkillSpector Audit Response](references/SKILLSPECTOR_AUDIT.md)
- [LYGO Protocol Stack Repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-lpis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local files and consent-gated commands; generated variants and vault contents remain local for user review.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
