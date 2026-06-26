## Description: <br>
OpenClaw News Publisher helps agents create, preview, and publish Markdown news articles to RSS and configured content platforms from a command-line workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and content teams use this skill to draft Markdown news articles, preview them, and publish or dry-run publishing to RSS and configured platforms from a CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install and run external publishing code and dependencies. <br>
Mitigation: Review the external project and dependencies before installing, preferably pinning to a known commit. <br>
Risk: Publishing workflows may use platform credentials stored in environment files. <br>
Mitigation: Use test or least-privilege credentials, keep .env files out of version control, and review credential scope before use. <br>
Risk: Live publish commands can distribute content publicly across configured platforms. <br>
Mitigation: Use preview and --dry-run first, specify target platforms explicitly, and require human confirmation before live publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZhenStaff/news-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI command examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include platform-specific publishing steps, dry-run guidance, and credential configuration reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
