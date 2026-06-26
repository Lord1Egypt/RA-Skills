## Description: <br>
Configure a powerful macOS machine to host multiple dedicated OpenClaw agent users with Fast User Switching, a shared Homebrew toolchain, per-user OpenClaw homes, per-user SSH trust, and auditable rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to plan and configure a Mac as a multi-user OpenClaw agent host. It helps inspect host capacity, render or execute repeatable macOS account setup commands, verify shared Homebrew/OpenClaw access, and leave rollout receipts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent macOS user accounts and change local account state. <br>
Mitigation: Run it only on a Mac you administer, render commands for review first, and prefer non-admin agent accounts unless admin access is specifically required. <br>
Risk: Account passwords can be exposed when passed through environment variables, command arguments, or dry-run output. <br>
Mitigation: Use placeholder passwords when rendering commands, avoid dry-running with real passwords, and rotate any password used through the environment or command line immediately after account creation. <br>


## Reference(s): <br>
- [Fast User Switching](references/fast-user-switching.md) <br>
- [Shared Homebrew](references/shared-homebrew.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and optional JSONL receipt output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for administrator-reviewed macOS account setup and per-user OpenClaw environment verification.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
