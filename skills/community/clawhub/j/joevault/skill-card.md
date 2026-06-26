## Description: <br>
Audit, classify, and quarantine stale paths after a profile switch, account migration, reset, or workspace move. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeproai](https://clawhub.ai/user/joeproai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use JoeVault to inspect stale local state after profile switches, account migrations, resets, or workspace moves. It helps them decide which inactive paths can be archived without breaking live configuration, symlinks, or active workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A stale path could still be referenced by live configuration, services, or symlinks. <br>
Mitigation: Run the audit first, review reference hits and symlink targets, and quarantine only paths that are clearly inactive. <br>
Risk: Large or recently modified workspaces may contain model files, media, training outputs, repos, or current work. <br>
Mitigation: Inventory large trees and recent activity before moving them; treat uncertain paths as reference archives instead of cleanup targets. <br>
Risk: Running cleanup with elevated privileges can expand the impact of an incorrect move. <br>
Mitigation: Use normal user permissions, limit search roots to directories intended for inspection, and keep archive moves reversible with manifest entries. <br>


## Reference(s): <br>
- [Classification guide](references/classification.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands; bundled scripts produce JSON audit reports and Markdown archive manifests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review audit output before moving paths; quarantine only clearly inactive state and inventory large or recent workspaces first.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
