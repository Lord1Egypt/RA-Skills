## Description:

This command skill helps agents search public Xiaohongshu notes, retrieve note details and comments, and collect public creator posts for content, competitor, KOL, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing, content, social media, and data-analysis users use this skill to gather structured public Xiaohongshu data for trend research, competitor monitoring, creator screening, and comment insight workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the Guaikei API token, Xiaohongshu links, keywords, and related user inputs to Guaikei.

Mitigation: Use a limited API token where possible, avoid sensitive or regulated inputs, and confirm that the data transfer is authorized.

Risk: Fetched Xiaohongshu results are automatically stored locally in a logs directory.

Mitigation: Inspect and delete generated logs regularly, especially after collecting comments, creator data, or commercially sensitive research.

Risk: The skill is intended only for public Xiaohongshu data and does not support private, hidden, or login-gated content.

Mitigation: Use only public keywords and links, and do not use the skill for private accounts, hidden content, publishing, liking, or other account interactions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-search-detail-comment)
- [Guaikei API service](https://www.guaikei.com)
- [Options and calling guide](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON stdout and JSON log files, with agent-facing command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; command results are saved under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
