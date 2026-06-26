## Description: <br>
Brave Search (search.brave.com). Use this skill for Brave Search requests involving searching and reading web, image, news, or video results through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent perform Brave Search web, image, news, and video searches through an OOMOL-connected Brave Search account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The first-time setup path includes one-line installer commands that execute downloaded scripts. <br>
Mitigation: Review OOMOL's official install guide or installer script before running the installer; after setup, normal skill actions are read-only Brave Search operations. <br>
Risk: The skill requires connected Brave Search credentials through an OOMOL account. <br>
Mitigation: Use the OOMOL connection flow for Brave Search and avoid handling raw credentials in agent prompts or local skill files. <br>


## Reference(s): <br>
- [Brave Search homepage](https://search.brave.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed oo CLI, OOMOL sign-in, connected Brave Search credentials, and live schema inspection before action execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
