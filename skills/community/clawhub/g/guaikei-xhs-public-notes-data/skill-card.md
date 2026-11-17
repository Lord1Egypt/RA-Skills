## Description:

Searches public Xiaohongshu notes by keyword and retrieves public note details, comments, and creator post histories for social content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, marketers, and analysts use this skill to gather public Xiaohongshu search results, note details, comment data, and creator post histories for topic research, competitor monitoring, KOL screening, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive Xiaohongshu research terms, note URLs, profile URLs, and the Guaikei API token may be exposed through API requests or operational traces.

Mitigation: Use the skill only for approved public-data workflows, avoid sensitive queries, restrict token access, and rotate the token if logs or infrastructure traces may have exposed it.

Risk: Returned Xiaohongshu data is automatically saved under logs/.

Mitigation: Protect the logs/ directory, avoid committing generated outputs, and delete old result files when they are no longer needed.

Risk: The security verdict is suspicious due to token handling and persisted result data.

Mitigation: Review the skill before installation and confirm that data sharing with Guaikei and local retention under logs/ are acceptable for the intended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-public-notes-data)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Files, Guidance]

**Output Format:** [JSON on stdout with optional Markdown or narrative analysis by the calling agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can save returned public Xiaohongshu data under logs/ and require GUAIKEI_API_TOKEN.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
