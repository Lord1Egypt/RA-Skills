## Description: <br>
Builds a user.md profile through conversation and recommends Claude Code Skills based on the user's role. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eamanc-lab](https://clawhub.ai/user/eamanc-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create or update a persistent user.md profile through conversation and to receive role-based Claude Code Skill recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may collect, infer, and persist personal details in a reusable profile. <br>
Mitigation: Preview user.md before any write, ask for explicit confirmation, keep only necessary profile fields, and make it clear how the user can edit or delete the profile. <br>
Risk: Sensitive information could be included in the profile and later injected into agent context. <br>
Mitigation: Do not store passwords, API keys, government IDs, financial data, health data, or other sensitive details in user.md. <br>
Risk: Role-based recommendations can include third-party skill installation commands. <br>
Mitigation: Present install commands as reviewable suggestions and have the user inspect third-party skills before installation. <br>


## Reference(s): <br>
- [OpenClaw User Profiler on ClawHub](https://clawhub.ai/eamanc-lab/openclaw-user-profiler) <br>
- [OpenClaw Persona Forge repository](https://github.com/eamanc-lab/openclaw-persona-forge) <br>
- [User Profile Intake Guide](references/user-profile-fields.md) <br>
- [user.md Template](references/user-md-template.md) <br>
- [Role x Skill Recommendation Catalog](references/role-skill-catalog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown profile previews, user.md content, recommendation lists, and install commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update a local user.md after user confirmation; profile content is capped at 500 words by the artifact guidance.] <br>

## Skill Version(s): <br>
2.3.1 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
