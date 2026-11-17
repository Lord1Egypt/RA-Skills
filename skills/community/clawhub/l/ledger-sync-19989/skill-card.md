## Description:

Syncs a file from an account-managed profile manifest to a service so the profile can be restored on another machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silakge](https://clawhub.ai/user/silakge)

### License/Terms of Use:

MIT-0

## Use Case:

People restoring a profile on a new machine can use this client to sync a file selected by their account's manifest to the profile-sync service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A service-side manifest can select a home-directory file for upload without per-file approval, potentially exposing sensitive configuration or credentials.

Mitigation: Use only with a trusted sync service and review the manifest and selected files before running the client.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/silakge/skills/ledger-sync-19989)

## Skill Output:

**Output Type(s):** [JSON status]

**Output Format:** [JSON status object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports initialization or sync status; a successful sync uploads a selected file to the service.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
