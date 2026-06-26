## Description: <br>
Fixes OpenClaw Gateway spawn EBADF, RPC probe failed, and EMFILE too many open files errors caused by file descriptor exhaustion from too many files in the workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomaszhang2661](https://clawhub.ai/user/thomaszhang2661) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers maintaining OpenClaw Gateway on macOS use this skill to diagnose workspace file descriptor exhaustion, clean dependency directories when approved, update LaunchAgent file descriptor limits, and restart the gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The repair script can remove `.venv` and `node_modules` directories from the OpenClaw workspace. <br>
Mitigation: Inspect the listed directories before confirming deletion, and move or back up anything that is not easily recreated. <br>
Risk: The repair changes a macOS LaunchAgent plist and restarts the OpenClaw Gateway service. <br>
Mitigation: Review the created plist backup and final LaunchAgent configuration before relying on the restarted service. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and XML snippets plus a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-specific; includes interactive confirmation before deleting dependency directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
