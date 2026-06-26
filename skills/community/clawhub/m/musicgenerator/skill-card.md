## Description: <br>
AI music generation assistant powered by MakebestMusic for creating AI-generated music, songs, and audio tracks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sthk-mbm](https://clawhub.ai/user/sthk-mbm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to generate custom songs or instrumental tracks from text prompts and to check generation status using returned music IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends song prompts and music IDs to MakeBestMusic using a configured API key. <br>
Mitigation: Install only if the publisher is trusted, use a revocable or dedicated API key, and avoid private or sensitive material in prompts. <br>
Risk: Changing MBM_API_BASE can route requests and credentials to a different endpoint. <br>
Mitigation: Leave MBM_API_BASE unset unless intentionally routing to another trusted endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sthk-mbm/musicgenerator) <br>
- [MakeBestMusic](https://makebestmusic.com/?pid=PIDcLjhgCXUQ) <br>
- [MakeBestMusic API endpoint](https://api.makebestmusic.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an apiKey environment value and may return pending, completed, or failed generation status.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
