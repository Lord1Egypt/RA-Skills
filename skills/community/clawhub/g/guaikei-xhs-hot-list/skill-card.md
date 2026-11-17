## Description:

Searches public Xiaohongshu notes, retrieves note details and comments, and fetches author posts for content research, competitor monitoring, KOL screening, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketing teams, data analysts, and business operators use this skill to collect public Xiaohongshu note, comment, and author-post data for topic research, competitor monitoring, KOL evaluation, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords or links and the Guaikei API token to www.guaikei.com.

Mitigation: Use only with authorization to share those inputs with Guaikei, keep GUAIKEI_API_TOKEN in environment configuration, and rotate the token if URLs or logs may have exposed it.

Risk: The skill automatically saves full command results locally, which may include business research, comments, profile data, and tokenized Xiaohongshu links.

Mitigation: Restrict access to the logs directory, avoid sharing raw logs, and delete or protect generated logs after use.

Risk: The skill is limited to public Xiaohongshu data and depends on a third-party API service.

Mitigation: Confirm the requested data is public and allowed for the intended use, and treat API failures or empty results as inconclusive rather than fabricating findings.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/guaikei-xhs-hot-list)
- [Guaikei API website](https://www.guaikei.com)
- [Artifact README](artifact/readme.md)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, text, guidance]

**Output Format:** [JSON command output with local JSON log files and markdown/bash usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; command outputs include status, request metadata, skill metadata, and results or error details.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package and skill metadata report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
