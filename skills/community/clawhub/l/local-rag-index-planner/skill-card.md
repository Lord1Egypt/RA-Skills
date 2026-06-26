## Description: <br>
Plans local knowledge-base directories, chunking granularity, naming, update timing, and access boundaries for RAG-oriented knowledge workflows without directly deploying vector databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge managers, and teams use this skill to turn local content requirements, retrieval goals, and permission boundaries into a reviewable indexing plan. It helps draft structure, metadata, update strategy, risks, and next steps before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may reflect sensitive or private content from user-provided files or directories. <br>
Mitigation: Review and minimize inputs before use, remove sensitive material when possible, and prefer stdout or dry-run review before writing reports. <br>
Risk: Broad directory inputs can expose more local content than intended to the generated planning report. <br>
Mitigation: Run the helper on specific, reviewed files or narrowly scoped directories rather than broad private workspaces. <br>
Risk: Plans are advisory and may omit context needed for permission, privacy, or compliance decisions. <br>
Mitigation: Treat outputs as reviewable drafts and confirm access boundaries, update rules, and risk controls before implementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/local-rag-index-planner) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [resources/spec.json](artifact/resources/spec.json) <br>
- [resources/template.md](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown by default, with optional JSON report output from the bundled local script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a local report file when an output path is provided; dry-run or stdout mode is available for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
