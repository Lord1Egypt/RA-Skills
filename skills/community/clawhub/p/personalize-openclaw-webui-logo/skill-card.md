## Description:

Personalizes the OpenClaw WebUI favicon by applying bundled logo sets to control-ui assets and optionally installing a startup hook that restores the selected logo after upgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woohahahaaa](https://clawhub.ai/user/woohahahaaa)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to switch among bundled favicon sets, restore the default favicon, update the logo library, and optionally install an auto-restore hook for OpenClaw upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes into the local OpenClaw UI package and its optional startup hook can repeatedly restore favicon files.

Mitigation: Install only if this local customization behavior is desired; review or remove ~/.openclaw/hooks/logo-guard to stop automatic restoration.

Risk: OPENCLAW_UI_DIR can direct the scripts to a local path beyond the auto-detected OpenClaw control-ui directory.

Mitigation: Set OPENCLAW_UI_DIR only to a verified OpenClaw control-ui directory, and avoid running the scripts as root.

## Reference(s):

- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw)
- [ClawHub skill page](https://clawhub.ai/woohahahaaa/skills/personalize-openclaw-webui-logo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed, the skill can write favicon files and managed hook files in local OpenClaw directories.]

## Skill Version(s):

2.4.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
