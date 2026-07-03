## Description: <br>
Complete daily operations automation for GitHub projects, including GitHub interactions, daily report generation, trending watch, health checks, and multi-platform social publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nima54851](https://clawhub.ai/user/nima54851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to schedule routine GitHub operations, monitor project topics, generate daily markdown reports, and prepare social digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate public GitHub and social actions, including stars, comments, issue updates, and publishing. <br>
Mitigation: Review configured repositories, comment templates, publishing channels, and schedules before enabling automation. <br>
Risk: The skill requests GitHub access that may affect repositories or account activity. <br>
Mitigation: Use fine-grained, least-privilege GitHub tokens and store secrets outside committed files. <br>
Risk: Scheduled automation can repeatedly post low-quality or unintended public content. <br>
Mitigation: Require human review for generated comments and social posts until behavior is validated for the target projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nima54851/skills/lingxi-daily-ops) <br>
- [GitHub](https://github.com) <br>
- [GitHub API](https://api.github.com) <br>
- [ZeroGPU platform](https://platform.zerogpu.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and configuration-oriented text with command triggers and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate operational summaries, GitHub activity plans, health-check status, and social publishing drafts based on configured targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
