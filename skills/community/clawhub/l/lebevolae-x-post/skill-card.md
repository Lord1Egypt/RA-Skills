## Description: <br>
Automatically posts text or a single local image to X/Twitter using provided developer credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lebevolae](https://clawhub.ai/user/lebevolae) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and social media operators use this skill to let an agent publish text posts or single-image posts to X/Twitter with configured OAuth credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent using this skill can publish text or a local image through the user's X/Twitter account. <br>
Mitigation: Review the exact text and image before posting, avoid private media, and use revocable, least-privilege developer credentials. <br>
Risk: Configured X/Twitter credentials could grant account write access beyond a single post. <br>
Mitigation: Use dedicated developer credentials with only the permissions needed for posting and rotate or revoke them when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lebevolae/lebevolae-x-post) <br>
- [X Developer Platform](https://developer.twitter.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with requested post content, local image path details, and credential setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish text and one local image through the user's X/Twitter account when credentials are configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
