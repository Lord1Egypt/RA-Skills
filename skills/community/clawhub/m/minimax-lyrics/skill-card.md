## Description: <br>
Generate structured song lyrics in various styles and themes using the MiniMax lyrics_generation API for full song creation or editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raydoomed](https://clawhub.ai/user/raydoomed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to generate or edit full song lyrics with structure tags through the MiniMax lyrics_generation API. The generated lyrics can be reviewed by the user before being passed into a downstream music-generation workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MiniMax API key exposure or broad credential reuse. <br>
Mitigation: Use a dedicated MiniMax API key where possible and keep it in the skill configuration with normal file-access controls. <br>
Risk: Confidential unpublished lyrics or sensitive prompts may be sent to MiniMax. <br>
Mitigation: Avoid sending confidential or sensitive material unless the user is comfortable sharing it with MiniMax. <br>
Risk: API calls may consume MiniMax quota or create billing activity. <br>
Mitigation: Monitor MiniMax quota or billing use and confirm the user wants lyrics-only generation before invoking the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/raydoomed/minimax-lyrics) <br>
- [MiniMax lyrics_generation API endpoint](https://api.minimaxi.com/v1/lyrics_generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON containing song_title, style_tags, and lyrics, with human-readable text also printed by the script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MiniMax API key and sends the prompt and any supplied lyrics to MiniMax.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
