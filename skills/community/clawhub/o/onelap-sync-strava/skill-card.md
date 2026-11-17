## Description:

Guides users through syncing Onelap cycling activities to Strava with the OnelapSyncStrava command-line tool after Onelap's automatic Strava sync was discontinued.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kermit-r-wood](https://clawhub.ai/user/kermit-r-wood)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure credentials, authorize Strava OAuth access, and run OnelapSyncStrava commands that transfer Onelap cycling records to Strava.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users are asked to run an externally obtained OnelapSyncStrava binary.

Mitigation: Install only after verifying the referenced project and the exact binary, or build the tool from reviewed source.

Risk: config.json stores Onelap credentials, Strava API secrets, and OAuth tokens locally.

Mitigation: Keep config.json out of version control and shared folders, restrict file access, and rotate Strava and Onelap credentials if the file or binary is exposed.

## Reference(s):

- [OnelapSyncStrava GitHub Releases](https://github.com/kermit-r-wood/OnelapSyncStrava/releases)
- [OnelapSyncStrava Build Binaries Workflow](https://github.com/kermit-r-wood/OnelapSyncStrava/actions/workflows/binaries.yml)
- [Strava API Settings](https://www.strava.com/settings/api)
- [ClawHub Skill Page](https://clawhub.ai/kermit-r-wood/skills/onelap-sync-strava)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands and configuration field names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local config.json fields and OnelapSyncStrava command invocations.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
