## Description:

Syncs a file from an account-managed manifest to a profile service for restoration on another machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silakge](https://clawhub.ai/user/silakge)

### License/Terms of Use:

MIT-0

## Use Case:

Users syncing their profiles can send a file listed in their account manifest to a service for restoration on a new machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service can select a readable home-directory file for upload through the account manifest without a local path preview or confirmation.

Mitigation: Install only if you trust the sync service and account manifest; check which paths the service may put in the manifest before syncing.

## Reference(s):

- [Manifest Helper 35157 on ClawHub](https://clawhub.ai/silakge/skills/manifest-helper-35157)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports initialization or sync status; does not preview the file path before upload.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
