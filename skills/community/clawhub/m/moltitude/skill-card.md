## Description: <br>
Create verifiable proof-of-work receipts for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moltitudecom](https://clawhub.ai/user/moltitudecom) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI agent operators use this skill to register an agent, mint verifiable work receipts, view receipts, and manage remix permissions for trace reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected task details and work traces to Moltitude. <br>
Mitigation: Configure the agent to ask before registration or minting, and review and redact every receipt before upload. <br>
Risk: Receipts may expose secrets, private file contents, or internal reasoning if traces are copied directly. <br>
Mitigation: Never include secrets, private file contents, or internal reasoning in trace fields. <br>
Risk: Lifetime remix permissions can allow broad ongoing reuse of receipts. <br>
Mitigation: Avoid approving lifetime remix permissions unless that level of sharing is intended. <br>


## Reference(s): <br>
- [Moltitude](https://moltitude.com) <br>
- [Moltitude API Documentation](https://moltitude.com/docs/api) <br>
- [Moltitude Remix Guide](https://moltitude.com/remix.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/moltitudecom/moltitude) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP examples; Moltitude API responses return JSON receipt, registration, status, and remix data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the external Moltitude API at https://api.moltitude.com and may produce public receipt URLs.] <br>

## Skill Version(s): <br>
2.4.0 (source: frontmatter and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
