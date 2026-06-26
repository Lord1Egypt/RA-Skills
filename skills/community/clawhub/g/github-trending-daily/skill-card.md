## Description: <br>
Fetches daily, weekly, or monthly GitHub Trending repositories and formats them for DingTalk group delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangzhiyu](https://clawhub.ai/user/jiangzhiyu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and team operators use this skill to monitor GitHub Trending projects and share recurring Markdown summaries to a DingTalk group. It supports daily, weekly, monthly, dry-run, and no-push modes for testing and scheduled delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends messages by default to a hardcoded DingTalk webhook that the installer may not control. <br>
Mitigation: Replace the embedded webhook with local configuration before use, then test with --dry-run or --no-push before enabling delivery. <br>
Risk: Cron examples can create recurring automated posts. <br>
Mitigation: Add scheduled cron entries only after confirming the destination webhook and desired posting frequency. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiangzhiyu/github-trending-daily) <br>
- [GitHub Trending](https://github.com/trending) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, terminal status text, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can post to DingTalk by default; dry-run and no-push modes support testing without delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
