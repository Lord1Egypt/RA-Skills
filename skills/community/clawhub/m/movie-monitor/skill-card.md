## Description:

Automates a movie monitoring pipeline that scrapes 6v520 listings, filters titles by IMDb or Douban score, adds downloads to 115 offline download, copies media to NAS storage, and renames local and cloud files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuexinguo](https://clawhub.ai/user/yuexinguo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a personal movie-download pipeline that monitors new listings, queues 115 offline downloads, copies completed media to NAS storage, and performs cleanup or rename actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled tasks may modify local NAS media and 115 cloud files without interactive confirmation.

Mitigation: Review the scheduled actions before installation, use a restricted dedicated account, and preview cleanup or batch rename operations before allowing them to run.

Risk: The workflow depends on cookie files for 115 access, including a separate renamer cookie.

Mitigation: Keep cookie files under strict filesystem permissions, rotate them if exposed, and avoid sharing them across unrelated automation.

Risk: The skill calls external local scripts from expected ~/.openclaw paths that are not included in the artifact.

Mitigation: Audit the referenced Python and Node.js scripts in the local ~/.openclaw locations before enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuexinguo/skills/movie-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May schedule agent turns that execute local Python and Node.js scripts against 115 cloud storage and NAS paths.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
