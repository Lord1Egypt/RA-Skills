## Description:

Nutrient DWS (nutrient.io). Use this skill for ANY Nutrient DWS request — reading, creating, updating, and deleting data. Whenever a task involves Nutrient DWS, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect Nutrient DWS action schemas and operate a connected account for account information, build analysis, and authentication token management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run changing remote installer or CLI code and startup synchronization may add persistent agent skills.

Mitigation: Review setup behavior, install a reviewed pinned CLI yourself, and set OO_SKILLS_SYNC_DISABLED=1 if startup skill synchronization is unwanted.

Risk: Connecting Nutrient DWS gives OOMOL access to the provider account.

Mitigation: Retain the required approvals and use restricted, short-lived tokens where possible.

## Reference(s):

- [Nutrient DWS API](https://www.nutrient.io/api/)
- [Nutrient DWS Processor Guide](https://www.nutrient.io/guides/dws-processor/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with shell command and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads should follow the live connector schema.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
