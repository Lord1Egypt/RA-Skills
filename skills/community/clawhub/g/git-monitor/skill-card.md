## Description: <br>
Git Monitor helps agents track Git repositories across GitHub, GitLab, Gitee, and other Git platforms, pull updates, and summarize code changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gushenjie](https://clawhub.ai/user/gushenjie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to add, list, remove, and check monitored Git repositories, then receive concise update summaries through the agent and optional Feishu notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run broad Git operations, including cloning, fetching, and resetting local repositories. <br>
Mitigation: Use it only with repositories intentionally selected for monitoring, review the repository list before checks, and avoid paths where uncommitted local work could be overwritten. <br>
Risk: The skill can reuse Feishu credentials and send repository update summaries outside the local environment. <br>
Mitigation: Confirm the Feishu app, chat target, and least-privilege credentials before enabling notifications. <br>
Risk: Untrusted branch names or unusual repository inputs can affect command execution behavior. <br>
Mitigation: Use trusted repository URLs and ordinary branch names, and review configured entries before scheduled or repeated checks. <br>


## Reference(s): <br>
- [ClawHub Git Monitor page](https://clawhub.ai/gushenjie/git-monitor) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with optional JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May clone or update configured repositories and may send update summaries to Feishu when credentials are configured.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
