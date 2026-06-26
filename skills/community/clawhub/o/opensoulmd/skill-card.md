## Description: <br>
Search, summon, and possess your agent with SOUL.md personality files from the OpenSOUL.md registry <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielliuzy](https://clawhub.ai/user/danielliuzy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to search the OpenSOUL.md registry, download SOUL.md personality files, activate a selected personality for future conversations, and restore the original personality when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote registry or local SOUL.md files can persistently change the agent personality used in future conversations. <br>
Mitigation: Preview or read SOUL.md content before possession, use trusted sources, and keep `soul exorcise` available to restore the original personality. <br>
Risk: The recommended curl installer executes a remote shell script. <br>
Mitigation: Prefer the npm install path when appropriate, or inspect and verify the installer before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielliuzy/opensoulmd) <br>
- [OpenSOUL install script](https://opensoul.md/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target the soul CLI and may change the agent personality used in later conversations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
