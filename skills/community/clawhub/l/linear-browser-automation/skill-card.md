## Description: <br>
Automate Linear.app workflows in the OpenClaw-managed browser profile using browser tool actions (open, navigate, snapshot, act). Use when users want UI-based Linear automation such as triage, issue updates, comments, filtering, bulk state changes, and visual verification in the managed OpenClaw browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hassam-powerhouse](https://clawhub.ai/user/hassam-powerhouse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to operate Linear through the managed browser for issue search, creation, edits, comments, state changes, bulk triage, and visual verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate in a logged-in Linear workspace through the managed browser. <br>
Mitigation: Install only when that access is acceptable, and review requested actions before confirming them. <br>
Risk: Issue creation, edits, state changes, comments, bulk triage, delete, or archive actions can change workspace data. <br>
Mitigation: Require explicit user confirmation for sensitive or destructive changes and verify the resulting Linear state after action. <br>
Risk: Ambiguous team, project, issue, state, or priority inputs can target the wrong Linear item. <br>
Mitigation: Collect required fields before acting, reject unsupported state or priority values, and resolve the exact issue from team and issue number. <br>


## Reference(s): <br>
- [Linear Browser Workflows](references/workflows.md) <br>
- [Selectors and Fallbacks](references/selectors-and-fallbacks.md) <br>
- [ClawHub release page](https://clawhub.ai/hassam-powerhouse/linear-browser-automation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown text with browser-action guidance, confirmations, and completion reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include actions performed, changed issue identifiers or titles when visible, verification results, and manual follow-up notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
