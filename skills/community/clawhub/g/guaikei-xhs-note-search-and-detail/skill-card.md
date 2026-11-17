## Description:

Searches Xiaohongshu public notes, note details, comments, and creator posts so agents can gather structured inputs for content research, competitor monitoring, trend analysis, and KOL screening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content operators, analysts, and agent developers use this skill to retrieve public Xiaohongshu search results, note details, comments, and creator post lists for downstream summaries, comparisons, and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu targets and GUAIKEI_API_TOKEN-backed requests to a third-party API service.

Mitigation: Use only approved tokens, confirm that the data-sharing path through www.guaikei.com is permitted, and avoid submitting private or login-only targets.

Risk: Command output may be saved locally under logs/ and can include research targets, comments, or token-bearing URLs.

Mitigation: Protect the logs/ directory, remove generated files after use, and avoid sharing logs outside the approved workspace.

Risk: The skill is limited to public Xiaohongshu data and can return empty or error results for deleted, private, inaccessible, or invalid targets.

Mitigation: Treat empty and error responses as retrieval status, not facts about the target, and verify important conclusions with the original public source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-note-search-and-detail)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Node.js command examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require GUAIKEI_API_TOKEN and may save retrieved results under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
