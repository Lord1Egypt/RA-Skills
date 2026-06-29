## Description: <br>
音乐库整理工作流：扫描→规划→主人确认→软删除→验证→清理。强调安全流程。Safe-by-default music library organizer with soft-delete + mandatory owner confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thinkcodee](https://clawhub.ai/user/thinkcodee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan, review, and execute local music-library organization tasks for audio files and lyrics, including A-Z artist grouping, standardized naming, quality-based deduplication, and lyric rematching. The workflow emphasizes dry-run reports, owner confirmation, soft-delete behavior, and post-action verification before cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled scripts can bulk-move, rename, or soft-delete local media files, and the enforced safeguards may be weaker than the workflow promises. <br>
Mitigation: Run dry-run modes first, inspect generated CSV and log outputs, and use --apply only after confirming exact source and target paths. <br>
Risk: Recovery after an incorrect operation may require manual file moves from backup or trash directories. <br>
Mitigation: Keep backups available, verify generated reports before execution, and check backup or trash directories before performing any permanent cleanup. <br>
Risk: Music-library parsing, deduplication, and lyric matching can misclassify files or conflicts. <br>
Mitigation: Review conflict reports and sample the organized output before continuing to deduplication, cleanup, or any irreversible action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thinkcodee/music-library-organizer) <br>
- [README.md](artifact/README.md) <br>
- [scripts/README.md](artifact/scripts/README.md) <br>
- [organize_music.README.md](artifact/scripts/organize_music.README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python script usage, and CSV or JSON report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces dry-run plans, operation logs, verification reports, and local file move or rename actions when the bundled scripts are executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
