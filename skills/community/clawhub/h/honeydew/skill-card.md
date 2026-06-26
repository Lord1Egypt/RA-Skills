## Description: <br>
Manage HoneyDew Kanban boards, cards, and labels via the REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smartify-dot-ai](https://clawhub.ai/user/smartify-dot-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, teams, and agent users use this skill to manage HoneyDew Kanban boards through a running local or trusted-network REST API, including creating, moving, deleting, labeling, and transferring task cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The HoneyDew API is documented as unauthenticated for local or trusted-network use. <br>
Mitigation: Keep the API bound to localhost or a trusted network before allowing an agent to manage boards. <br>
Risk: Delete, bulk-change, move, and transfer actions can materially alter task boards. <br>
Mitigation: Review high-impact requests before allowing the agent to execute them. <br>
Risk: Cards and comments may expose sensitive information to anyone with access to the HoneyDew instance. <br>
Mitigation: Avoid storing secrets or sensitive credentials in cards, comments, labels, or task metadata. <br>


## Reference(s): <br>
- [HoneyDew ClawHub listing](https://clawhub.ai/smartify-dot-ai/honeydew) <br>
- [HoneyDew repository](https://github.com/smartify-inc/honeydew) <br>
- [HoneyDew API documentation](https://github.com/smartify-inc/Honeydew#api-endpoints) <br>
- [HoneyDew agent tools reference](https://github.com/smartify-inc/Honeydew#agent-integration) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and REST API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to operate on a running HoneyDew instance and may change board, card, label, comment, and profile assignment state.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
