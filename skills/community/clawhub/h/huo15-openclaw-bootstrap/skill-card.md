## Description: <br>
Guides OpenClaw users through a four-step workspace onboarding flow that prepares standard identity, user, style, tools, and agent instruction files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw and Claude Code users use this skill to complete a guided onboarding flow for a new or reset workspace. It collects basic profile, role, domain, and preference information, then prepares workspace configuration files for future agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change workspace identity and instruction files and complete bootstrap state. <br>
Mitigation: Ask for a dry run before applying changes, review generated file contents, and keep backups of existing workspace files before replacement. <br>
Risk: The skill describes copying shared memory that may contain credentials or sensitive information. <br>
Mitigation: Skip MEMORY.md copying unless the source file has been reviewed for secrets and the destination workspace is appropriate. <br>
Risk: The skill may persist profile data outside the current workspace for cross-workspace reuse. <br>
Mitigation: Skip or delete the profile backup under ~/knowledge/huo15/profile when cross-workspace persistence is not desired. <br>
Risk: Deleting BOOTSTRAP.md removes the onboarding marker and can make rollback harder. <br>
Mitigation: Prefer renaming BOOTSTRAP.md to a completed timestamped file when retaining rollback context matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-openclaw-bootstrap) <br>
- [README](artifact/README.md) <br>
- [Domain presets](artifact/presets/domains.md) <br>
- [Role presets](artifact/presets/roles.md) <br>
- [Style presets](artifact/presets/souls.md) <br>
- [Timezone presets](artifact/presets/timezones.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file and shell command instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates workspace profile and configuration files; may include optional cross-workspace profile backup guidance.] <br>

## Skill Version(s): <br>
2.1.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
