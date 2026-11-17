## Description:

Use Langbase to read, create, update, and delete data through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage Langbase memories through their connected account, including retrieving information and creating or deleting memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute changing remote code and introduce broader changes to agent skills.

Mitigation: Review dependency setup, prefer a reviewed CLI release, and set OO_SKILLS_SYNC_DISABLED=1 if startup skill synchronization is unwanted.

Risk: The connected account can be used to change or delete Langbase data.

Mitigation: Use appropriately scoped credentials and retain the skill's user approval requirements for writes and explicit approval for deletions.

## Reference(s):

- [Langbase API documentation](https://langbase.com/docs/api-reference)
- [Langbase](https://langbase.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action results with concise task guidance and oo CLI shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs follow the live connector schema; writes require user confirmation and deletions require explicit approval.]

## Skill Version(s):

1.0.5 (source: release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
