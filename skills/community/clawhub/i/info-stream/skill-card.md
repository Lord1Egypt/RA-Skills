## Description: <br>
Daily News Collector helps an agent collect, curate, cache, and distribute daily technology news digests using scheduled collection and delivery workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgy2020](https://clawhub.ai/user/lgy2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure automated daily news digests for a chosen topic, including source selection, collection, anti-duplication checks, cached Markdown reports, and chat delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may set up unattended daily automation that runs in the background. <br>
Mitigation: Confirm the exact cron entries, report file path, chat destination, pause and deletion steps, and API key revocation process before enabling the jobs. <br>
Risk: The skill uses a Tavily API key for AI search. <br>
Mitigation: Store TAVILY_API_KEY only in the intended environment, limit access to it, and revoke or rotate it if the automation is disabled or exposed. <br>
Risk: Automated collection and distribution can publish incorrect, stale, or duplicate news. <br>
Mitigation: Keep the collection and distribution jobs separate, preserve the date-header duplicate checks, and review source quality before relying on the digest. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lgy2020/info-stream) <br>
- [Usage guide](references/usage-guide.md) <br>
- [Tavily setup](references/tavily-setup.md) <br>
- [Information source reference](references/sources.md) <br>
- [Tavily](https://tavily.com) <br>
- [Hacker News](https://news.ycombinator.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cached weekly Markdown reports and scheduled collection and distribution configuration; Tavily-based search requires TAVILY_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
