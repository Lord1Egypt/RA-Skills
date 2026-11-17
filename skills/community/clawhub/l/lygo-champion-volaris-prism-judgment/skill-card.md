## Description:

Deprecated legacy VOLARIS persona helper for advisory evaluation of branching choices; use lygo-champion-council for new installs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this deprecated persona helper to frame advisory analysis of branch points, compare truth and distortion signals, and request receipts-first recommendations. New installs should use the successor skill lygo-champion-council.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deprecated skill documentation includes an unpinned `npx clawhub@latest` migration command for installing the successor skill.

Mitigation: Review the successor skill and prefer a pinned package version or review-before-install workflow before running the command.

Risk: Persona guidance can sound decisive even when it is advisory and evidence is incomplete.

Mitigation: Keep the skill's Observed, Inferred, and Unknown separation and require receipts-first analysis for high-stakes decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-champion-volaris-prism-judgment)
- [persona_pack.md](references/persona_pack.md)
- [canon.json](references/canon.json)
- [equations.md](references/equations.md)
- [verifier_usage.md](references/verifier_usage.md)
- [LYGO-MINT Verifier](https://clawhub.ai/DeepSeekOracle/lygo-mint-verifier)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Shell commands]

**Output Format:** [Markdown advisory responses with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure-advisor persona behavior; no automatic actions.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
