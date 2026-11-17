## Description:

LYGO Emotional RAM is a local Python skill that converts text scenarios into affective and ethical indices, grace damping values, UMP recommendations, consent-gated memory records, and swarm aggregates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to summarize text scenarios as lightweight affective and ethical signals for agent memory, recall, and multi-agent aggregate workflows. It is suited for local analysis where humans remain responsible for consent, interpretation, and downstream decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indexing creates a local memory file that may preserve sensitive labels, hashes, vectors, or opt-in plaintext.

Mitigation: Use indexing only with explicit consent, avoid secrets, API keys, PHI, and private material, and use --store-plaintext only on a private host.

Risk: The skill's outputs are lightweight indices and may be mistaken for clinical emotion detection or evidence of sentience.

Mitigation: Treat outputs as decision-support signals only and keep human review responsible for interpretation and downstream action.

Risk: Recall or swarm summaries can expose sensitive context if built from private source text.

Mitigation: Prefer summaries for sharing, keep state files under operator control, and avoid indexing private material that should not persist.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-emotional-ram)
- [ClawHub Release Listing](https://clawhub.ai/deepseekoracle/lygo-emotional-ram)
- [LYGO Emotional RAM Whitepaper](https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/whitepapers/LYGO_EMOTIONAL_RAM_v1.md)
- [Security Notes](references/SECURITY.md)
- [SkillSpector Audit Notes](references/SKILLSPECTOR_AUDIT.md)
- [Quickstart](examples/quickstart.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown instructions with CLI commands; CLI output is JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only operation; index writes require explicit consent and default to hash, label, and vectors rather than plaintext.]

## Skill Version(s):

1.0.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
