## Description: <br>
No.0 monitors AI agent cognitive files and sensitive local data access, detecting tampering while supporting rollback, classification, authorization, and audit workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanghaoyu-xiaolu](https://clawhub.ai/user/wanghaoyu-xiaolu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams running OpenClaw agents use this skill to watch cognitive identity files, review unauthorized changes, and roll back tampering. Teams handling sensitive local data can optionally add the DLC layer for classification, authorization prompts, MFA, and audit logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change agent control files and runtime state on the local machine. <br>
Mitigation: Review the code and test installation, monitoring, rollback, and uninstall behavior in a disposable workspace before using it with production agent memory. <br>
Risk: The DLC access-control layer is weaker than advertised and should not be treated as non-bypassable access control or strong MFA by default. <br>
Mitigation: Use it as a supplemental control unless fail-open paths, notification escaping, logging minimization, and install packaging have been hardened and reviewed. <br>
Risk: Examples and classification flows may involve sensitive credentials or private-key paths. <br>
Mitigation: Do not run examples against real private keys, wallet material, or production credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wanghaoyu-xiaolu/no0-skill) <br>
- [No.0 Quickstart](artifact/QUICKSTART.md) <br>
- [No.0 Installation Guide](artifact/INSTALL.md) <br>
- [No.0 Event Schema](artifact/docs/event_schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local installation, monitoring, rollback, classification, authorization, and audit guidance for agent workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
