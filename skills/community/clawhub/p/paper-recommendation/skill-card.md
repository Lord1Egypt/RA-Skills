## Description:

Automates discovery, parallel review, scoring, and briefing generation of AI research papers from arXiv, supporting daily updates and PDF analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sjf-ecnu](https://clawhub.ai/user/sjf-ecnu)

### License/Terms of Use:


## Use Case:

Developers and research teams use this skill to find recent AI papers, generate parallel review tasks, score recommendations, and produce concise research briefings. It is especially suited to recurring literature-monitoring workflows that combine arXiv discovery, PDF extraction, and Markdown summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring automation can send generated briefings and local file paths to a fixed Telegram recipient.

Mitigation: Before enabling cron or delivery, replace the Telegram target with an account you control and review outgoing content.

Risk: The workflow can download PDFs and create files under the user's account on a recurring schedule.

Mitigation: Run it in a controlled workspace with expected storage limits and review scheduled commands before installation.

## Reference(s):

- [Paper Recommendation on ClawHub](https://clawhub.ai/sjf-ecnu/skills/paper-recommendation)
- [arXiv API endpoint used for paper discovery](https://export.arxiv.org/api/query)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact workflow documentation](artifact/WORKFLOW.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown briefings, JSON task payloads, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create downloaded PDF files and briefing files under the user's paper directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
