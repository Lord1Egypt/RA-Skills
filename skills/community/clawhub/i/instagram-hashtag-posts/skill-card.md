## Description: <br>
Scrapes Instagram hashtag posts from a logged-in browser session and returns captions, engagement counts, media URLs, pagination data, and user identifiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and automation developers use this skill to collect Instagram hashtag top-post data that is available through their own logged-in browser session for social content review, reporting, or research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the user's logged-in Instagram browser session to make backend GraphQL requests. <br>
Mitigation: Install and run only when the user is comfortable with an agent making authenticated requests through that session. <br>
Risk: Batch or multi-session use may trigger rate limits and can support throughput scaling that the security guidance flags for review. <br>
Mitigation: Avoid stealth sessions or throughput scaling; keep usage serial, low frequency, and aligned with the user's access permissions. <br>
Risk: The authoritative security verdict is suspicious pending clearer disclosure of token and session behavior. <br>
Mitigation: Review before deployment and prefer documentation that clearly discloses session use and removes rate-limit evasion guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/instagram-hashtag-posts) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON objects with Markdown guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an active logged-in Instagram browser session; results are limited to Instagram top posts and may include pagination cursors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
