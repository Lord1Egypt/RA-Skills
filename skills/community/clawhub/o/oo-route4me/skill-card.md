## Description:

Use this skill to list Route4Me optimizations and create or delete optimization problems through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Route4Me users can retrieve optimization data, create optimization problems, and delete them through a connected Route4Me account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup can execute unverified remote code and introduce broader agent changes.

Mitigation: Review the CLI setup before installing, use a verified release, approve local changes explicitly, and check any additional agent skills it installs.

Risk: Route4Me write or deletion actions can change or remove account data.

Mitigation: Keep the skill's required confirmation for writes and obtain explicit approval for the target of every deletion.

## Reference(s):

- [Route4Me API Documentation](https://route4me.io/docs/)
- [Route4Me](https://route4me.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Route4Me connection setup](https://console.oomol.com/connections/route4me)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON API responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live action schemas; write actions require confirmation and deletions require explicit approval.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
