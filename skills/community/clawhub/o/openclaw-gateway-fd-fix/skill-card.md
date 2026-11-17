## Description:

Fixes OpenClaw Gateway spawn EBADF, RPC probe failed, and EMFILE too many open files errors caused by file descriptor exhaustion from too many files in a workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhang2661](https://clawhub.ai/user/thomaszhang2661)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to diagnose and repair macOS OpenClaw Gateway crashes or hangs caused by workspace file descriptor exhaustion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The repair script can permanently delete workspace dependency directories.

Mitigation: Review the listed targets first and back up important workspace content before confirming deletion.

Risk: The repair script modifies the macOS OpenClaw Gateway LaunchAgent and restarts the service.

Mitigation: Back up the LaunchAgent plist, validate the intended resource-limit changes, and confirm gateway health after restart.

Risk: Unsafe shell path handling could delete unintended files or break the gateway service.

Mitigation: Prefer NUL-delimited path handling, plist-aware validation, and a rollback plan before operational use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash and XML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a shell repair script that can remove dependency directories, update a macOS LaunchAgent plist, restart the gateway service, and report verification status.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
