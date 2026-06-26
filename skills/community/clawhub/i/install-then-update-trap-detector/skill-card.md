## Description: <br>
Helps detect the install-then-update attack pattern, where a skill passes initial security review cleanly and then silently introduces malicious behavior through an automatic update that bypasses re-audit; v1.1 adds cryptographic chain-of-custody verification for update sequences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, marketplace reviewers, and agent operators use this skill to assess whether a skill's update history shows install-then-update risk, including undeclared behavioral changes, permission expansion, timing anomalies, rollback difficulty, and broken chain-of-custody signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assessment inputs may include private skill bundles, version history, or installed-skill lists. <br>
Mitigation: Provide only the materials intended for review and avoid unnecessary access to private projects or credentials. <br>
Risk: Results can be incomplete when registries do not preserve older versions, signed update metadata, or content hashes. <br>
Mitigation: Treat missing history or custody metadata gaps as reasons for manual review rather than proof of safety. <br>
Risk: Behavioral deltas and timing anomalies are investigative signals, not proof of malicious intent. <br>
Mitigation: Confirm suspicious findings with manual code review and changelog and permission comparison before taking action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/install-then-update-trap-detector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with scored findings and a risk verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes update policy, behavioral delta, permission scope, timing, rollback, and chain-of-custody signals when evidence is available.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
