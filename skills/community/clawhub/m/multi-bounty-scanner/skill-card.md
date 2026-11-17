## Description:

Scans recent GitHub bounty-labeled issues for new bounty opportunities with filtering, local seen-history tracking, and optional JSON export; broader multi-platform support is described as planned rather than currently implemented.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT

## Use Case:

Developers, security researchers, and bounty hunters use this skill to automate discovery of recent GitHub issues labeled as bounties, filter results by technology or reward threshold, and export new findings for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package metadata can cause npm to install an unrelated package named `gh`, while the scanner expects the official GitHub CLI.

Mitigation: Install and authenticate the official GitHub CLI separately, and remove or ignore the npm `gh` peer dependency before deployment.

Risk: The release describes broad multi-platform scanning, but the reviewed implementation currently supports GitHub scanning only.

Mitigation: Scope operational use and validation to GitHub bounty-labeled issues unless additional platform scanners are implemented and reviewed.

Risk: The scanner stores local configuration and seen-bounty history under `~/.bounty-scanner`.

Mitigation: Review local retention expectations and filesystem permissions before running it in shared or managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dagangtj/skills/multi-bounty-scanner)
- [Publisher profile](https://clawhub.ai/user/dagangtj)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text summaries or JSON scan results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tracks seen bounties under ~/.bounty-scanner and can write scan results to a user-specified JSON file.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
