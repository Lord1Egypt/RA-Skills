## Description: <br>
Intelligent memory management for OpenClaw agents that reviews daily notes, suggests MEMORY.md updates, maintains directory health, and auto-cleans old files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MaxLaurieHutchinson](https://clawhub.ai/user/MaxLaurieHutchinson) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to keep agent memory files organized, review recent daily notes, and generate human-reviewed suggestions for long-term MEMORY.md updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The review workflow can send memory files, USER.md, MEMORY.md, daily notes, and environment-derived context to Gemini. <br>
Mitigation: Install only when this data can be shared with Gemini, and review the workspace .env file so unrelated secrets are not exposed. <br>
Risk: The install workflow can add a recurring daily cron job. <br>
Mitigation: Review the scheduled job during installation and disable scheduling if recurring automated review is not desired. <br>
Risk: Apply and cleanup workflows can move, archive, or trash memory files based on generated review JSON. <br>
Mitigation: Inspect generated JSON before applying changes, prefer dry-run or safe mode first, and confirm that trash or archive retention meets recovery needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MaxLaurieHutchinson/memory-maintenance) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, structured JSON review files, shell command guidance, and configuration settings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gemini CLI, jq, and GEMINI_API_KEY; generated review JSON should be treated as untrusted until reviewed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
