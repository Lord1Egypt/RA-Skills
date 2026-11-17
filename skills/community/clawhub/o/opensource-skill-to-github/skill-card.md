## Description:

This skill guides agents through preparing a local agent skill for public release on GitHub and optionally ClawHub, with checks for internal information and user decisions at sensitive steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to prepare a local agent skill for public release. It helps create a separate copy, check for internal information, generate release files, and guide publishing decisions for GitHub and optional skill hubs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A release could expose local files or internal information if the copied skill contains unexpected content or a scan misses it.

Mitigation: Review the copied files and strip-scan results before publishing, and confirm that only intended content will be included.

Risk: Publishing could send skill contents to a service that is not part of the intended release.

Mitigation: Confirm the destination before publishing and explicitly choose whether to use optional publishing services.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/songhonglei/skills/opensource-skill-to-github)
- [Project repository (listed in skill documentation)](https://github.com/Songhonglei/build-better-skills/tree/main/skills/opensource-skill-to-github)
- [README.md](README.md)
- [Open-source playbook](references/opensource_playbook.md)
- [Internal information stripping checklist](references/strip_checklist.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown guidance and shell commands; may create a copied skill folder and release files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The steps selected by the user determine which files are created; publishing requires a user decision and configured credentials.]

## Skill Version(s):

1.0.19 (source: server-resolved release evidence and CHANGELOG.md, released 2026-10-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
