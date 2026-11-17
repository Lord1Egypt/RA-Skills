## Description:

Teach agents to register pages into the LYGO Pure-Data lattice via a public register portal and safety-gated CLI, producing digests, optional witness fragments, ledgers, Continuum claims, and Star Chart submission JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to archive public URLs or local files as Pure-Data Witness records after human consent. It guides portal-based registration, creates local digest artifacts, and prepares Star Chart submission files without silently publishing live chart changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL-fetch safety claims are stronger than the scanner says the code enforces.

Mitigation: Use URL fetching only for trusted public HTTPS URLs, keep network access off unless explicitly authorized, and do not archive private dashboards, credentials, cookies, API keys, or internal network resources.

Risk: The install command may run a mutable remote package.

Mitigation: Prefer a pinned installer version and run installation or first use in a low-privilege environment.

Risk: Local export packs may contain redacted snapshots, and redaction is incomplete by nature.

Mitigation: Review every generated export file before sharing it with Hugging Face or any third party.

Risk: The skill can produce persistent local artifacts such as ledgers, witness cards, and Star Chart submission files.

Mitigation: Use the consent flags for register, fetch, all, and export flows, and treat Star Chart submissions as proposals requiring steward review before live publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-pure-data-witness)
- [ClawHub Release Page](https://clawhub.ai/deepseekoracle/lygo-pure-data-witness)
- [GitHub Homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/clawhub/mirrors/lygo-pure-data-witness)
- [Register Portal](https://deepseekoracle.github.io/lygo-protocol-stack/data-vault/register.html)
- [Pure-Data UI](https://deepseekoracle.github.io/lygo-protocol-stack/data-vault/pure-data.html)
- [ClawHub Security Audit](https://clawhub.ai/deepseekoracle/skills/lygo-pure-data-witness/security-audit)
- [PORTAL_TRAINING.md](references/PORTAL_TRAINING.md)
- [SECURITY.md](references/SECURITY.md)
- [SKILLSPECTOR_AUDIT.md](references/SKILLSPECTOR_AUDIT.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, json, markdown]

**Output Format:** [Markdown guidance with shell commands and JSON artifact paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local witness cards, optional text snapshots, egg fragments, ledgers, Continuum claims, and Star Chart submission JSON under operator-selected output paths.]

## Skill Version(s):

1.3.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
