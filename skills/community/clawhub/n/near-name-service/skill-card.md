## Description:

Manage NEAR Name Service (.near domains) - check availability, register, resolve, and manage names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaiss](https://clawhub.ai/user/shaiss)

### License/Terms of Use:

MIT

## Use Case:

Developers and NEAR users use this skill to check .near name availability, resolve existing .near names, and register names to a NEAR account from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The registration command can execute unsafe shell input and may trigger blockchain actions without enough safeguards.

Mitigation: Review commands before execution, use trusted NEAR account and name inputs only, and require explicit confirmation before registration.

Risk: The skill can rely on NEAR_ACCOUNT from the environment, which may be untrusted or point to the wrong account.

Mitigation: Set NEAR_ACCOUNT explicitly in a trusted shell session or pass the intended account ID directly when registering a name.

Risk: Testnet and real funded account behavior may be unclear to users.

Mitigation: Confirm the target network and account funding before running registration commands.

## Reference(s):

- [NEAR Name Service](https://near.org/names/)
- [NEAR CLI](https://docs.near.org/tools/near-cli)
- [ClawHub skill page](https://clawhub.ai/shaiss/skills/near-name-service)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Command-line text output with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses NEAR RPC endpoints and the NEAR CLI for name checks, resolution, and registration.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
