## Description: <br>
Search, install, and export agentars from the CatchClaw marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovelcp](https://clawhub.ai/user/lovelcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find marketplace agentars, install them into OpenClaw workspaces, export local agents as agentar ZIP packages, or restore a workspace from backup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged installer downloads and runs remote code without integrity checks. <br>
Mitigation: Prefer running the bundled agentar_cli.mjs directly as documented, and use install.sh only after verifying the release source and integrity. <br>
Risk: Installing an agentar can overwrite the main workspace. <br>
Mitigation: Prefer creating a new named agent, require explicit user confirmation before overwrite, and rely on backups before restoring or replacing a workspace. <br>
Risk: API keys or memory content can persist locally or be packaged into exports when sensitive options are used. <br>
Mitigation: Use --api-key and --include-memory only when explicitly needed, and review exported ZIP files for credentials or personal data before sharing. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/lovelcp/install) <br>
- [Project homepage](https://github.com/OpenAgentar/catchclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or overwrite of local agent workspaces and export ZIP files when the user confirms those actions.] <br>

## Skill Version(s): <br>
3.5.8 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
