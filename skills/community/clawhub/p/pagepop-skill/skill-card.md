## Description: <br>
Create and continue PagePop content-generation conversations from a host app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jujian-pp](https://clawhub.ai/user/jujian-pp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and host application integrators use this skill to connect agents to PagePop so users can authorize once, create or continue content-generation conversations, stream progress, and receive generated artifacts. <br>

### Deployment Geography for Use: <br>
Global, with region-based PagePop endpoints for mainland China and non-mainland users. <br>

## Known Risks and Mitigations: <br>
Risk: Configuration can redirect PagePop credentials and user content to a non-PagePop API endpoint. <br>
Mitigation: Install only when the PagePop service, publisher, and host environment are trusted; do not set PAGEPOP_API_BASE_URL or --api-base-url unless the endpoint is controlled and trusted. <br>
Risk: A login token file can bypass the normal browser authorization flow. <br>
Mitigation: Avoid login-token-file unless the host operator understands and accepts the authorization bypass. <br>
Risk: The skill may write local PagePop state and generated image files. <br>
Mitigation: Configure or clear PAGEPOP_SKILL_STATE_DIR and PAGEPOP_SKILL_ARTIFACT_DIR according to the host environment's data retention requirements. <br>


## Reference(s): <br>
- [PagePop Skill API](references/api.md) <br>
- [PagePop ClawHub listing](https://clawhub.ai/jujian-pp/pagepop-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration, guidance] <br>
**Output Format:** [JSON Lines events with artifact delivery payloads and channel-aware presentation data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local PagePop state and generated image files unless disabled or cleared.] <br>

## Skill Version(s): <br>
0.0.4 (source: ClawHub release metadata; artifact manifest release_tag v0.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
