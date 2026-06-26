## Description: <br>
Pacta is a deprecated escrow skill that has been permanently deactivated and exits with a warning instead of providing V1 smart contract interaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amenizm](https://clawhub.ai/user/amenizm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers may encounter this release when checking Pacta V1 availability. The skill only communicates deactivation and regulatory-review status, then prevents agent-driven escrow actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users with historical Pacta V1 funds could mistake this release for a recovery or contract-interaction path. <br>
Mitigation: Treat the skill as informational only and seek official project guidance before attempting any manual Pacta V1 action. <br>
Risk: Automations that still expect Pacta escrow functionality will fail when the handler exits. <br>
Mitigation: Handle the non-zero exit status and remove this skill from workflows that require Pacta V1 escrow operations. <br>


## Reference(s): <br>
- [ClawHub Pacta Skill Page](https://clawhub.ai/amenizm/pacta) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text terminal warning] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exits with status code 1 after printing the deactivation warning.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter, manifest.json, evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
