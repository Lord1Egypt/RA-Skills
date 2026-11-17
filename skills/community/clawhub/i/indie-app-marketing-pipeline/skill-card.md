## Description:

Template-driven multi-platform content pipeline for indie iOS developers that generates and schedules a full week of social posts for TikTok, YouTube Shorts, X/Twitter, and Facebook from a reusable content bank with zero LLM calls per day.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zakmcintyre](https://clawhub.ai/user/zakmcintyre)

### License/Terms of Use:

MIT-0

## Use Case:

Indie iOS app developers use this skill to plan reusable social content, generate weekly posting plans, and schedule daily posts through Postiz across TikTok, YouTube Shorts, X/Twitter, and Facebook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Editable content and configured video-generation commands can lead to local command execution.

Mitigation: Review all content-bank, plan, and configuration files before live runs; replace command-string execution with argument-based execFile or spawn before production use.

Risk: The setup flow stores a Postiz API key in a local .env file without strong safeguards.

Mitigation: Use a least-privilege Postiz key, protect the .env file with owner-only permissions, add it to .gitignore, and avoid overwriting existing secrets.

Risk: Automated cron publishing can post incorrect or unreviewed content to connected social accounts.

Mitigation: Dry-run the weekly planner and daily publisher, validate generated plans and content banks, and enable cron only after manual review.

## Reference(s):

- [Content Bank Guide](references/content-bank-guide.md)
- [Platform Strategy](references/platform-strategy.md)
- [Postiz](https://postiz.com)
- [Postiz docs](https://docs.postiz.com)
- [ClawHub skill page](https://clawhub.ai/zakmcintyre/skills/indie-app-marketing-pipeline)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON plan/configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a Postiz API key; writes local planning, configuration, history, and log files when scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
