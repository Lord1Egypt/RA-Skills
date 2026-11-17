## Description:

Monitor and fetch Hugging Face model trends with filters for task, library, and popularity metrics, plus structured output and optional JSON export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianxingleo](https://clawhub.ai/user/tianxingleo)

### License/Terms of Use:


## Use Case:

Developers, researchers, and model evaluators use this skill to discover popular Hugging Face models, compare model popularity by task or library, and export model listings for follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make network requests to Hugging Face, optionally through a proxy.

Mitigation: Use only proxy settings you trust and run the skill only when external Hugging Face API access is intended.

Risk: The skill can write JSON exports to paths supplied by the user.

Mitigation: Choose explicit output paths and review generated files before using them in downstream workflows.

Risk: The optional cron example creates recurring network access and log output.

Mitigation: Add scheduled execution only when recurring daily monitoring is desired.

Risk: The artifact notes that trending results are approximated from recent models sorted by popularity metrics.

Mitigation: Treat results as model-discovery signals rather than an authoritative Hugging Face trending ranking.

## Reference(s):

- [Hugging Face Hub model metadata documentation](https://huggingface.co/docs/huggingface_hub/guides/models)
- [ClawHub skill page](https://clawhub.ai/tianxingleo/skills/huggingface-trends)
- [Publisher profile](https://clawhub.ai/user/tianxingleo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, formatted terminal output, and optional JSON export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can make Hugging Face API requests through a user-provided HTTP proxy and can write JSON exports to user-specified paths.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
