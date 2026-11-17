## Description:

Use Wachete to read, create, update, and delete monitoring data through a connected Wachete account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Wachete account can retrieve monitors, folders, check history, and notifications, or create, replace, and delete monitors through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses downloaded CLI installation scripts whose behavior has not been verified.

Mitigation: Review and approve the CLI installation separately before running it.

Risk: Automatic skill synchronization can make lasting changes to other agents' skills.

Mitigation: Consider disabling automatic synchronization and inspect changes before allowing them.

Risk: Connecting Wachete gives OOMOL access to the account's credentials and data.

Mitigation: Connect Wachete only if you trust OOMOL with that account's credentials and data.

Risk: Monitor deletion and replacement can remove or overwrite data.

Mitigation: Require approval for the specific monitor and intended deletion or replacement before running the action.

## Reference(s):

- [Wachete](https://www.wachete.com)
- [Wachete API documentation](https://www.wachete.com/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Wachete ClawHub release](https://clawhub.ai/oomol/skills/oo-wachete)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with oo CLI commands and JSON payload examples; action results are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Wachete action.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
