## Description: <br>
Leviathan News is a crowdsourced crypto news API for submitting articles, posting comments, voting on content, and reading community-curated DeFi news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcor](https://clawhub.ai/user/zcor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to interact with the Leviathan News API for crypto news discovery, article submission, comments, votes, profile updates, and leaderboard reads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a raw wallet private key for local wallet-signature authentication. <br>
Mitigation: Install only with a new empty burner wallet dedicated to Leviathan News, and store the key only in a local environment variable or secure storage. <br>
Risk: Authenticated API calls can submit articles, post comments, vote, or change profile details under the wallet identity. <br>
Mitigation: Require user confirmation before any authenticated write action, and review generated headlines, comments, votes, and profile updates before submission. <br>
Risk: Session cookies grant temporary authenticated API access if exposed. <br>
Mitigation: Keep access_token cookies out of logs and shared transcripts, and re-authenticate only when needed. <br>


## Reference(s): <br>
- [Leviathan News Website](https://leviathannews.xyz) <br>
- [Leviathan News API Docs](https://api.leviathannews.xyz/docs/) <br>
- [ClawHub Skill Page](https://clawhub.ai/zcor/leviathan-news) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/zcor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands, JSON examples, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce authenticated API request examples that read or modify public wallet-linked content.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
