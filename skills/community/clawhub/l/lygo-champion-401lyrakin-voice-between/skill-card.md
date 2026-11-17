## Description:

DEPRECATED slug - use lygo-champion-council. Legacy champion persona helper for 401LYRAKIN.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this legacy persona helper to translate alignment and continuity ideas into portable bootlines, identity anchors, vows, and verification hashes. New installs should use the successor skill lygo-champion-council.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deprecated skill recommends an unpinned npx clawhub@latest migration command that can change installed agent behavior.

Mitigation: Do not run the migration command unattended; use a pinned, verified installer version and review the successor skill before installation.

Risk: The referenced verifier can be used in workflows that write ledgers or publish public anchors.

Mitigation: Review the LYGO-MINT verifier behavior and require human approval before ledger writes or public anchor publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-champion-401lyrakin-voice-between)
- [LYGO-MINT verifier](https://clawhub.ai/DeepSeekOracle/lygo-mint-verifier)
- [persona_pack.md](references/persona_pack.md)
- [canon.json](references/canon.json)
- [verifier_usage.md](references/verifier_usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline commands and hash or anchor snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output only; users should separate observed, inferred, and unknown claims when factual stakes are high.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
