## Description: <br>
Lemon Squeezy (lemonsqueezy.com). Use this skill for ANY Lemon Squeezy request - reading, creating, updating, and deleting data. Whenever a task involves Lemon Squeezy, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Lemon Squeezy account, store, customer, order, product, variant, subscription, and webhook workflows through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update Lemon Squeezy customers and webhooks, changing production account state. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running actions tagged as write operations. <br>
Risk: The skill can delete Lemon Squeezy webhooks. <br>
Mitigation: Require explicit approval for the target webhook before running destructive actions. <br>
Risk: The skill requires connected account credentials for Lemon Squeezy access. <br>
Mitigation: Use the OOMOL connector flow described by the skill so raw API tokens are not handled locally. <br>
Risk: Security confidence is limited by the evidence summary, which says full coherence verification of the actual artifact was not available. <br>
Mitigation: Install only when the ClawHub listing purpose and requested permissions match the intended Lemon Squeezy workflow. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/oomol/oo-lemon-squeezy) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Lemon Squeezy homepage](https://www.lemonsqueezy.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are returned as JSON data with execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
