## Description: <br>
Search X (Twitter) in real time, extract relevant posts, and publish tweets/replies instantly - useful for social listening, engagement, and rapid content operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and social operations teams use this skill to search X posts, monitor users and trends, and perform account actions such as posting, liking, and retweeting through the SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish posts, like posts, retweet, and update profile data from a connected X account. <br>
Mitigation: Require human approval before login, posting, liking, retweeting, or profile changes, and prefer a dedicated low-risk account. <br>
Risk: Login operations send account credentials and proxy details to the third-party SkillBoss/api.aisa.one provider. <br>
Mitigation: Install only when the provider is trusted, avoid using a primary account password where possible, and limit credentials to the minimum account needed. <br>
Risk: API calls may consume paid credits and account automation may trigger platform rate limits or suspension. <br>
Mitigation: Review planned calls before execution, monitor returned usage costs, and keep automated engagement volume conservative. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/godfery-tw) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [SkillBoss signup](https://skillbossai.com) <br>
- [API Reference](https://aisa.mintlify.app/api-reference/introduction) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python command examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; write operations require X account login and may consume paid credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
