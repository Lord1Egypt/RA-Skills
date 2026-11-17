## Description:

Researches topics by searching Lowyat forum, scraping selected forum threads into Excel spreadsheets, and helping analyze the resulting discussions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superoo7](https://clawhub.ai/user/superoo7)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and developers use this skill to gather public Lowyat forum discussions about Malaysian consumer topics, export selected threads to spreadsheets, and synthesize opinions, recommendations, price ranges, warnings, and user experiences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scraper can fetch arbitrary user-supplied URLs.

Mitigation: Run it in a constrained environment and provide only forum.lowyat.net topic URLs.

Risk: Untrusted forum text is written into Excel spreadsheets without spreadsheet-safety handling.

Mitigation: Treat generated spreadsheets as untrusted content and add formula neutralization for Excel cells before wider use.

Risk: Network requests and dependency resolution may behave unexpectedly without explicit controls.

Mitigation: Add URL allowlisting, redirect and timeout controls, clearer file-write disclosure, and pinned dependency versions.

## Reference(s):

- [Lowyat Forum](https://forum.lowyat.net)
- [uv Documentation](https://docs.astral.sh/uv/)
- [ClawHub Skill Page](https://clawhub.ai/superoo7/skills/lowyat-forum-research)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown analysis with shell commands and Excel .xlsx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scraper writes one .xlsx file per forum topic with Name, Date, and Comment columns.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
