## Description:

Ppt Extract helps agents extract PowerPoint presentation content into structured Markdown using the MinerU CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract content from .ppt and .pptx presentations, including local files and URLs, and convert the result into readable Markdown for documentation or content processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation content may be processed through token-backed MinerU services, which can be inappropriate for confidential slides unless the user accepts those data handling terms.

Mitigation: Do not use the skill on confidential presentations unless the organization has reviewed and accepted MinerU service handling for that content.

Risk: The skill depends on the third-party mineru-open-api CLI, so installer source or version drift could affect extraction behavior.

Mitigation: Install only from expected MinerU/OpenDataLab sources, avoid administrator privileges, and pin or review the CLI version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzlzyca/skills/ppt-extract)
- [MinerU homepage](https://mineru.net)
- [MinerU token management](https://mineru.net/apiManage/token)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Extraction requires mineru-open-api and a MINERU_TOKEN or interactive MinerU authentication; output may stream to stdout or be saved with an output directory.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
