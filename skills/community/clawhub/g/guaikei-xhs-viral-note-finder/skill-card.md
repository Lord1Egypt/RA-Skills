## Description:

Retrieves public Xiaohongshu search results, note details, creator posts, and comments through GUAIKEI-powered CLI commands for content research, competitor monitoring, trend analysis, KOL screening, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, brand marketers, social media operators, and analysts use this skill to collect public Xiaohongshu data for viral-note discovery, competitor monitoring, trend research, KOL screening, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu links, search terms, requested limits, and the GUAIKEI API token to guaikei.com.

Mitigation: Use a dedicated token with limited scope when possible and confirm that the requested analysis is appropriate for external processing.

Risk: Result logs may persist locally and can contain search terms, links, and retrieved public-data results.

Mitigation: Avoid sensitive investigations in shared workspaces, protect the logs directory, and delete generated logs when they are no longer needed.

Risk: The security review verdict is suspicious because token handling and saved results should be reviewed before installation.

Mitigation: Review the publisher's token handling and result-saving behavior before deployment; prefer explicit redaction or operational controls for generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-viral-note-finder)
- [GUAIKEI API service](https://www.guaikei.com)
- [Parameter and invocation guide](references/options.md)
- [Skill changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON status objects from CLI commands, with optional text or Markdown summaries from the calling agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save result JSON files under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter, package.json, and changelog report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
