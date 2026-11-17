## Description:

Use when patching Hermes Desktop source for titlebar, font, window-chrome, zoom, launcher icon, app metadata, or related desktop-app customization work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mina-atef-00](https://clawhub.ai/user/mina-atef-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, apply, rebuild, and verify local Hermes Desktop source customizations, especially titlebar sizing, font behavior, and desktop chrome changes. It emphasizes checking the live source tree and git state before claiming or changing local customizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users through local Hermes Desktop source changes that can break layout, rebuilding, or update behavior if applied without checking the current source tree.

Mitigation: Follow the approval-first workflow, inspect the current git branch and working tree, verify target files before editing, rebuild, and visually check the desktop after changes.

Risk: The security evidence notes a documentation inconsistency about update handling that users should verify before following.

Mitigation: Confirm the active update strategy and clean working tree before using the update guidance, and stop to inspect git state if an update reports conflicts or skipped code updates.

Risk: Titlebar and font behavior depends on multiple independently maintained source locations, so partial edits can leave visible UI drift.

Mitigation: Change related constants, hardcoded class values, CSS variables, icon sizing, and fallback values together, then verify the result with a screenshot.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mina-atef-00/skills/hermes-desktop-customization)
- [Publisher profile](https://clawhub.ai/user/mina-atef-00)
- [Project homepage](https://github.com/mina-atef-00/agent-skills)
- [Titlebar sizing map](references/titlebar-sizing.md)
- [Desktop font pipeline map](references/font-pipeline.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code paths and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
