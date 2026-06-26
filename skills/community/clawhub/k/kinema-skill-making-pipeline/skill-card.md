## Description: <br>
KinemaClaw Skill development and publishing specification for skill development, version management, and publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeshunee](https://clawhub.ai/user/leeshunee) <br>

### License/Terms of Use: <br>
GNU General Public License v3.0 <br>


## Use Case: <br>
Developers and release maintainers use this skill to create, version, publish, and update KinemaClaw skills across GitHub, ClawHub, local caches, and Claude Code marketplace workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through remote releases, ClawHub publishing, marketplace edits, and local plugin updates using authenticated tools. <br>
Mitigation: Require explicit approval before git push, GitHub release creation, ClawHub publish, marketplace edits, or plugin update/install commands, and verify the repository, account, marketplace, version, changelog, and files before publication. <br>
Risk: The ClawHub API fallback reads a stored ClawHub token and submits release files directly when the CLI path fails. <br>
Mitigation: Use the fallback only after confirming the CLI failure, target skill, publisher account, token source, payload metadata, and upload file list; never expose or paste the token. <br>
Risk: Cache cleanup and local synchronization steps can change local ClawHub or Claude Code plugin state. <br>
Mitigation: Review each local update or cache cleanup command before execution and confirm the affected paths are limited to the intended skill cache or plugin installation. <br>


## Reference(s): <br>
- [Kinema's Skill Making Pipeline on ClawHub](https://clawhub.ai/leeshunee/kinema-skill-making-pipeline) <br>
- [Onboarding](references/ONBOARDING.md) <br>
- [Release Process](references/release-process.md) <br>
- [Marketplace Index Publishing](references/marketplace-publishing.md) <br>
- [ClawHub API Fallback](references/clawhub-api-fallback.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent through release, publishing, marketplace, plugin update, and version-check workflows.] <br>

## Skill Version(s): <br>
1.10.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
