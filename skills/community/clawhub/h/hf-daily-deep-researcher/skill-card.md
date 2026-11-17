## Description:

Tracks Hugging Face Daily Papers and arXiv with a multi-agent workflow to find new papers, read priority papers, analyze trends, and produce Markdown research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomfoxxxx](https://clawhub.ai/user/tomfoxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and technical teams use this skill to monitor configured AI research directions and produce weekly or monthly scans, deeper survey-style reports, prioritized paper lists, analysis, and quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read local profile and memory files to infer research interests during setup.

Mitigation: Review the generated config.json before use and manually set research_focus when local profile or memory-derived configuration is not desired.

Risk: Research topics and paper metadata may be sent to external services including arXiv, Hugging Face or its GitHub mirror, Kimi where available, and optionally Feishu after authorization.

Mitigation: Use only with research topics and metadata that are appropriate for those services, and keep cloud upload disabled unless Feishu authorization and destination settings have been reviewed.

Risk: The release was flagged suspicious because of broad external search and shell-fetch behavior.

Mitigation: Review the skill behavior and configuration before scheduled runs or deployment in shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomfoxxxx/skills/hf-daily-deep-researcher)
- [Hugging Face Daily Papers API](https://huggingface.co/api/daily_papers?date=YYYY-MM-DD)
- [Hugging Face Daily Papers page](https://huggingface.co/papers?date=YYYY-MM-DD)
- [arXiv API query endpoint](https://export.arxiv.org/api/query?search_query=all:KEYWORD&sortBy=submittedDate&sortOrder=descending&max_results=50)
- [Daily HuggingFace AI Papers GitHub mirror](https://raw.githubusercontent.com/AtharvaDomale/Daily-HuggingFace-AI-Papers/main/data/latest.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown research reports, structured paper notes, configuration updates, and quality-check summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save report and history files locally; optional Feishu upload is used only when configured and authorized.]

## Skill Version(s):

5.2.9 (source: evidence release, SKILL.md frontmatter, config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
