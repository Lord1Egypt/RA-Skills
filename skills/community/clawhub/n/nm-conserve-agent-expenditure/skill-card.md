## Description: <br>
Tracks per-agent token usage and flags waste in parallel dispatch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering leads use this skill after multi-agent runs to review per-agent token usage, identify redundant or low-value parallel dispatches, and adjust future agent coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may assume the linked external Claude Code plugin has the same security posture as this documentation-only artifact. <br>
Mitigation: Review the external plugin independently before installing it; the clean security verdict applies to this artifact only. <br>
Risk: Post-dispatch waste findings can be misleading when agents were not assigned distinct scopes or when review evidence is incomplete. <br>
Mitigation: Apply the checklist after execution and compare agent outputs, file access, token usage, and evidence citations before changing dispatch patterns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conserve-agent-expenditure) <br>
- [Conserve plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown] <br>
**Output Format:** [Markdown guidance and review checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
