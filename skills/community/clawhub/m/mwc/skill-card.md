## Description: <br>
A macOS wallpaper assistant that changes desktop backgrounds, downloads images from Bing, Unsplash, Picsum, local files, or direct URLs, and uses ratings and preference data to recommend future wallpapers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akayj](https://clawhub.ai/user/akayj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage macOS wallpapers, automate scheduled wallpaper changes, search or apply wallpapers from supported sources, rate images, and receive preference-based recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact remote wallpaper providers and download image files. <br>
Mitigation: Use supported providers or trusted direct image URLs, and avoid sensitive search terms. <br>
Risk: The skill saves downloaded wallpapers, logs, and preference data under ~/wallpaper-daily. <br>
Mitigation: Review or delete local wallpaper history and preference files before sharing the machine or collected data. <br>
Risk: The skill can change the macOS desktop wallpaper and can be scheduled to run automatically with cron. <br>
Mitigation: Add recurring cron entries only when automatic wallpaper changes are desired, and remove the entry to stop scheduled changes. <br>
Risk: Optional provider configuration may include API keys. <br>
Mitigation: Keep API keys out of shared configuration files and use local environment-specific configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/akayj/mwc) <br>
- [Wallpaper source configuration](references/wallpaper-sources.md) <br>
- [Embedding configuration](references/embedding-config.md) <br>
- [Embedding configuration template](assets/embedding-config.template.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions and commands for macOS wallpaper changes, recommendation workflows, preference management, location setup, and scheduled automation.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
