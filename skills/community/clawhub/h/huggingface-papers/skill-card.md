## Description:

Look up and read Hugging Face paper pages in markdown, and use the papers API for structured metadata such as authors, linked models/datasets/spaces, Github repo and project page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huggingface](https://clawhub.ai/user/huggingface)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical writers use this skill to fetch Hugging Face paper pages, retrieve structured paper metadata, and analyze AI research papers from Hugging Face or arXiv identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Hugging Face write actions can change account or public paper state.

Mitigation: Do not provide HF_TOKEN for normal summaries or analysis; when a token is required, use a narrowly scoped token and require explicit confirmation before claim, index, or link update actions.

Risk: The release evidence security verdict is suspicious because write actions lack clear confirmation guidance.

Mitigation: Install only when paper administration capabilities are intended, and review any command that uses authenticated endpoints before execution.

## Reference(s):

- [Hugging Face Papers](https://huggingface.co/papers/{PAPER_ID})
- [Hugging Face Papers Markdown](https://huggingface.co/papers/{PAPER_ID}.md)
- [Hugging Face Papers API](https://huggingface.co/api/papers/{PAPER_ID})
- [arXiv Abstract](https://arxiv.org/abs/{PAPER_ID})
- [arXiv PDF](https://arxiv.org/pdf/{PAPER_ID})
- [ClawHub Skill Page](https://clawhub.ai/huggingface/skills/huggingface-papers)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference public Hugging Face and arXiv pages; authenticated write endpoints require HF_TOKEN.]

## Skill Version(s):

1.0.10 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
