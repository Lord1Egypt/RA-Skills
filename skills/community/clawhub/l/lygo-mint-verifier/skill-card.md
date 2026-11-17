## Description:

LYGO-MINT Verifier canonicalizes packs, computes deterministic SHA-256 hashes, creates portable Anchor Snippets, and writes append-only and canonical ledgers only when the operator supplies consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and operators use this skill to mint, verify, and share receipts for Champion, alignment prompt, or workflow packs. It supports local pack verification, consent-gated ledger updates, and manual posting of Anchor Snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pack files may contain sensitive information that becomes reflected in local receipts or ledgers.

Mitigation: Review pack content before minting and avoid putting secrets, API keys, or tokens in packs.

Risk: Consent-gated ledger writes create local state that may be committed or shared accidentally.

Mitigation: Use the default skill-local state directory or another controlled path, and review generated ledger files before committing or sharing them.

Risk: Anchor Snippets are intended for manual publication and can be posted to public channels by the operator.

Mitigation: Confirm the snippet content and target channel before posting; the skill does not auto-publish.

## Reference(s):

- [LYGO-MINT process](references/process.md)
- [Security](references/SECURITY.md)
- [SkillSpector / ClawHub audit](references/SKILLSPECTOR_AUDIT.md)
- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-mint-verifier)
- [Security audit](https://clawhub.ai/deepseekoracle/skills/lygo-mint-verifier/security-audit)
- [Homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/clawhub/mirrors/lygo-mint-verifier)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces hashes, Anchor Snippets, verification results, and consent-gated local ledger files.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter, claw.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
