## Description: <br>
OnePageCRM (onepagecrm.com). Use this skill for OnePageCRM requests involving reading, creating, and updating CRM data through the OOMOL connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to list and retrieve OnePageCRM contacts and deals, and to create contacts or deals after confirming write payloads. It is intended for CRM workflows mediated through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can create OnePageCRM contacts or deals in the connected account. <br>
Mitigation: Confirm the exact JSON payload and expected effect with the user before running create actions. <br>
Risk: Incorrect action payloads may fail or create malformed CRM records. <br>
Mitigation: Inspect the live connector schema before building each payload and match the command data to that schema. <br>
Risk: The skill depends on the local oo CLI, OOMOL sign-in, and an active OnePageCRM connection. <br>
Mitigation: Use first-time setup steps only after an auth, connection, missing CLI, or billing error is returned. <br>


## Reference(s): <br>
- [OnePageCRM homepage](https://www.onepagecrm.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; read actions can run directly, while write actions require payload confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
