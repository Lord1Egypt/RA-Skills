## Description:

Discover hot topics on X, enrich tweets one-by-one, score and summarize signals, generate one tweet draft, and optionally publish on schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vmining](https://clawhub.ai/user/vmining)

### License/Terms of Use:


## Use Case:

External developers and social media operators use this skill to discover public X trends, produce a concise briefing, generate a single tweet draft, and optionally publish it through X API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cron helper can create recurring public X posts without an extra confirmation or clear removal path.

Mitigation: Use draft-only runs first, avoid scripts/setup_cron.sh unless recurring public posting is intended, and review any scheduled job after creation.

Risk: Publishing requires X credentials capable of posting to an account.

Mitigation: Use narrowly scoped X credentials and provide posting credentials only when direct publication is required.

Risk: Tweet URLs are sent to FxTwitter during enrichment.

Mitigation: Treat FxTwitter as a third-party enrichment service and disable or review enrichment behavior if that data sharing is not acceptable.

Risk: Generated outputs are saved under outputs/x-hot by default.

Mitigation: Review latest.json and latest.txt before sharing or publishing because they can contain source tweet data, summaries, and draft content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vmining/skills/kiro-x-publisher)
- [Publisher profile](https://clawhub.ai/user/vmining)
- [X](https://x.com)
- [X API](https://api.x.com)
- [FxTwitter API](https://api.fxtwitter.com/{username}/status/{tweet_id})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [JSON files, plain-text briefings, tweet draft text, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes latest.json and latest.txt under outputs/x-hot by default; posting to X only occurs when the --post option is used.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
