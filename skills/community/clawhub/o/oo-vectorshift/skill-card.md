## Description: <br>
Operate VectorShift through an OOMOL-connected account to list, fetch, and run VectorShift pipelines with schema-checked JSON inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with VectorShift pipelines through OOMOL's connected VectorShift connector, including listing accessible pipelines, fetching pipeline details, and running single or bulk pipeline executions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The first-time setup path includes an installer command that downloads and executes a remote script. <br>
Mitigation: Use OOMOL's documented install path or review the oo CLI installer source before running the setup command. <br>
Risk: Running VectorShift pipelines may send payload data to connected services and may affect account usage or billing. <br>
Mitigation: Install and use the skill only when OOMOL is intended as an intermediary for VectorShift, and confirm pipeline payloads before execution. <br>
Risk: Pipeline actions depend on the current connector schema and connected account state. <br>
Mitigation: Fetch the live connector schema before constructing payloads and retry setup only when authentication, connection, or billing errors indicate it is needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-vectorshift) <br>
- [VectorShift Homepage](https://vectorshift.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution so payloads match the current VectorShift action contract.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
