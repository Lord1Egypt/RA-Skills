## Description:

Fetch, classify, and summarize papers from multiple sources (arXiv, etc.) with AI-powered multi-language summaries and email delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pigeondan1](https://clawhub.ai/user/pigeondan1)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, research teams, and agents use this skill to configure research-paper sources, classify papers by field, generate multilingual summaries, and send daily paper digests by email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example code can execute a Python script outside the reviewed skill package.

Mitigation: Review and correct the skill root path handling, and ensure the target script is packaged inside the reviewed skill directory before execution.

Risk: The skill can send email digests and change recipient or source configuration.

Mitigation: Require explicit operator confirmation before sending email or modifying recipients, sources, categories, or language settings.

Risk: The skill depends on SMTP credentials and optional LLM provider API keys.

Mitigation: Provide credentials through environment variables, keep recipient and secret files out of shared outputs, and rotate credentials if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pigeondan1/skills/paperclaw)
- [Project homepage from artifact metadata](https://github.com/PigeonDan1/paper_claw)
- [arXiv Computation and Language recent papers](https://arxiv.org/list/cs.CL/recent)
- [arXiv Computer Vision and Pattern Recognition recent papers](https://arxiv.org/list/cs.CV/recent)
- [arXiv Machine Learning recent papers](https://arxiv.org/list/cs.LG/recent)
- [arXiv Artificial Intelligence recent papers](https://arxiv.org/list/cs.AI/recent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown digests, JSON data, configuration snippets, Python helper results, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update local configuration files and can send email digests when SMTP settings and recipients are configured.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
