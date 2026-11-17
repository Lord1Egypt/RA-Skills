## Description:

Search Podscribe data and retrieve integration health, show details, and episode information through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to check Podscribe integration health, retrieve show information, and search podcast episodes through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute downloaded code without a clear user approval step and can make persistent changes.

Mitigation: Review and approve CLI setup separately, prefer a verified pinned release, and check or disable automatic installation of additional agent skills.

## Reference(s):

- [Podscribe](https://podscribe.com)
- [Podscribe API Documentation](https://docs.api.podscribe.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-podscribe)

## Skill Output:

**Output Type(s):** [API data, JSON, Guidance]

**Output Format:** [JSON responses with concise natural-language summaries and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned data depends on the requested Podscribe health, show, or episode query.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
