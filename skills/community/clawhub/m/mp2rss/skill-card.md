## Description: <br>
Mp2rss helps agents manage WeChat Official Account and X (Twitter) RSS subscriptions, authentication, and content retrieval through the mp2rss CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[areyoubugcoder](https://clawhub.ai/user/areyoubugcoder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure the mp2rss CLI, manage Feed Key authentication, manage WeChat Official Account RSS subscriptions, and retrieve WeChat articles or subscribed X posts and articles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MP2RSS_FEED_KEY is a bearer credential and can expose the user's mp2rss account if logged or shared. <br>
Mitigation: Use a trusted local terminal or secret store, avoid putting the key in shared shells or CI logs, and rely on mp2rss auth login when possible. <br>
Risk: The documented curl pipe shell installer executes remote shell content. <br>
Mitigation: Prefer the npm package or downloaded release binary; inspect installer content before using a piped shell install. <br>
Risk: Authenticated mp2rss commands can change WeChat Official Account subscriptions. <br>
Mitigation: Check login status, validate user-provided URLs, and confirm subscription identifiers from CLI output before changing subscriptions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/areyoubugcoder/mp2rss) <br>
- [Mp2rss service homepage](https://mp2rss.bugcode.dev) <br>
- [Installation reference](references/install.md) <br>
- [Authentication reference](references/auth.md) <br>
- [WeChat Official Account reference](references/mp.md) <br>
- [X account reference](references/x.md) <br>
- [Error handling reference](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON parsing notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose mp2rss CLI commands and summarize JSON command results; authenticated actions require a local mp2rss binary and a Feed Key.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
