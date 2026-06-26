## Description: <br>
Novel Assistant helps writers create and continue novel chapters while maintaining story continuity through local memory files for characters, worldbuilding, plot summaries, foreshadowing, timelines, backups, and memory compression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnskycn](https://clawhub.ai/user/cnskycn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External writers and collaborative writing teams use this skill to manage long-form fiction projects, continue chapters consistently, track character and world details, maintain timelines and foreshadowing, and compress local manuscript memory files as projects grow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and update local novel memory files and chapter backups. <br>
Mitigation: Confirm the target novel and file path before allowing edits, and keep an independent backup or version-control commit before compression or bulk updates. <br>
Risk: Memory compression rewrites manuscript memory files and may remove resolved foreshadowing or summarize older chapters. <br>
Mitigation: Review the compressed output against the original backup before relying on it for future chapter continuity. <br>
Risk: Optional Git sync can publish manuscript data to a configured remote repository. <br>
Mitigation: Verify the remote repository and access controls before pushing novel memory or chapter files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cnskycn/novel-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/cnskycn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prose with structured story notes, local file templates, review reports, and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local novel memory files and backup chapter files when the user enables those workflows.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
