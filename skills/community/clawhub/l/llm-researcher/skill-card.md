## Description:

Analyzes LLM-related papers and GitHub projects, then classifies and organizes them by specified categories to track recent progress and research directions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runshengdu](https://clawhub.ai/user/runshengdu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical teams use this skill to collect recent LLM papers and GitHub projects from configured sources, analyze them, classify them by the bundled taxonomy, and generate a traceable Markdown research report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends public arXiv PDF URLs to MinerU and requires network access plus MINERU_API_KEY.

Mitigation: Use it only for PDFs and environments suitable for third-party parsing, and keep MINERU_API_KEY scoped to this workflow.

Risk: The workflow deletes tmp_llm_research after writing the final report.

Mitigation: Run it from a workspace where any existing tmp_llm_research folder is disposable.

Risk: Research summaries can be incomplete when source pages, PDFs, or repositories cannot be retrieved reliably.

Mitigation: Preserve original links in the report and state retrieval limitations clearly for failed or partial entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runshengdu/skills/llm-researcher)
- [Category taxonomy](artifact/references/categories.md)
- [MinerU API documentation](https://mineru.net/apiManage/docs)
- [alphaxiv hot papers](https://www.alphaxiv.org/?sort=Hot&interval=7+Days)
- [alphaxiv GitHub-sourced papers](https://www.alphaxiv.org/?source=GitHub&interval=7+Days&sort=Hot)
- [GitHub Trending](https://github.com/trending?since=weekly)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with categorized research entries, preserved source links, and a trend summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a timestamped report under output/ and uses temporary Markdown files during processing.]

## Skill Version(s):

1.0.6 (source: release evidence and frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
