## Description:

Pilot Share helps agents share a single file or directory over Pilot Protocol with progress tracking and retry guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Pilot Share to send one-time files or archived directories to another agent and inspect received shares.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files may be sent to the wrong destination agent or include sensitive content.

Mitigation: Confirm the destination agent ID and inspect the exact file or directory path before running send commands.

Risk: The directory archive example writes a temporary archive under /tmp and removes it only after the send command completes.

Mitigation: Use a mktemp-based archive path and cleanup trap before sharing directories.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-share)

## Skill Output:

**Output Type(s):** [shell commands, code, guidance]

**Output Format:** [Markdown with Bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use JSON output from pilotctl and may require jq, tar, pilotctl, and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: release evidence; artifact frontmatter version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
