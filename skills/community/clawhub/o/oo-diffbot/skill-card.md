## Description: <br>
Diffbot (diffbot.com). Use this skill for Diffbot requests involving searching and reading data through the OOMOL-backed Diffbot connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect the live Diffbot connector schema and run Diffbot article extraction through the oo CLI. It supports extracting normalized article data from a public URL without directly handling raw Diffbot API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Diffbot credentials to be brokered by OOMOL. <br>
Mitigation: Install only when the user accepts OOMOL as the credential broker and understands that connector actions run through the oo CLI. <br>
Risk: The documented remote installer commands execute installer scripts for the oo CLI. <br>
Mitigation: Review the oo CLI installer before running the install commands. <br>
Risk: Future Diffbot connector actions could write, delete, or change account data if such actions are added. <br>
Mitigation: Keep explicit user confirmation for any connector action marked write or destructive, including the exact payload and intended effect. <br>


## Reference(s): <br>
- [Diffbot homepage](https://www.diffbot.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-diffbot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include data and meta.executionId fields when actions run successfully.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
