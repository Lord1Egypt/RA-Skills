## Description:

PPTX Parse helps agents parse PowerPoint (.pptx) presentations into structured Markdown with MinerU while preserving slide organization and content hierarchy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content pipeline builders use this skill to have an agent extract structure, slide text, and hierarchy from .pptx presentations for analysis or downstream Markdown workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PowerPoint decks may contain confidential or regulated information when processed with MinerU.

Mitigation: Confirm MinerU's data handling is acceptable for the presentation contents before installing or running the parser.

Risk: The external mineru-open-api dependency may change behavior or introduce supply-chain risk if installed without review.

Mitigation: Prefer a pinned or reviewed mineru-open-api version before using the skill in routine workflows.

Risk: Full parsing uses an authentication token and local presentation files.

Mitigation: Run parsing with only the files and MINERU_TOKEN needed for the task.

## Reference(s):

- [PPTX Parse ClawHub release](https://clawhub.ai/mzlzyca/skills/pptx-parse)
- [MinerU homepage](https://mineru.net)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)
- [MinerU token management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples; parsing output is structured Markdown from MinerU.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full parsing requires MINERU_TOKEN; quick flash-extract works without a token and supports .pptx inputs from local files or URLs.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
