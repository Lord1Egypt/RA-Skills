## Description: <br>
Searches web pages, news, images, and videos through SkillBoss API Hub with filters and text, Markdown, or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve current web, news, image, and video results for research, fact-checking, resource discovery, and market or topic monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to SkillBoss API Hub and may contain sensitive or confidential information. <br>
Mitigation: Only submit queries authorized for external search; do not include secrets, credentials, private personal data, or confidential company material. <br>
Risk: The output option can create or overwrite files at a user-chosen path. <br>
Mitigation: Review output paths before execution and write only to intended locations. <br>
Risk: Search results may be incomplete, outdated, or unsuitable as sole evidence for high-impact decisions. <br>
Mitigation: Verify important claims with primary sources before relying on the results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/jx-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text, Markdown, or JSON search results printed to stdout or saved to a user-chosen file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and supports result limits, time range, region, safe-search, and media-specific filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
