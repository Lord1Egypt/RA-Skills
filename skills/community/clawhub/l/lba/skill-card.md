## Description: <br>
Automate Linear.app workflows in the OpenClaw-managed browser profile using browser tool actions for triage, issue updates, comments, filtering, bulk state changes, and visual verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hassam-powerhouse](https://clawhub.ai/user/hassam-powerhouse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and team members use this skill to operate Linear through a managed browser session for issue search, creation, updates, comments, state changes, bulk triage, and visual verification. It is intended for UI-based Linear workflows where the agent must confirm required inputs and verify visible results after actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent operates Linear through the user's logged-in browser session and can create, edit, comment on, move, or bulk-triage issues under that account. <br>
Mitigation: Verify the workspace, team, issue identifier, destination state, and exact text or fields before edits; require explicit confirmation for issue creation, destructive actions, and bulk triage. <br>
Risk: Browser UI automation can act on stale, ambiguous, or changed interface elements. <br>
Mitigation: Use fresh snapshots and stable refs before actions, re-snapshot after major UI transitions, and verify visible post-action state before completion. <br>


## Reference(s): <br>
- [LBA ClawHub listing](https://clawhub.ai/hassam-powerhouse/lba) <br>
- [Linear](https://linear.app/) <br>
- [Selectors and Fallbacks](references/selectors-and-fallbacks.md) <br>
- [Linear Browser Workflows](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown completion report with browser-driven verification details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated Linear session in the OpenClaw-managed browser and confirmation of required fields before mutating issues.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
