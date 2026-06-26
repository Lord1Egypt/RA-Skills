## Description: <br>
Safely verifies OpenClaw upgrade candidates in an isolated sidecar flow before optionally applying a global update with explicit confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianchenx](https://clawhub.ai/user/ianchenx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to verify OpenClaw updates in an isolated candidate installation and sidecar before applying them to the global installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying an update changes the global OpenClaw installation. <br>
Mitigation: Run verify-only mode first, review any printed log path on failure, and use --apply or sudo only when ready to change the global installation. <br>
Risk: Unpinned update checks may select the latest published OpenClaw version rather than a specific target. <br>
Mitigation: Use --target <version> when a specific release should be verified and applied. <br>
Risk: Sidecar verification can fail or time out before an update is safe to apply. <br>
Mitigation: Inspect the preserved sidecar log path and do not mutate the global install when verification fails. <br>


## Reference(s): <br>
- [OpenClaw Updating Documentation](https://docs.openclaw.ai/install/updating) <br>
- [Linux Guide](references/linux.md) <br>
- [macOS Guide](references/macos.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ianchenx/openclaw-safe-update) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default workflow is verify-only; apply mode requires explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
