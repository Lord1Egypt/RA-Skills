## Description:

Fetch and digest HuggingFace Daily Papers for daily paper reports, including paper metadata retrieval, scoring, and formatted commentary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godiao](https://clawhub.ai/user/godiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and external users use this skill to fetch Hugging Face Daily Papers for a selected date and turn the results into a concise research digest with scores, summaries, and commentary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fetch script requires a Hugging Face token.

Mitigation: Use a minimally scoped read token and avoid broad personal tokens when possible.

Risk: The fetch script creates or overwrites hf_results.json in its working directory.

Mitigation: Run it from the intended scripts directory or an isolated working directory before reviewing the generated digest input.

Risk: Generated commentary may overstate paper significance or reflect the skill's default author-branded tone.

Mitigation: Review the digest before sharing and override tone or branding requirements in the prompt when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godiao/skills/hf-daily-papers)
- [Publisher profile](https://clawhub.ai/user/godiao)
- [Hugging Face](https://huggingface.co)
- [Hugging Face Daily Papers](https://huggingface.co/papers)
- [Hugging Face access tokens](https://huggingface.co/settings/tokens)
- [arXiv abstract pages](https://arxiv.org/abs/{paper_id})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown digest plus JSON intermediate file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The fetcher writes hf_results.json in the script working directory and the agent uses it to produce a ranked paper digest.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
