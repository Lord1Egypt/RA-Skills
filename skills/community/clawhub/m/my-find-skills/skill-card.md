## Description: <br>
My Find Skills helps agents discover, compare, and optionally install skills when users ask for skill discovery or installation, with a skillhub preference for Chinese users and clawhub fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujiang817](https://clawhub.ai/user/liujiang817) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search skill registries, present relevant candidates with source and install commands, and help install selected skills after summarizing source, version, and risk signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has an opinionated registry preference for Chinese users and CN networks. <br>
Mitigation: Before approving an install, confirm the registry, slug, version, and risk summary, and specify clawhub or another source if skillhub should not be preferred. <br>
Risk: Installing a discovered skill may add third-party agent instructions to the environment. <br>
Mitigation: Review and scan the selected skill before deployment, and approve installation only after the source and notable risk signals are understood. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liujiang817/my-find-skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include registry source, candidate summaries, install commands, and risk-signal reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
