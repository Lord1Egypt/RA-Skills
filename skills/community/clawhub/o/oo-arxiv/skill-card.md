## Description: <br>
Provides OOMOL oo CLI guidance for searching arXiv and retrieving paper metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to direct an agent to search arXiv, inspect action schemas, and fetch paper metadata through the OOMOL oo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-time setup can install the OOMOL oo CLI or start an OOMOL login flow. <br>
Mitigation: Run setup only when an oo command fails for that reason and only with intentional user approval; routine arXiv lookups are read-only. <br>
Risk: Live connector actions require payloads that match the current action schema. <br>
Mitigation: Inspect the action schema with oo connector schema before running oo connector run. <br>


## Reference(s): <br>
- [arXiv](https://arxiv.org/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-oriented arXiv connector actions are run through the oo CLI after inspecting live action schemas.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
