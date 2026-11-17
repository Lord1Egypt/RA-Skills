## Description:

Finds and retrieves public Xiaohongshu notes, creator post lists, note details, and comments for competitive research, trend monitoring, and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, marketers, and analysts use this skill to collect structured public Xiaohongshu search results, note details, comments, and creator posts for follow-on analysis or reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, Xiaohongshu URLs, URL xsec_token parameters, and GUAIKEI_API_TOKEN are sent to the third-party guaikei.com API.

Mitigation: Use only approved public Xiaohongshu inputs, treat the API token as sensitive, and rotate the token if it may have been exposed.

Risk: Retrieved public data and Xiaohongshu URL tokens may be saved in local plaintext logs.

Mitigation: Review the logs directory after use, restrict access to generated files, and delete logs that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-note-finder)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output may include request metadata, status fields, errors, and public Xiaohongshu data saved to local log files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
