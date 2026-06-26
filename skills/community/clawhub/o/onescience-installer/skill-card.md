## Description: <br>
Guide remote installation of OneScience on DCU clusters via SSH with strict remote-only execution rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onescience-ai](https://clawhub.ai/user/onescience-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and guide remote OneScience installation on SSH-accessible DCU cluster environments for selected science domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks to inspect local SSH configuration before the user chooses or confirms a host. <br>
Mitigation: Ask it to show a redacted host list first, then explicitly confirm the exact remote host before any SSH command is proposed or run. <br>
Risk: The workflow can run installation commands on a remote cluster account. <br>
Mitigation: Require the full remote command plan, selected domain, and verification steps to be shown before execution. <br>
Risk: Installation may fail because of missing SSH configuration, unavailable cluster modules, permission issues, or repository setup problems. <br>
Mitigation: Use the environment check and require the failing step and likely cause to be reported before retrying. <br>


## Reference(s): <br>
- [Domain Map](artifact/docs/domain-map.md) <br>
- [Install Sequence](artifact/docs/install-sequence.md) <br>
- [OneScience Skills Homepage](https://github.com/onescience-ai/oneskills) <br>
- [OneScience Repository](https://gitee.com/onescience-ai/onescience) <br>
- [ClawHub Skill Page](https://clawhub.ai/onescience-ai/onescience-installer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with structured text, YAML plan sections, and remote shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment check, install plan, remote commands, verification steps, and risk notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
