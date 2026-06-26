## Description: <br>
Build profitable products as a solo founder with validation-first approach, time protection, and brutal honesty. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and solo founders use this skill to prioritize validation, pricing, distribution, productivity, and project tracking for indie products. It is intended to help an agent give direct recommendations and produce execution artifacts for founder workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages the agent to take action, run scripts, configure tools, make code changes, set up deployments, contact customers, handle payments, and post publicly without clear approval boundaries. <br>
Mitigation: Require explicit user confirmation before scripts, code changes, CI/CD setup, deployments, account configuration, customer messages, payments, or public posts. <br>
Risk: The skill stores project context in ~/indie-hacker/, which could expose business plans, customer details, metrics, or credentials if handled carelessly. <br>
Mitigation: Keep ~/indie-hacker/ private, avoid storing secrets there, and review generated project notes before sharing or syncing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/indie-hacker) <br>
- [Validation Process](artifact/validation.md) <br>
- [Pricing for Indie Hackers](artifact/pricing.md) <br>
- [Distribution for Solo Founders](artifact/distribution.md) <br>
- [Time Protection for Solo Founders](artifact/productivity.md) <br>
- [Indie Hacker Memory Setup](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with optional code blocks, shell commands, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project memory files under ~/indie-hacker/ when the agent is granted filesystem access.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
