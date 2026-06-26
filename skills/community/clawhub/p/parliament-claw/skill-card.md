## Description: <br>
Play The Parliament Game by helping a user label Canadian House of Commons Q&A pairs as substantive, non-response, or skip. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[idiom-bytes](https://clawhub.ai/user/idiom-bytes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to fetch Canadian parliamentary Q&A pairs, review them with a human in the loop, and submit confirmed labels that support civic AI accountability scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts qa.canada-central.com and sends confirmed labels plus model attribution to that service. <br>
Mitigation: Review each Q&A pair with the user before submission and submit only labels the user confirms. <br>
Risk: The skill creates or uses a Parliament Game token for API access. <br>
Mitigation: Use a dedicated token when providing PARLIAMENT_GAME_TOKEN and avoid sharing token values in chat or logs. <br>
Risk: API rate limits can interrupt batch labeling. <br>
Mitigation: Respect the documented limits and wait 60 seconds before retrying after a 429 response. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/idiom-bytes/parliament-claw) <br>
- [The Parliament Game website](https://qa.canada-central.com) <br>
- [The Parliament Game API docs](https://qa.canada-central.com/docs) <br>
- [Canada Central](https://canada-central.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with HTTP request examples and short JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for API examples and may use PARLIAMENT_GAME_TOKEN when provided.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
