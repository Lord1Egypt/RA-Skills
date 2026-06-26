## Description: <br>
Clerk lets an agent manage Clerk users through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect, create, update, lock, ban, unban, or delete Clerk users through an OOMOL-connected Clerk account. It is suited for Clerk account administration workflows where the agent should fetch live action schemas before running commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-impact Clerk account changes, including deletes, bans, locks, and metadata updates. <br>
Mitigation: Confirm the exact target, payload, and intended effect with the user before write or destructive actions. <br>
Risk: The skill depends on an OOMOL-connected Clerk account and first-time setup may require installing the oo CLI. <br>
Mitigation: Use the existing signed-in OOMOL connection when available, avoid handling raw Clerk tokens, and verify the oo CLI installer source before setup. <br>


## Reference(s): <br>
- [Clerk skill on ClawHub](https://clawhub.ai/oomol/oo-clerk) <br>
- [Clerk homepage](https://clerk.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands call the oo CLI and may return JSON data with an execution id.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence release.version and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
