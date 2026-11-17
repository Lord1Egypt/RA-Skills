## Description:

Add, refine, calibrate, or migrate OpenClaw Control UI themes by patching the installed bundled frontend assets in dist/control-ui/assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ailough](https://clawhub.ai/user/ailough)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create, tune, and migrate Control UI themes in an installed OpenClaw frontend bundle. It is also useful when preserving a custom theme across an OpenClaw upgrade through backup, structural comparison, and careful re-registration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill edits live OpenClaw UI bundles, which can break theme selection or visible UI behavior if the active install or patch point is wrong.

Mitigation: Confirm the active OpenClaw path, back up the live JavaScript and CSS bundles before editing, and verify the exact bundle structures before patching.

Risk: The helper script can run shell commands and can write backups outside the intended directory.

Mitigation: Run it only from a trusted workspace and PATH, use a simple lowercase theme id containing only letters, numbers, and hyphens, and choose an explicit backup directory.

## Reference(s):

- [OpenClaw Theme Patcher on ClawHub](https://clawhub.ai/ailough/skills/openclaw-theme-patcher)
- [Bundle Patch Points](references/patch-points.md)
- [Theme Input to Token Mapping](references/token-mapping.md)
- [Theme Migration Checklist](references/theme-migration-checklist.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell commands, code snippets, file paths, and verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce instructions for editing live OpenClaw JavaScript and CSS bundles, backup paths, theme IDs, selectors, and verification notes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
