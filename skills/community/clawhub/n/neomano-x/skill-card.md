## Description: <br>
Draft, revise, and publish X (Twitter) posts with an image using the X API, with an explicit human approval step before publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elandivar](https://clawhub.ai/user/elandivar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to draft and revise X posts, attach an image, suggest image alt text, and publish only after the user explicitly approves with PUBLICAR or PUBLISH. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive X API credentials and access tokens. <br>
Mitigation: Use a dedicated least-privilege X app or token where possible, keep OAuth values out of shared logs and command history, and rotate tokens if they are exposed. <br>
Risk: The skill can publish content to the user's X account after approval. <br>
Mitigation: Review the final post text and image before typing PUBLICAR or PUBLISH. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/elandivar/neomano-x) <br>
- [X OAuth request token endpoint](https://api.twitter.com/oauth/request_token) <br>
- [X media upload endpoint](https://upload.twitter.com/1.1/media/upload.json) <br>
- [X create tweet endpoint](https://api.twitter.com/2/tweets) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON dry-run output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and X API credentials supplied through environment variables.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
