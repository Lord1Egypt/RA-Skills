## Description: <br>
Organizes podcast production workflows from topic selection through publishing, producing show notes, title options, editing points, publishing checklists, and reusable materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Podcast creators, producers, content teams, and agents use this skill to turn episode topics, guest summaries, and recording notes into reviewable production packages. It is suited for drafting structured podcast materials while keeping missing information and publishing decisions explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Podcast materials may contain private guest details, unpublished transcripts, or other sensitive information. <br>
Mitigation: Use only the input needed for the task, redact sensitive material when practical, and review generated Markdown before sharing or publishing. <br>
Risk: Draft show notes, titles, and editing points may misrepresent guest views or imply facts not present in the source material. <br>
Mitigation: Treat outputs as reviewable drafts, keep missing information in the confirmation list, and verify claims against the provided recording notes before publication. <br>
Risk: The helper script can write an output file when an output path is supplied. <br>
Mitigation: Use stdout or dry-run mode when file writes are not intended, and choose output paths deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/podcast-production-ops) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [Specification JSON](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>
- [Smoke test](artifact/tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown by default, with optional JSON output from the local helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be printed to stdout, written to a selected file, or produced in dry-run mode for review before publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
