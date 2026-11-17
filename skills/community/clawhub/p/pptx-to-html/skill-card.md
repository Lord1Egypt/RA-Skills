## Description:

Convert PowerPoint (.pptx) presentations to HTML using MinerU.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, web publishers, and content teams use this skill to convert PowerPoint slide decks from local files or URLs into HTML for web display, embedding, or publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow gives the MinerU CLI access to a MINERU_TOKEN and presentation content.

Mitigation: Use the skill only with presentations suitable for the MinerU service and manage MINERU_TOKEN as a credential.

Risk: Installing the CLI with latest-version package commands can reduce reproducibility.

Mitigation: Review the MinerU CLI source or pin a specific mineru-open-api version when reproducible installs matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzlzyca/skills/pptx-to-html)
- [MinerU homepage](https://mineru.net)
- [MinerU token management](https://mineru.net/apiManage/token)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated workflow expects the mineru-open-api command and a MINERU_TOKEN credential.]

## Skill Version(s):

0.4.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
