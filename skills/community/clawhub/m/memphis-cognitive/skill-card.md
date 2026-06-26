## Description: <br>
Memphis Cognitive is a documentation-only OpenClaw skill that guides agents and users through installing and using the separate Memphis CLI for decision capture, memory search, reflection, knowledge graphs, and multi-agent synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elathoxu-crypto](https://clawhub.ai/user/elathoxu-crypto) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to add decision-first memory workflows to OpenClaw agents. It provides guidance and command examples for journaling, decision tracking, semantic recall, prediction, reflection, knowledge graphs, and multi-agent synchronization through the separately installed Memphis CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installation guidance includes remote shell installers, including commands that may run privileged setup steps. <br>
Mitigation: Review installer scripts before execution, prefer a pinned release or manually inspected install, and avoid sudo-piped setup commands unless the source is trusted. <br>
Risk: Memphis memory, trade, and share-sync workflows may contain or export private project, business, decision, journal, or reflection data. <br>
Mitigation: Treat Memphis memory as sensitive data and use trade or share-sync only with trusted peers after checking exactly which blocks will be exported. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/elathoxu-crypto/memphis-cognitive) <br>
- [Memphis Repository](https://github.com/elathoxu-crypto/memphis) <br>
- [Memphis Documentation](https://github.com/elathoxu-crypto/memphis/tree/master/docs) <br>
- [Memphis Installer Script](https://raw.githubusercontent.com/elathoxu-crypto/memphis/main/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only meta-package; the included wrapper forwards arguments to a locally installed Memphis CLI.] <br>

## Skill Version(s): <br>
3.7.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
