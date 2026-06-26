## Description: <br>
Face search and deep research via the Nuwa World API for visual identity intelligence and knowledge synthesis from the open web. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrewchen-oss](https://clawhub.ai/user/andrewchen-oss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External investigators and developers use this skill to guide agents through Nuwa World API requests for face search and person-focused open-web research. It helps agents prepare authenticated curl calls, poll asynchronous face-search jobs, and interpret structured research responses with sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends face images and person-focused research queries to Nuwa World, which can involve sensitive identity data. <br>
Mitigation: Use only for lawful, authorized investigations; confirm each image or query before submission; avoid images of people without consent or another legal basis. <br>
Risk: Nuwa World privacy, retention, billing, and credit terms may affect whether a specific investigation is appropriate. <br>
Mitigation: Review Nuwa World's privacy, retention, billing, and credit terms before deployment or use. <br>


## Reference(s): <br>
- [Nuwa World API documentation](https://gateway.nuwa.world/docs) <br>
- [Nuwa World platform](https://platform.nuwa.world) <br>
- [ClawHub release page](https://clawhub.ai/andrewchen-oss/nuwa-world-osint-human-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash curl commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NUWA_API_KEY and curl; face-search requests send face images to Nuwa World and deep-research requests send user queries to Nuwa World.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
