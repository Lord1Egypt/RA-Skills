## Description:

Paper Review Pro helps researchers search arXiv and Semantic Scholar, rank relevant papers, generate structured summaries, export BibTeX entries, and create research review reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alfredliang11](https://clawhub.ai/user/alfredliang11)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and developers use this skill to discover papers for a topic, compare candidate papers, summarize methods and findings, and export references for literature review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send paper content and an OpenClaw gateway token to a configurable LLM endpoint.

Mitigation: Use only trusted HTTPS or local gateway endpoints, use a dedicated limited token, and disable LLM features with --no-llm for confidential, unpublished, or proprietary paper content.

Risk: The skill makes outbound calls to arXiv, Semantic Scholar, OpenClaw Gateway, and possibly Dashscope.

Mitigation: Install and run it only in environments where those outbound network calls are acceptable for the searched topics and paper content.

Risk: The skill writes results under ~/.openclaw/paper-review-pro.

Mitigation: Review generated reports, BibTeX files, and configuration before sharing them or reusing them in other research workflows.

## Reference(s):

- [BibTeX Export Module](reference/BIBTEX_EXPORT.md)
- [LLM Integration](reference/LLM_INTEGRATION.md)
- [Publication Status and CCF Ranking](reference/PUBLICATION_STATUS.md)
- [Scoring System](reference/SCORING_SYSTEM.md)
- [Bugfix Notes](reference/BUGFIXES.md)

## Skill Output:

**Output Type(s):** [text, markdown, BibTeX, configuration, shell commands, guidance]

**Output Format:** [Markdown reports, BibTeX files, terminal text, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes paper records, BibTeX exports, reports, and configuration under ~/.openclaw/paper-review-pro.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
