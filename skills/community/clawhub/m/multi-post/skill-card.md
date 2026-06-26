## Description: <br>
Multi-platform content publisher via browser automation that adapts and posts text and images to Weibo, Xiaohongshu, Zhihu, Twitter/X, Reddit, V2EX, Douban, LinkedIn, and similar platforms from one command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffchang2024](https://clawhub.ai/user/jeffchang2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to adapt one piece of content for multiple social platforms and publish it through browser sessions where they are already logged in. It is intended for cross-platform posting workflows that need platform-specific length, tone, image, subreddit, node, or title handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live content through accounts already logged into Chrome without a built-in confirmation step. <br>
Mitigation: Require a final preview and explicit user approval for each destination before any publish button is clicked. <br>
Risk: Content may be posted to the wrong platform, account, subreddit, or V2EX node if the target is underspecified. <br>
Mitigation: Specify the exact target platforms and accounts before execution, and provide required destination details such as subreddit, node, and title. <br>
Risk: Browser automation can encounter platform rate limits, upload failures, login redirects, or CAPTCHA challenges. <br>
Mitigation: Run platforms sequentially, wait between destinations, retry uploads once when appropriate, and skip blocked or CAPTCHA-gated flows while reporting the status. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jeffchang2024/multi-post) <br>
- [Publisher Profile](https://clawhub.ai/user/jeffchang2024) <br>
- [Platform Automation Flows](artifact/references/platform-flows.md) <br>
- [Platform Content Rules](artifact/references/platform-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, browser automation steps] <br>
**Output Format:** [Markdown-style adapted post content, browser action guidance, and per-platform success or failure summaries with URLs when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill operates sequentially across selected platforms and may publish live posts through logged-in browser sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
