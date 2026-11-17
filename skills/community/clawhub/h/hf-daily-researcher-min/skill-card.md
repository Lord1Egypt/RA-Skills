## Description:

HF Daily Researcher Min helps agents track HuggingFace Daily Papers and arXiv papers, choose between recent-paper scans and deeper research workflows, and produce research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomfoxxxx](https://clawhub.ai/user/tomfoxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research operations teams use this skill to monitor new HuggingFace Daily Papers and arXiv work, prioritize papers for closer reading, analyze trends, and generate weekly, monthly, or deep-dive research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may inspect persistent user memory for research topics, which can select unintended or stale research focus areas.

Mitigation: Prefer explicit topic entry for each run and review configuration before starting scheduled or deep research workflows.

Risk: Generated reports may be uploaded to Feishu without a clear consent boundary.

Mitigation: Use local-only report saving by default and require per-run confirmation before any Feishu or other cloud publication.

Risk: Cron-style scheduled operation can repeatedly run searches, spawn agents, and create reports without fresh human review.

Mitigation: Enable scheduling only after confirming scope, destination, and cadence, and review each report before sharing it externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomfoxxxx/skills/hf-daily-researcher-min)
- [arXiv API query endpoint](https://export.arxiv.org/api/query?search_query={query}&max_results=50)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with intermediate JSON and Markdown working files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save local report files and intermediate research artifacts; optional Feishu publication is described by the artifact.]

## Skill Version(s):

4.1.4 (source: server release metadata and artifact/config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
