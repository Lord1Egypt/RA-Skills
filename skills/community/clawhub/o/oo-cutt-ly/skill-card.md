## Description: <br>
Cuttly (cutt.ly) helps an agent inspect Cuttly action schemas, retrieve link analytics, and create short URLs through the OOMOL-connected Cuttly connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate Cuttly through an OOMOL-connected account, including reading analytics for short links and creating new Cuttly short URLs after inspecting the live connector schema. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create Cuttly short URLs with a connected account and the security summary says this state-changing action is under-disclosed and under-controlled. <br>
Mitigation: Require explicit user confirmation of the exact shorten_url payload and expected effect before running URL creation commands. <br>
Risk: The skill requires sensitive credentials through the OOMOL-connected Cuttly connector. <br>
Mitigation: Use the connector only after schema inspection, avoid exposing raw tokens, and review first-time CLI or connection setup before proceeding. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-cutt-ly) <br>
- [Cuttly Homepage](https://cutt.ly) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce credentialed Cuttly connector commands that read analytics or create short URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
