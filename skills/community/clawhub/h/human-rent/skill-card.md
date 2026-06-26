## Description: <br>
Human-as-a-Service for OpenClaw - Dispatch verified human agents to perform physical world tasks and sensory validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhenstaff](https://clawhub.ai/user/zhenstaff) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agents use Human-Rent to request paid human workers for physical verification, photos, inspections, phone calls, and other real-world tasks that require explicit user confirmation. <br>

### Deployment Geography for Use: <br>
United States (select cities) <br>

## Known Risks and Mitigations: <br>
Risk: The skill can dispatch paid human workers for physical-world tasks and send task details, locations, budgets, and worker-selection data to an external service involving real people. <br>
Mitigation: Install and use it only when that behavior is intended; require clear user approval, spending limits, audit logs, and task-safety controls before dispatch. <br>
Risk: Auto-confirmation can bypass interactive approval for human dispatches. <br>
Mitigation: Keep HUMAN_RENT_AUTO_CONFIRM disabled unless separate approvals, budget controls, and monitoring are already in place. <br>
Risk: The security guidance flags unsafe cleanup, secret-printing, NODE_DEBUG, and exec-based integration examples as patterns that need review. <br>
Mitigation: Review those examples before reuse and avoid copying patterns that expose secrets or execute untrusted input. <br>


## Reference(s): <br>
- [ZhenRent Documentation](https://docs.zhenrent.com) <br>
- [ZhenRent API Keys](https://www.zhenrent.com/api/keys) <br>
- [ClawHub Human-Rent Listing](https://clawhub.ai/zhenstaff/human-rent) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Text, Guidance] <br>
**Output Format:** [CLI text with task identifiers, worker listings, status updates, and human-provided result data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHENRENT_API_KEY and ZHENRENT_API_SECRET; ZHENRENT_BASE_URL is optional and defaults to the ZhenRent API.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata; artifact version files report 0.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
