## Description: <br>
Audits dependency supply chains for bad versions, lockfile drift, and artifact integrity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit Python dependency supply chains, check lockfiles and installed packages for known-bad versions, and guide response to suspected package compromise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad dependency scans can unintentionally inspect unrelated project directories or a whole machine. <br>
Mitigation: Limit scan roots to relevant project directories unless a machine-wide sweep is intentional. <br>
Risk: Environment snapshots collected during incident response can contain credentials or other secrets. <br>
Mitigation: Treat snapshots as sensitive forensic artifacts, restrict access, and remove them when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-leyline-supply-chain-advisory) <br>
- [Night Market leyline source homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Incident Response](modules/incident-response.md) <br>
- [Scanning Patterns](modules/scanning-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command snippets, checklists, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no automatic execution, persistence, or data sending was identified in security evidence.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
