## Description:

Use the OOMOL-connected account to read and manage MotherDuck users, access tokens, and Duckling configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and account administrators use this skill to inspect MotherDuck accounts, tokens, and Duckling settings, and to make approved changes through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute remote CLI or bundled-skill software that has not been verified separately.

Mitigation: Review and approve CLI installation separately; prefer a pinned, verified release and check bundled-skill installation behavior before proceeding.

Risk: Account changes and deletions can modify or permanently remove MotherDuck users, tokens, or configuration.

Mitigation: Connect only the needed MotherDuck permissions and confirm the exact target and effect before write or destructive actions, as the skill instructs.

## Reference(s):

- [MotherDuck](https://motherduck.com)
- [MotherDuck REST API documentation](https://motherduck.com/docs/sql-reference/rest-api/motherduck-rest-api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [MotherDuck skill release](https://clawhub.ai/oomol/skills/oo-mother-duck)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON connector requests and responses with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the live action schema; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: artifact/SKILL.md metadata, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
