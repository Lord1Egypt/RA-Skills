## Description: <br>
Add, reorder, and manage content in a Kosu queue via API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewspear](https://clawhub.ai/user/matthewspear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage a Kosu read-it-later queue: adding URLs, listing queued items, suggesting content, reordering items, marking items read, archiving, deleting, restoring, and exporting queue data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent using this skill can add, reorder, archive, soft-delete, suggest, and export items in a user's Kosu account. <br>
Mitigation: Use a dedicated minimal-scope API key, limit it to usekosu.com, and revoke it from Kosu settings if behavior is unexpected. <br>
Risk: Missing or misconfigured API credentials prevent authenticated Kosu API actions. <br>
Mitigation: Guide the user to create a Kosu API key, store it in KOSU_API_KEY, and confirm access by listing the queue before making changes. <br>


## Reference(s): <br>
- [Kosu homepage](https://usekosu.com) <br>
- [Kosu API base](https://usekosu.com/api/v1) <br>
- [Kosu OpenAPI spec](https://usekosu.com/openapi.json) <br>
- [Kosu skill page](https://clawhub.ai/matthewspear/kosu) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KOSU_API_KEY for authenticated Kosu API calls.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
