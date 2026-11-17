## Description:

Operate X (Twitter) through an OOMOL-connected account to read, search, create, update, and delete account data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search X and manage an authorized account through OOMOL, including posts, lists, profiles, and direct messages. Account-changing actions should be reviewed with the user before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Two account-changing actions bypass the skill's stated confirmation rules.

Mitigation: Require approval for every account change, including hiding replies and pinning lists.

Risk: Setup runs remote installers, and the hosted connector implementation was not verified.

Mitigation: Install a reviewed, verified CLI version and review or disable its automatic agent-skill synchronization.

Risk: Connecting X gives the OOMOL integration access to authorized account data, including private messages.

Mitigation: Review and authorize the account connection and its data access before use.

## Reference(s):

- [X API introduction](https://docs.x.com/x-api/introduction)
- [X](https://x.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector requests and responses, with shell command instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available actions include read operations and account changes; write actions require confirmation and destructive actions require explicit approval.]

## Skill Version(s):

1.0.7 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
