## Description:

Brandfetch (brandfetch.com). Use this skill for ANY Brandfetch request — searching and reading data. Whenever a task involves Brandfetch, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search for Brandfetch brand profiles and resolve transaction labels to merchant profiles through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup path downloads and runs a CLI installer, and the downloaded installer and runtime behavior have not been verified.

Mitigation: Review the CLI installation separately and prefer a verified, pinned release before using the setup fallback.

Risk: The CLI may synchronize changes to other installed agent skills at startup.

Mitigation: Review and approve any skill changes; consider setting OO_SKILLS_SYNC_DISABLED=1 as documented in the oo CLI command reference.

Risk: Resolving transaction labels sends those labels through OOMOL.

Mitigation: Submit only transaction labels you are comfortable sharing through OOMOL.

## Reference(s):

- [Brandfetch](https://brandfetch.com)
- [Brandfetch API documentation](https://docs.brandfetch.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference: environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Brandfetch ClawHub release](https://clawhub.ai/oomol/skills/oo-brandfetch)

## Skill Output:

**Output Type(s):** [API Calls, JSON data, Text summaries]

**Output Format:** [Brand profile data returned as JSON, with optional natural-language summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected Brandfetch account; credentials are not included in the skill's output.]

## Skill Version(s):

1.0.6 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
