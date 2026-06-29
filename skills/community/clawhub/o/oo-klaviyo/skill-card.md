## Description: <br>
Klaviyo (klaviyo.com). Use this skill for ANY Klaviyo request - reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with Klaviyo through an OOMOL-connected account: reading campaigns, profiles, and events, validating account access, and creating events after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Klaviyo campaigns, profiles, and events through the connected account. <br>
Mitigation: Install it only when OOMOL is trusted as the Klaviyo connector provider and ensure the connected account has appropriate access. <br>
Risk: The create_event action can write new Klaviyo event data. <br>
Mitigation: Confirm the exact action payload and expected effect with the user before running write actions. <br>


## Reference(s): <br>
- [Klaviyo homepage](https://www.klaviyo.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
