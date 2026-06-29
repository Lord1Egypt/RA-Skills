## Description: <br>
Use this skill to read, create, update, and delete CodeRabbit data through the OOMOL CodeRabbit connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and organization administrators use this skill to operate CodeRabbit through an OOMOL-connected account, including reviewing organization users, audit logs, roles, seats, and review metrics. It can also guide approved role, seat, and self-hosted Enterprise configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions that change CodeRabbit organization roles, seats, custom roles, and seat assignment mode. <br>
Mitigation: Require the user to confirm the exact payload and expected effect before running write actions. <br>
Risk: The skill includes a destructive custom-role deletion action. <br>
Mitigation: Require explicit approval of the target role before deletion and verify that the role is not assigned to users. <br>
Risk: Organization-level actions can affect many users. <br>
Mitigation: Review prompts carefully before approving role, seat, or deletion actions. <br>


## Reference(s): <br>
- [CodeRabbit homepage](https://www.coderabbit.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-coderabbit) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use the oo CLI and should inspect the live connector schema before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
