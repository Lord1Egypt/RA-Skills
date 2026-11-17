## Description:

Creates a local Git bundle backup of the OpenClaw workspace repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trumppo](https://clawhub.ai/user/trumppo)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create a local Git bundle containing the workspace repository history and refs, then report the generated bundle path and size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The created Git bundle may include private code, branches, tags, and previously committed secrets.

Mitigation: Treat bundle files as sensitive artifacts and restrict, rotate, or delete them according to retention requirements.

Risk: Older backup bundles are not deleted automatically.

Mitigation: Monitor the backup directory and remove obsolete bundles when storage or retention limits apply.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text status output with a local bundle path and size.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local Git bundle file under /root/.openclaw/backups; older bundles are not deleted.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
