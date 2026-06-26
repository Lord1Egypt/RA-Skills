## Description: <br>
Search Xiaohongshu notes, inspect creator profiles, resolve share links, and drill into note comments, replies, and note detail endpoints through JustOneAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to retrieve structured Xiaohongshu note, creator, comment, reply, search, and share-link data through JustOneAPI endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is used for authenticated requests and may appear in query parameters or command logs if handled carelessly. <br>
Mitigation: Keep JUST_ONE_API_TOKEN in an environment variable, avoid sharing full request URLs or logs, and rotate the token if it is exposed. <br>
Risk: Submitted Xiaohongshu searches, note IDs, user IDs, comment IDs, cursors, and share links are sent to JustOneAPI. <br>
Mitigation: Use the skill only when the user trusts JustOneAPI with those inputs and avoid sending unnecessary sensitive identifiers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu&utm_content=project_link) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu&utm_content=project_link) <br>
- [Generated operations reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and the JUST_ONE_API_TOKEN environment variable for authenticated JustOneAPI requests.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
