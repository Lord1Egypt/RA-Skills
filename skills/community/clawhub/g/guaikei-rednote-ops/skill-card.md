## Description:

Retrieves public Xiaohongshu/Rednote search results, note details, creator posts, and comments as structured JSON for content research, competitor monitoring, KOL screening, trend tracking, and audience-feedback analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, analysts, content creators, and agents use this skill to retrieve public Xiaohongshu/Rednote data for content research, competitor monitoring, KOL screening, trend tracking, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated logs and command output can contain research history, comments, profile data, and tokenized Xiaohongshu URLs.

Mitigation: Run the skill in a private workspace, protect or delete generated logs, and share exports only with approved recipients.

Risk: Exposure of GUAIKEI_API_TOKEN can allow unauthorized API access.

Mitigation: Use a dedicated low-privilege token, keep it out of prompts and shared files, and rotate it if exposed.

Risk: The release description emphasizes comment retrieval while the artifact also supports keyword search, note detail, and creator post retrieval.

Mitigation: Review the selected CLI and requested action before execution, and limit use to public data and authorized analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-rednote-ops)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Structured JSON on stdout plus JSON log files and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; commands can return up to 10000 records when supported.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
