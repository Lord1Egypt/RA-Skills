## Description: <br>
Control your X/Twitter account — view timeline, search tweets, post, like, retweet, bookmark. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bosshuman](https://clawhub.ai/user/bosshuman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to read X/Twitter timelines, searches, tweet details, and user posts through a local API, and to perform account actions such as posting, liking, retweeting, and bookmarking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external executable and exported X/Twitter browser cookies, which can expose account session access. <br>
Mitigation: Install only from a trusted release source, keep cookies.json private, use a secondary account where possible, and stop the localhost service when the task is complete. <br>
Risk: The skill can perform account-changing actions such as posting, liking, retweeting, and bookmarking. <br>
Mitigation: Require explicit user approval before any post, like, retweet, or bookmark action. <br>


## Reference(s): <br>
- [OpenClaw X ClawHub listing](https://clawhub.ai/bosshuman/openclaw-x) <br>
- [OpenClaw X GitHub releases](https://github.com/bosshuman/openclaw-x/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local API endpoint patterns and curl examples; account-changing actions should require explicit user approval.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence; artifact frontmatter states 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
