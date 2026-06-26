## Description: <br>
AI News Digest helps agents generate daily or weekly AI and technology news briefings with structured summaries, topic grouping, optional formats, and optional email delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and content teams can use this skill to produce recurring AI and technology news digests for personal tracking, newsletters, or internal briefings. It is most useful when the user wants structured summaries that can be reviewed before publishing or emailing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or aggregated news summaries may be inaccurate, stale, or unsuitable for publication without review. <br>
Mitigation: Review digest content and source coverage before sharing it with readers or internal stakeholders. <br>
Risk: Email delivery can expose recipient lists or send unwanted messages if SMTP credentials or targets are misconfigured. <br>
Mitigation: Use revocable app-specific SMTP credentials or a secret manager, limit recipients, and test delivery before enabling routine sends. <br>
Risk: Scheduled cron execution can create recurring output or email activity beyond the user's intent. <br>
Mitigation: Add cron entries only after confirming the desired cadence, destination, and generated content review process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/new-ai-news-digest) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown news digest with documented options for HTML or plain-text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional email delivery and recurring cron examples require user-provided SMTP configuration and intentional scheduling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
