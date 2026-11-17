## Description:

Install, verify, and operate the obclip CLI to clip live web pages into Markdown or Obsidian notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rycen7822](https://clawhub.ai/user/rycen7822)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to install and run the obclip CLI, choose browser/profile options, and capture web pages as Markdown files, stdout, or Obsidian notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead users to install or run mutable remote npm code.

Mitigation: Review the skill before installing and prefer a pinned, reviewed @harris7/obclip version instead of bare npm or npx commands.

Risk: Authenticated browser profiles may expose cookies, sessions, or private page content during clipping.

Mitigation: Use a dedicated browser profile with only the minimum login state needed and confirm before clipping authenticated or private pages.

## Reference(s):

- [Obclip Skill Page](https://clawhub.ai/rycen7822/skills/obclip)
- [Installation And Invocation](references/install-and-invoke.md)
- [Command Recipes](references/command-recipes.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce saved Markdown or Obsidian notes when the documented obclip commands are executed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
