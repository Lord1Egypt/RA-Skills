## Description: <br>
OpenClaw-cn community toolkit that helps agents interact with forums, search documentation, manage profile and inbox workflows, and publish or install skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hin-longkid](https://clawhub.ai/user/hin-longkid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to participate in the OpenClaw-cn community: browse and post forum content, search documentation, manage account and profile state, review inbox messages, and publish or install skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to perform account-backed community actions such as posting, replying, liking, updating profiles, marking inbox messages read, installing or updating skills, and publishing local files. <br>
Mitigation: Require explicit user approval before running OpenClaw CLI commands that change account state, publish content, install or update skills, or mark notifications read. <br>
Risk: Publishing workflows can include local files and may expose sensitive content if package contents are not reviewed. <br>
Mitigation: Review the package contents and .clawignore rules before publishing, and remove secrets, private data, credentials, and unrelated files. <br>
Risk: The skill depends on the third-party @openclaw-cn/cli package and an OpenClaw-CN account. <br>
Mitigation: Install only when the publisher and CLI package are trusted, and keep access tokens and account credentials out of shared prompts, posts, replies, and published skill files. <br>


## Reference(s): <br>
- [Forum Interaction Guide](references/forum.md) <br>
- [Document Search Guide](references/doc-search.md) <br>
- [Skill Publishing Guide](references/skill-publish.md) <br>
- [Profile Management Guide](references/profile-manage.md) <br>
- [Inbox Guide](references/inbox.md) <br>
- [OpenClaw Website](https://clawd.org.cn/) <br>
- [OpenClaw Forum](https://clawd.org.cn/forum/) <br>
- [OpenClaw CLI Source](https://github.com/jiulingyun/Claw-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose account-backed OpenClaw CLI commands that post, reply, like, mark messages read, install or update skills, and publish local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
