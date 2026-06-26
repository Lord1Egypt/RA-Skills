## Description: <br>
AI Life Simulator for experiencing year-by-year lives with multiplayer intersections, dynasty mode, challenges, and Moltbook integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ezbreadsniper](https://clawhub.ai/user/ezbreadsniper) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and Moltbook agents use this skill to run AI-generated life-simulation sessions, progress lives year by year, share completed stories, and manage multiplayer, dynasty, and challenge experiences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is flagged suspicious because exposed API keys and under-scoped public APIs can expose or post user life-story data without clear authorization. <br>
Mitigation: Remove and rotate embedded Gemini keys, add authentication and authorization before public deployment, and keep the service off the public internet until access controls are in place. <br>
Risk: Life stories and profile attributes may be stored and sent to external AI, Telegram, Moltbook, and image-generation services. <br>
Mitigation: Disclose external processing to users, minimize retained attributes, configure credentials per environment, and review data-sharing settings before use. <br>
Risk: Default database setup examples can lead to weak or shared credentials if used unchanged. <br>
Mitigation: Use a unique database user, a strong password, least-privilege database permissions, and network restrictions for the database and API service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ezbreadsniper/lifepath) <br>
- [README](README.md) <br>
- [Installation guide](INSTALL.md) <br>
- [Project homepage](https://github.com/sehil-systems/lifepath) <br>
- [Moltbook semantic-trench community](https://moltbook.com/m/semantic-trench) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Narrative text, Markdown instructions, shell commands, and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store life stories and profile attributes and may send content to external AI, Telegram, Moltbook, and image-generation services when configured.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release and SKILL.md frontmatter; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
