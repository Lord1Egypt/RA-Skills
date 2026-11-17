## Description:

Generates Morgan Stanley style investment presentation PPTX decks for roadshows, pitch books, investment committee memos, coverage initiations, and quarterly earnings updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjkj999999](https://clawhub.ai/user/yjkj999999)

### License/Terms of Use:

MIT

## Use Case:

External analysts, investment professionals, and developers use this skill to generate structured investment presentation decks from financial and narrative inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated decks may contain inaccurate source labels, branding, disclosures, or financial claims.

Mitigation: Review generated presentations for factual accuracy, source labeling, branding permissions, disclosures, and financial claims before sharing them.

Risk: The skill writes local PPTX files and creates output directories.

Mitigation: Run it in a virtual environment and choose an output path that is appropriate for the workspace.

Risk: The PowerPoint generation path depends on python-pptx.

Mitigation: Pin python-pptx to a reviewed version before use in managed or production workflows.

## Reference(s):

- [README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/yjkj999999/skills/ms-investment-deck)
- [Publisher Profile](https://clawhub.ai/user/yjkj999999)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [PPTX files generated through a Python API or CLI, with supporting Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local .pptx decks from structured investment-deck data and supports zh, en, and bilingual language modes.]

## Skill Version(s):

1.1.0 (source: release evidence and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
