## Description:

Pilot Sync provides command workflows for synchronizing files between agents over the Pilot Protocol network, including directory watching and manifest-based conflict detection examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and agent operators use this skill to propose Pilot Protocol command workflows for syncing files between controlled local directories and trusted remote peers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The file-sync examples can affect local files and remote peers, and evidence.security recommends review before installing or using.

Mitigation: Review the generated commands before execution and run them only against tightly controlled directories and trusted remote peers.

Risk: The manifest-generation example includes unsafe shell behavior that could execute commands from malicious or unusual filenames.

Mitigation: Fix or replace the manifest-generation command before use, and test filename handling with representative edge cases.

Risk: The artifact overclaims safe two-way conflict handling and should not be treated as reliable conflict recovery as written.

Mitigation: Do not rely on the examples for production bidirectional sync or conflict recovery without independent implementation review and testing.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [Pilot Sync on ClawHub](https://clawhub.ai/teoslayer/skills/pilot-sync)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, jq, fswatch or inotifywait, md5sum, and stat.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
