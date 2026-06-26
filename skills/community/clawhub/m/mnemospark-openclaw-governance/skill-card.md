## Description: <br>
Operate OpenClaw multi-agent governance with openclaw-gov: read-only audit, material change documentation, staged discovery, registry and runbook validation, and governance PR shipping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pawlsclick](https://clawhub.ai/user/pawlsclick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to maintain OpenClaw governance roots, run read-only audits, document material workflow changes, validate registry and runbook consistency, and prepare governance pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward file writes, branch creation, commits, pushes, PR creation, and AGENTS.md governance injection. <br>
Mitigation: Use the read-only audit workflow by default; allow mutating workflows only when the operator explicitly intends governance state changes. <br>
Risk: Auto-installing the pinned CLI source may introduce supply-chain risk if the source is not reviewed. <br>
Mitigation: Verify the pinned openclaw-governance GitHub source before allowing auto-install. <br>


## Reference(s): <br>
- [OpenClaw Governance repository](https://github.com/pawlsclick/openclaw-governance) <br>
- [Pinned openclaw-governance source](https://github.com/pawlsclick/openclaw-governance@v0.5.5) <br>
- [Migrating Existing Governance](https://github.com/pawlsclick/openclaw-governance/blob/main/docs/migrating-existing-governance.md) <br>
- [Brownfield discover flow](references/brownfield-flow.md) <br>
- [openclaw-gov command reference](references/commands.md) <br>
- [Safe discovery JSON slices](references/discovery-json-slices.md) <br>
- [What counts as material?](references/material-change-threshold.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents through read-only audit, material change, and governance PR workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
