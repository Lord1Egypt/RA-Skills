## Description: <br>
Verify an email address's deliverability and reputation using OpenMerch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kernel-gd](https://clawhub.ai/user/kernel-gd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to check a single email address for deliverability and basic reputation signals before outreach, onboarding, or list hygiene work. It requires an authorized OpenMerch account and API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each verification sends the submitted email address and OpenMerch API key to OpenMerch. <br>
Mitigation: Use the skill only with email addresses you are authorized to check, and keep OPENMERCH_API_KEY scoped and protected. <br>
Risk: Each successful execution can consume OpenMerch account credits. <br>
Mitigation: Review the /v1/plan quote before execution and rely on max_cost from the plan response rather than a hardcoded price. <br>
Risk: The skill may fail while the documented upstream provider outage remains active. <br>
Mitigation: Do not use the skill until the outage notice is removed or OpenMerch confirms the provider is available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kernel-gd/openmerch-email-verify) <br>
- [Publisher profile](https://clawhub.ai/user/kernel-gd) <br>
- [OpenMerch documentation](https://docs.openmerch.dev) <br>
- [OpenMerch API endpoint](https://api.openmerch.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and normalized JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes one email address per run and includes the raw OpenMerch job output, actual cost, and job id when execution completes.] <br>

## Skill Version(s): <br>
1.0.3 (source: evidence.json release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
