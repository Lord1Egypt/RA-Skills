## Description: <br>
Collects a user's own NetEase Cloud Music desktop listening data into local JSONL, CSV, aggregate, and prompt outputs for optional AI-assisted listening-profile analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dragonknightk](https://clawhub.ai/user/dragonknightk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent-client users use this skill to collect their own NetEase Cloud Music main playlist, recent-week listening ranking, and all-time listening ranking into local files. The outputs help users review the data themselves or share selected files with an AI service for optional analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Collected listening-profile files may reveal music habits, mood, routines, or personal traits. <br>
Mitigation: Keep generated outputs private, review selected files before sharing them with any AI service, and avoid committing output directories to public repositories. <br>
Risk: Dependency reproducibility may matter because the skill runs local Python scripts with third-party packages. <br>
Mitigation: Install dependencies in a locked or isolated virtual environment when reproducibility or local package hygiene is important. <br>
Risk: The collection flow uses a local CDP session against a logged-in desktop client context. <br>
Mitigation: Use the skill only for your own account, follow its local-only collection flow, and close the desktop client or debug session after collection. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dragonknightk/ncm-listening-profile) <br>
- [Project Homepage](https://github.com/dragonknightk/ncm-listening-profile) <br>
- [Environment Reference](references/environment.md) <br>
- [API Collection Reference](references/api-patterns.md) <br>
- [Schema Reference](references/schemas.md) <br>
- [Troubleshooting Reference](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands plus local JSONL, CSV, JSON, and diagnostic files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are local to the user's machine and include result, csv, raw, aggregate, and log directories for each collection run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
