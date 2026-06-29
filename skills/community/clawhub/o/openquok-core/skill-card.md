## Description: <br>
Schedule and manage social posts with the openquok CLI: authenticate, upload media, create drafts and scheduled posts, and read channel analytics for integrations in an OpenQuok workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ratimon](https://clawhub.ai/user/ratimon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and social media teams use this skill to have an agent prepare and run OpenQuok CLI workflows for authenticated social channel posting, scheduling, media upload, drafts, status changes, and analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect connected social accounts by posting, scheduling, uploading media, deleting queued posts, changing draft or scheduled status, and reading analytics. <br>
Mitigation: Install and use it only for OpenQuok workspaces where the agent is expected to manage connected social channels, and review planned publishing actions before execution. <br>
Risk: Media uploads or URL-based fetches may expose confidential, private, or embargoed assets through provider workflows or public-fetch requirements. <br>
Mitigation: Use only approved media sources and avoid confidential, private, or embargoed media URLs unless the workspace owner accepts the public-fetch and timing behavior. <br>
Risk: Authenticated CLI credentials authorize API actions in the selected OpenQuok workspace. <br>
Mitigation: Use the intended workspace, prefer device login or scoped programmatic tokens, and rotate or revoke tokens that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ratimon/skills/openquok-core) <br>
- [OpenQuok CLI package](https://www.npmjs.com/package/@openquok/auto-cli) <br>
- [OpenQuok](https://www.openquok.com/) <br>
- [Command reference](resources/command-reference.md) <br>
- [Provider settings](resources/provider-settings.md) <br>
- [Workflow recipes](resources/patterns.md) <br>
- [JSON post examples](resources/examples/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with openquok shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the openquok binary and authenticated OpenQuok workspace credentials for API actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
