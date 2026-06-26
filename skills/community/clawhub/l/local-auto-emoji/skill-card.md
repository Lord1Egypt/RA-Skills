## Description: <br>
Local Auto Emoji automatically sends emotion-matched emoji images, generates personalized emoji sets from user avatars, supports incremental updates, and expands inline emoji markers in OpenClaw conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wdkmail](https://clawhub.ai/user/wdkmail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent developers use this skill to personalize chat responses with avatar-based emotion emojis and marker-triggered image insertion. It is intended for chat workflows that benefit from automatic emotional tone detection and generated emoji media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves avatar images and generated emojis under its public assets area. <br>
Mitigation: Use it only with user consent, and provide clear retention and deletion controls for stored avatar and emoji assets. <br>
Risk: The skill keeps short local emotion-history logs that may include chat snippets. <br>
Mitigation: Review the logging behavior before deployment, minimize retained context, and clear logs when they are no longer needed. <br>
Risk: The skill depends on an external Qwen/DashScope image-generation path and an undeclared projects/getemoji dependency. <br>
Mitigation: Review and declare the dependency chain, configure external API use explicitly, and provide a static-emoji fallback when generation is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wdkmail/local-auto-emoji) <br>
- [Publisher profile](https://clawhub.ai/user/wdkmail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Image files, Configuration] <br>
**Output Format:** [OpenClaw chat text with media directives and generated PNG emoji assets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates 512x512 PNG emoji assets, stores local user/version indexes, and limits automatic sends by interval and hourly count.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
