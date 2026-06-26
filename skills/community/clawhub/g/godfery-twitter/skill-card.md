## Description: <br>
Search X (Twitter) in real time, extract relevant posts, and publish tweets or replies for social listening, engagement, and rapid content operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, social media operators, and agents use this skill to search Twitter/X, monitor users and trends, and publish tweets, likes, or retweets through SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to send Twitter/X passwords and proxy details to a third-party API. <br>
Mitigation: Install only if SkillBoss/AISA is trusted with the account, prefer a test or low-risk account, and avoid sharing a primary password where possible. <br>
Risk: The skill can perform public account actions such as posting, liking, retweeting, and profile updates without built-in confirmation. <br>
Mitigation: Require explicit human approval before login, post, like, retweet, or profile-update actions. <br>
Risk: The skill depends on the SKILLBOSS_API_KEY credential for paid API access. <br>
Mitigation: Store the API key in a controlled environment variable, rotate it if exposed, and monitor credit usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godferylindsay/godfery-twitter) <br>
- [SkillBoss API reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY, curl, and python3; write operations require Twitter/X account login through the third-party API.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
