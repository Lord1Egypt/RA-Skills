## Description:

Tracks HuggingFace Daily Papers and arXiv research with light-scan and deep-research workflows that search papers, analyze findings, and produce Markdown research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomfoxxxx](https://clawhub.ai/user/tomfoxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to monitor HuggingFace Daily Papers and arXiv for a configured research focus, triage relevant papers, and generate weekly/monthly or deep-dive Markdown reports with analysis and quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can infer and persist research interests or profile details from USER.md, MEMORY.md, and conversation memory.

Mitigation: Review before installing in workspaces with sensitive memory files, and keep generated profile/configuration fields minimal.

Risk: Generated reports may be uploaded to Feishu or cloud storage when cloud upload is explicitly enabled or triggered.

Mitigation: Keep cloud upload disabled unless publication is intended, and verify the destination folder before upload.

Risk: Research summaries can include unverified paper metadata, citations, or reported experimental results.

Mitigation: Use the quality-check workflow and manually verify arXiv IDs, citations, and metrics before relying on a report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomfoxxxx/skills/hf-daily-researcher-v2)
- [arXiv API query endpoint](https://export.arxiv.org/api/query)
- [Hugging Face Papers](https://huggingface.co/papers)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with supporting JSON configuration and occasional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save local Markdown reports, JSON config/history files, and temporary intermediate analysis files; cloud upload is disabled by default and on demand.]

## Skill Version(s):

4.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
