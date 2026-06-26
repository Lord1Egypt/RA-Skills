## Description: <br>
Beehiiv connector for reading, creating, and updating Beehiiv data through an OOMOL-connected account instead of direct API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Beehiiv publications, posts, and subscriptions through the OOMOL connector with live schema inspection before each action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Beehiiv subscriber lists, publication data, and draft or post content may be sensitive and are handled through the OOMOL connector. <br>
Mitigation: Install and use the skill only when OOMOL is an intended connector, and treat returned Beehiiv data as sensitive. <br>
Risk: Write or destructive actions can change or remove Beehiiv data if an incorrect payload is sent. <br>
Mitigation: Inspect the live connector schema, review the exact payload and expected effect, and get explicit user confirmation before state-changing or destructive actions. <br>
Risk: Unneeded setup or account connection commands can expose unnecessary account or billing workflow risk. <br>
Mitigation: Run one-time CLI installation, sign-in, and Beehiiv connection steps only when a command fails for the corresponding setup reason. <br>


## Reference(s): <br>
- [Beehiiv ClawHub listing](https://clawhub.ai/oomol/oo-beehiiv) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Beehiiv homepage](https://www.beehiiv.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Beehiiv connection settings](https://console.oomol.com/app-connections?provider=beehiiv) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects with data and meta.executionId fields.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
