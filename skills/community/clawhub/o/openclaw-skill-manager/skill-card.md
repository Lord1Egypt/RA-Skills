## Description: <br>
Manages OpenClaw skill installation, discovery, updates, movement, and custom skill spaces through CLI-guided workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage skill spaces, install or update skills, list installed skills, and move skills between configured OpenClaw locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The manual install flow can unpack arbitrary remote archives into agent-loaded skill directories without safety checks. <br>
Mitigation: Prefer ClawHub registry installs, inspect and trust any URL archive before use, and add only custom skill directories that the user controls. <br>
Risk: The skill modifies OpenClaw skill paths and configuration. <br>
Mitigation: Confirm target paths before changes, keep the documented backups for moves and updates, and verify the OpenClaw skill list after configuration changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liberalchang/openclaw-skill-manager) <br>
- [Publisher profile](https://clawhub.ai/user/liberalchang) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes user confirmations before path, install, update, and move operations.] <br>

## Skill Version(s): <br>
3.1.3 (source: ClawHub release metadata; artifact frontmatter says 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
