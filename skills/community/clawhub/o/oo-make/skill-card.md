## Description: <br>
Make (make.com). Use this skill for any Make request involving reading, creating, updating, or deleting data through a connected Make account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate a connected Make account: inspect authorization and scenarios, list teams, activate or deactivate scenarios, run scenarios once, and review recent usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an OOMOL-connected Make account to read account and scenario information and perform scenario operations. <br>
Mitigation: Install only when agents may use that connected Make account, and review requested scenario operations before execution. <br>
Risk: Scenario activation, deactivation, and one-time runs can trigger downstream actions in other services. <br>
Mitigation: Confirm the target scenario, payload, and intended effect with the user before write or destructive actions. <br>


## Reference(s): <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Make](https://www.make.com) <br>
- [ClawHub skill listing](https://clawhub.ai/oomol/skills/oo-make) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses should inspect live connector schemas before constructing JSON payloads and should request confirmation before write or destructive scenario actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
