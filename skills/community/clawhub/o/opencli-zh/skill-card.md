## Description: <br>
Chinese-language agent guidance for using the opencli CLI to access supported websites, desktop apps, and external CLIs for browsing, search, timelines, bookmarks, notifications, trending content, articles, history, and user-confirmed write actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poiskgit](https://clawhub.ai/user/poiskgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to choose safe opencli command paths for supported platforms, summarize read results, and gate public or persistent write actions behind explicit user confirmation. It is especially useful when an agent needs Chinese-language operating guidance for opencli targets and custom adapter fallback workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rely on existing browser sessions for supported websites, which may expose logged-in or account-specific data to commands. <br>
Mitigation: Install and use it only when the user trusts the opencli package and consents to browser-session access for the target platform. <br>
Risk: Supported write actions such as posts, replies, likes, follows, comments, deletes, blocks, saves, and subscriptions can be public or irreversible. <br>
Mitigation: Confirm the target object, submitted content, and external visibility before executing any write action. <br>
Risk: Custom adapters and related debug flows can persist files under ~/.opencli or inspect browser bridge state, page data, or request traffic. <br>
Mitigation: Explain the affected browser and filesystem scope, then require explicit user approval before adapter creation, request interception, bridge changes, or persistent writes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/poiskgit/opencli-zh) <br>
- [Publisher profile](https://clawhub.ai/user/poiskgit) <br>
- [opencli upstream project](https://github.com/nicepkg/opencli) <br>
- [Skill instructions](SKILL.md) <br>
- [Fallbacks](guides/fallbacks.md) <br>
- [Custom Adapters](guides/custom-adapters.md) <br>
- [Custom Adapters Reference](guides/custom-adapters-reference.md) <br>
- [Reference Bootstrap](guides/reference-bootstrap.md) <br>
- [Bilibili target reference](references/bilibili.md) <br>
- [Google target reference](references/google.md) <br>
- [Hacker News target reference](references/hackernews.md) <br>
- [Mtime target reference](references/mtime.md) <br>
- [Reddit target reference](references/reddit.md) <br>
- [Twitter / X target reference](references/twitter.md) <br>
- [Wikipedia target reference](references/wikipedia.md) <br>
- [Xiaohongshu target reference](references/xiaohongshu.md) <br>
- [YouTube target reference](references/youtube.md) <br>
- [Zhihu target reference](references/zhihu.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Simplified Chinese Markdown with inline shell commands, concise summaries, and optional structured opencli output such as JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read workflows may summarize platform results; write workflows require explicit user confirmation before public, persistent, or irreversible actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
