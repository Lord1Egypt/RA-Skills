## Description:

Fetches structured JSON for Xiaohongshu public-content keyword searches, note details, note comments, and creator post monitoring through the Guaikei API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content, marketing, and analysis teams use this skill to collect public Xiaohongshu notes, comments, creator posts, and engagement signals for topic research, competitor monitoring, KOL screening, and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, links, and the GUAIKEI_API_TOKEN are sent to Guaikei.

Mitigation: Use the skill only with approved targets and an authorized Guaikei token; avoid submitting sensitive research topics or links.

Risk: Retrieved content is automatically saved locally under logs/ without redaction.

Mitigation: Run in a private workspace, clear generated logs when finished, and avoid shared terminals or directories for sensitive work.

Risk: The API token could be exposed through terminal captures, logs, or shared environments.

Mitigation: Store the token in a managed environment variable or secret store and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xiaohongshu-content-monitor)
- [engheng-art publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Files, Guidance]

**Output Format:** [Structured JSON written to stdout and archived under logs/]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and accepts Xiaohongshu keywords, note URLs, profile URLs, filters, and result limits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
