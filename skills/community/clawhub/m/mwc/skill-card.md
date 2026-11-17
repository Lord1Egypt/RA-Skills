## Description:

mac-wallpaper-changer helps agents change macOS wallpapers, recommend images from Bing, Unsplash, Picsum, local files, or URLs, and manage wallpaper ratings and preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akayj](https://clawhub.ai/user/akayj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent configure and run macOS wallpaper workflows, including wallpaper changes, scheduled daily updates, preference tracking, and recommendation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download remote images and set them as the macOS wallpaper.

Mitigation: Use trusted image sources and avoid untrusted --url values before allowing the agent to apply a wallpaper.

Risk: The skill can restart wallpaper-related UI processes and change desktop settings.

Mitigation: Run it only on macOS systems where wallpaper changes are intended and review commands before execution.

Risk: Cron setup can schedule recurring wallpaper changes.

Mitigation: Add cron entries only when scheduled wallpaper updates are explicitly desired.

Risk: The skill stores wallpaper ratings, preference data, and logs under ~/wallpaper-daily/.

Mitigation: Review stored preference and log files if wallpaper history or ratings are sensitive.

Risk: The scripts run through uv with Python dependencies.

Mitigation: Review the uv dependency environment before installation or execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/akayj/skills/mwc)
- [Wallpaper Sources](references/wallpaper-sources.md)
- [Embedding Configuration](references/embedding-config.md)
- [Embedding Configuration Template](assets/embedding-config.template.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download wallpaper image files, change macOS desktop settings, write ratings and logs under ~/wallpaper-daily/, and optionally read embedding configuration from ~/.wallpaper_prefs.json or WALLPAPER_EMBEDDING_CONFIG.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
