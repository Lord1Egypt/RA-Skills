## Description: <br>
Facilitates structured multi-agent debates with opposing expert views, a referee moderator, and nine specialized AI council votes for balanced decision-making. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miknasbh-stack](https://clawhub.ai/user/miknasbh-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and decision teams use this skill to run structured debates on complex strategic, technical, risk, product, policy, or business questions. It orchestrates opposing arguments, council evaluation, voting, and an outcome report with recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debate topics, transcripts, votes, and reports may contain confidential or regulated information and are saved in local logs or reports. <br>
Mitigation: Use only approved data, redact sensitive inputs, restrict workspace permissions, and define retention or deletion rules for generated logs and reports. <br>
Risk: Optional GitHub, external LLM provider, hosted API, or webhook integrations may send debate content outside the local environment. <br>
Mitigation: Disable remote sync, webhooks, hosted API use, and multi-provider routing unless approved; use private repositories and review provider data-handling terms. <br>
Risk: The artifact suggests an optional sudo symlink for system-wide CLI installation. <br>
Mitigation: Prefer user-level PATH configuration and use a sudo symlink only when system-wide installation is necessary and reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/miknasbh-stack/miknas-council-of-wisdom) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [PROJECT-SUMMARY.md](artifact/PROJECT-SUMMARY.md) <br>
- [IMPLEMENTATION.md](artifact/IMPLEMENTATION.md) <br>
- [referee-prompt.md](artifact/templates/referee-prompt.md) <br>
- [debater-prompt.md](artifact/templates/debater-prompt.md) <br>
- [council-prompts.md](artifact/templates/council-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and prompts with shell command examples and JSON metadata or configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local workspaces, debate logs, outcome reports, prompt templates, and optional GitHub issues or repositories when the CLI workflow is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
