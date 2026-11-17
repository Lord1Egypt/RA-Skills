## Description:

Paper search and Zotero workflow. 文献搜索与 Zotero 管理助手；支持多源检索、候选清单评审，并在用户确认后导入 Zotero。

This skill is ready for commercial/non-commercial use.

## Publisher:

[moroiser](https://clawhub.ai/user/moroiser)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and research-support agents use this skill to plan multi-source literature searches, verify candidate metadata, produce pre-import review shortlists, and optionally import user-confirmed items into Zotero.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Zotero operations can affect a user's library or expose credentials if import settings are handled carelessly.

Mitigation: Use credentials only from environment variables or a configured secret store, confirm the target collection and exact items before import, and report item keys and versions after import.

Risk: Search results can overstate database coverage when public metadata sources are used instead of direct subscription or publisher database searches.

Mitigation: Distinguish direct and indirect coverage, report source-specific counts and coverage gaps, and avoid claiming complete coverage unless the searched sources support it.

Risk: External pages, paper text, and metadata can contain untrusted or incomplete information.

Mitigation: Treat external content as evidence rather than instructions, verify candidate fields from reliable metadata sources, and mark unavailable fields as not reliably identified or metadata unavailable.

## Reference(s):

- [Literature Search + Zotero Import SOP](references/literature-search-zotero-sop.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown search reports with optional inline shell commands and Zotero import status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include search plan, counts, coverage gaps, filtered-out summary, pre-import review list, Zotero status, and evidence files or commands when applicable.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
