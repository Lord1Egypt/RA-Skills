## Description: <br>
Fetches comments from an Instagram post, including comment text, username, timestamp, like count, and reply count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect comments from Instagram posts by shortcode or media ID when they are logged in and authorized to access the target post. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an authenticated Instagram scraping workflow that may collect user identifiers and comment metadata. <br>
Mitigation: Use it only for posts and data the user is authorized to collect, and handle collected identifiers under applicable privacy and data-retention policies. <br>
Risk: The security review flags under-disclosed internal API collection and rate-limit evasion guidance. <br>
Mitigation: Review the workflow before use, avoid stealth-session or rate-limit distribution guidance, and keep collection behavior within the platform and user authorization boundaries. <br>
Risk: The workflow requires an active Instagram login and may fail or return incomplete data for disabled comments, deleted comments, or unavailable accounts. <br>
Mitigation: Verify login before execution, stop if the user cannot authenticate, and report incomplete or empty results without retrying aggressively. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/instagram-post-comments-skill) <br>
- [Instagram](https://www.instagram.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON comment data and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated Instagram browser session and paginates comments with an API cursor.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
