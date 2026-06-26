## Description: <br>
Crawls structured Webnovel and ReelShorts content, grades updates, generates RSS feeds, and prepares DingTalk broadcasts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[7487](https://clawhub.ai/user/7487) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations teams use this skill to run targeted crawls for Webnovel and ReelShorts, persist structured items, grade updates, generate RSS or Atom feeds, and send DingTalk summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The crawler may bypass anti-bot controls or ignore robots.txt for some targets. <br>
Mitigation: Review each target site's terms and crawling policy before use, keep crawl scope narrow, and avoid scheduled crawling unless it is explicitly approved. <br>
Risk: DingTalk broadcasting requires webhook credentials. <br>
Mitigation: Set DINGTALK_WEBHOOK only in a controlled environment, avoid committing secrets, and rotate the webhook if exposure is suspected. <br>
Risk: The artifact includes an optional Claude development loop that can modify repository files. <br>
Mitigation: Do not run scripts/claude_loop.sh unless you intentionally want repo-modifying automation and have reviewed the working tree. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/7487/lp-lobster-crawler) <br>
- [Publisher profile](https://clawhub.ai/user/7487) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated crawler outputs include stored structured data, RSS or Atom feeds, and DingTalk Markdown messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv for setup and DINGTALK_WEBHOOK for DingTalk broadcast.] <br>

## Skill Version(s): <br>
0.7.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
