## Description:

Searches Xiaohongshu public notes and retrieves note details, author and engagement data, creator posts, comments, and links for social content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content operators, marketers, and analysts use this skill to retrieve public Xiaohongshu notes, note details, creator posts, and comments for content research, competitor monitoring, KOL screening, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, Xiaohongshu URLs, and the Guaikei API token are sent to guaikei.com during command execution.

Mitigation: Use the skill only where sending those inputs to Guaikei is approved, avoid sensitive search terms or links, and rotate the token if request URLs may have been exposed.

Risk: Command output can be automatically saved to local logs, which may retain search terms, source URLs, returned public-data records, and analysis inputs.

Mitigation: Run in a private workspace, restrict access to the logs directory, treat generated logs as sensitive, and delete logs when they are no longer needed.

## Reference(s):

- [Guaikei API website](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-data-tool)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; CLI commands return structured JSON for Xiaohongshu public-data retrieval.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and a GUAIKEI_API_TOKEN; command results may be saved under local logs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
