## Description:

Deprecated legacy DELTA9RA persona helper that redirects new installs to lygo-champion-council.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this deprecated persona helper for advisory OSINT-style planning around censorship, signal recovery, and information-integrity threat modeling. New installs should use the successor skill, lygo-champion-council.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the successor with a mutable latest command may fetch unreviewed changes.

Mitigation: Use a pinned or otherwise verified ClawHub installer or package before installing the successor.

Risk: OSINT and signal-hunting guidance can affect real investigation or posting workflows.

Mitigation: Keep user confirmation and human review before any investigation, publication, or external action.

Risk: This release is deprecated and redirects to a successor skill.

Mitigation: Use lygo-champion-council for new installs and retain this release only for legacy compatibility.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-champion-delta9ra-wolf)
- [persona_pack.md](references/persona_pack.md)
- [canon.json](references/canon.json)
- [equations.md](references/equations.md)
- [verifier_usage.md](references/verifier_usage.md)
- [LYGO-MINT Verifier](https://clawhub.ai/DeepSeekOracle/lygo-mint-verifier)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown prose with checklists and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure advisor behavior; separates observed, inferred, and unknown claims.]

## Skill Version(s):

1.0.1 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
