## Description: <br>
Karakeep bookmark manager with full native RESTful API support including notes, updates, and deletion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VandeeFeng](https://clawhub.ai/user/VandeeFeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manage Karakeep bookmarks through shell helpers for creating, updating, deleting, listing, searching, tagging, and organizing saved content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Karakeep bookmark data when configured with a Karakeep API key. <br>
Mitigation: Use a limited or revocable API key when available and verify KARAKEEP_SERVER_URL before running account-changing commands. <br>
Risk: Delete and other account-changing operations can alter or remove saved bookmark data. <br>
Mitigation: Require explicit user approval before destructive or account-changing actions, including bookmark deletion, list changes, and tag changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/VandeeFeng/karakeep-sh) <br>
- [Publisher profile](https://clawhub.ai/user/VandeeFeng) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KARAKEEP_SERVER_URL, KARAKEEP_API_KEY, curl, and jq.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
