## Description:

Vincario (vincario.com). Use this skill for ANY Vincario request — searching and reading data. Whenever a task involves Vincario, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and vehicle support teams use the skill to query Vincario for VIN decoding, stolen-vehicle checks, market value estimates, available decode fields, and account credit balances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded CLI installer code that has not been verified.

Mitigation: Review and pin the CLI installation source and version before installing.

Risk: The oo CLI may install additional agent skills during startup.

Mitigation: Review any skill installation changes; set OO_SKILLS_SYNC_DISABLED=1 before invoking oo to prevent startup skill writes.

Risk: VIN queries pass through OOMOL and may use Vincario credits.

Mitigation: Connect only the intended Vincario account, send only intended VINs, and check credit costs.

## Reference(s):

- [Vincario](https://vincario.com/)
- [Vincario API documentation](https://vincario.com/api-docs/3.2/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://raw.githubusercontent.com/oomol-lab/oo-cli/main/docs/commands.md)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-vincario)

## Skill Output:

**Output Type(s):** [Text, JSON, Vehicle data, Account information]

**Output Format:** [Structured JSON responses with concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [VIN lookup results depend on the connected Vincario account; queries may consume service credits.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
