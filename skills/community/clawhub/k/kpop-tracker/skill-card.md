## Description: <br>
Track K-Pop idol updates including comebacks, albums, concerts, solo activities, merchandise, official YouTube content, and Chinese member Weibo activity using official, media, and Taiwan fan sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryemco](https://clawhub.ai/user/ryemco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to monitor followed K-Pop artists and groups for comeback schedules, album and merchandise information, concerts, events, official videos, and member solo activity. The skill summarizes findings in Traditional Chinese with source links and can optionally help maintain a local tracked-artist configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may browse public social, fan, media, and store sources and keep followed-artist configuration plus reported links in the workspace. <br>
Mitigation: Install only if that local state and browsing behavior are acceptable, and review the configured artist sources before use. <br>
Risk: Ticket, merchandise, signed-album, and price information can change or be inaccurate across fan and marketplace sources. <br>
Mitigation: Verify purchase, ticketing, and price details on official stores or event sites before acting. <br>
Risk: Optional automatic checks can continue producing twice-daily reports after setup. <br>
Mitigation: Enable scheduled checks only on explicit request, review the cron jobs, and remove them when reports are no longer wanted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ryemco/kpop-tracker) <br>
- [Config Examples](references/config_examples.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown summaries in Traditional Chinese, with source links, tables, local JSON configuration examples, and optional shell commands for scheduled checks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses browser access for public K-pop, social, fan, and store sources; keeps followed artists and reported links in local workspace files when configured.] <br>

## Skill Version(s): <br>
v2.1.0 (source: server release metadata, SKILL.md metadata.openclaw.version, and CHANGELOG released 2026-04-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
