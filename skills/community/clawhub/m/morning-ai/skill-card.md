## Description: <br>
Daily-scheduled AI news tracker. Collects updates from 80+ AI entities across 6 sources every 24 hours (default 08:00 UTC+8). Generates scored, deduplicated Markdown reports. Supports unattended cron/scheduled execution with date-stamped idempotent output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[octo-patch](https://clawhub.ai/user/octo-patch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use MorningAI to collect AI industry updates from public sources, score and deduplicate them, and generate daily Markdown reports. The skill also supports optional infographic, social-post, and message-digest outputs for distribution workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports a startup shell hook that can execute code from local environment files. <br>
Mitigation: Review or disable the SessionStart hook before installation and use the skill only with trusted configuration files. <br>
Risk: Local project configuration files such as .env or .claude/morning-ai.env can affect execution. <br>
Mitigation: Avoid running the skill in untrusted project directories and inspect configuration values before enabling scheduled or unattended runs. <br>
Risk: The bundled sync script is described by the security guidance as a broad deployment tool. <br>
Mitigation: Review scripts/sync.sh and its target directories before running it. <br>
Risk: Optional social distribution workflows can prepare content for external posting. <br>
Mitigation: Keep social distribution disabled unless intended, and review generated posts before publishing. <br>


## Reference(s): <br>
- [MorningAI repository](https://github.com/octo-patch/MorningAI) <br>
- [ClawHub skill page](https://clawhub.ai/octo-patch/morning-ai) <br>
- [README](artifact/README.md) <br>
- [Tracking list skill specification](artifact/skills/tracking-list/SKILL.md) <br>
- [Report template](artifact/templates/report.md) <br>
- [Infographic skill specification](artifact/skills/gen-infographic/SKILL.md) <br>
- [Social content skill specification](artifact/skills/gen-social/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON collection data, optional generated images, optional social copy, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write date-stamped report files and optional distribution assets; behavior depends on configured environment variables and enabled integrations.] <br>

## Skill Version(s): <br>
1.2.5 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
