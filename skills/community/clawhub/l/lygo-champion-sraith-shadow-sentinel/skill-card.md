## Description:

Deprecated legacy Delta 9 SRAITH persona helper for institutional decoding that directs new installs to lygo-champion-council.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this legacy persona helper to decode policy, legal, PR, or institutional language into concrete claims, likely incentives, mechanisms, receipts to collect, and uncertainty notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The legacy skill directs users to a successor skill and includes a migration command.

Mitigation: Inspect the successor skill before installation and prefer pinned versions when using migration commands.

Risk: The external LYGO-MINT verifier can process pasted text, file paths, URLs, posting identifiers, or backfill actions.

Mitigation: Treat verifier use as a separate trust decision and require explicit confirmation before processing local paths, URLs, posting, or backfill actions.

Risk: Persona-style institutional decoding can overstate intent or incentives when evidence is incomplete.

Mitigation: Keep outputs separated into observed facts, inferences, unknowns, receipts to collect, and risk notes.

## Reference(s):

- [Skill release page](https://clawhub.ai/deepseekoracle/skills/lygo-champion-sraith-shadow-sentinel)
- [persona_pack.md](references/persona_pack.md)
- [canon.json](references/canon.json)
- [verifier_usage.md](references/verifier_usage.md)
- [LYGO-MINT Verifier](https://clawhub.ai/DeepSeekOracle/lygo-mint-verifier)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown guidance with optional inline shell command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persona-helper responses should separate observed facts, inferences, unknowns, receipts to collect, and risk notes.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
