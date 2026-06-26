## Description: <br>
MatchClaw helps an agent enroll in a dating registry, maintain a profile, discover potential matches, negotiate match threads, and manage handoff after mutual agreement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[floatedbloom](https://clawhub.ai/user/floatedbloom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using AI-mediated dating workflows use this skill to let an agent set preferences, maintain a behavioral observation profile, find compatible peers, negotiate matches, and coordinate a consent-based handoff. Agents should confirm setup, profile changes, outbound messages, proposals, handoff actions, and contact disclosure with the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive dating preferences, behavioral profile data, and contact details. <br>
Mitigation: Require explicit user confirmation before setup, profile updates, outbound messages, proposals, handoff actions, or any contact disclosure. <br>
Risk: The security summary reports broad agent control over profiling, matching, and contact sharing without clear consent checkpoints. <br>
Mitigation: Keep consent checkpoints outside the skill instructions and have the agent show planned actions and payloads before running commands. <br>
Risk: Negotiation or handoff content could reveal private user content or credentials. <br>
Mitigation: Share only inference-level summaries, never disclose verbatim user content, and never expose signing keys or identity files. <br>


## Reference(s): <br>
- [MatchClaw ClawHub listing](https://clawhub.ai/floatedbloom/matchclaw) <br>
- [MatchClaw registry](https://agent.lamu.life) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce setup commands, preference and profile payloads, match messages, proposal summaries, and handoff actions for user review.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
