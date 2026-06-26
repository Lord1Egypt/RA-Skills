## Description: <br>
Scheduling polls for humans and their agents. Create polls, share participation links, collect votes, and find the best meeting time. A Doodle alternative built for the age of AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkelk](https://clawhub.ai/user/mkelk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to create Meetlark scheduling polls, share participant links, collect availability votes, inspect results, and close polls after a meeting time is chosen. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Poll admin tokens allow access to full results, individual votes, and poll closure actions. <br>
Mitigation: Keep admin tokens private, share only participation URLs, and remove admin tokens from agent memory or notes once the poll is closed or no longer needed. <br>
Risk: Individual vote results and scheduling availability can reveal sensitive participant information. <br>
Mitigation: Avoid exposing individual votes unless necessary and summarize aggregate availability when possible. <br>


## Reference(s): <br>
- [Meetlark skill page](https://clawhub.ai/mkelk/meetlark) <br>
- [Meetlark website](https://meetlark.ai) <br>
- [Meetlark OpenAPI spec](https://meetlark.ai/api/v1/openapi.json) <br>
- [Meetlark interactive docs](https://meetlark.ai/docs) <br>
- [Meetlark AI plugin manifest](https://meetlark.ai/.well-known/ai-plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown] <br>
**Output Format:** [Markdown with API request examples and user-facing scheduling messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include poll participation links, admin-token handling guidance, vote summaries, and close-poll instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
