## Description: <br>
Complete academic paper writing pipeline with integrity checks and multi-agent review system. Optimized prompts for Methods/Results/Discussion sections. Features self-counterargument framework, bias matrix, and overclaim self-audit. Use when writing research papers, need citation verification, anti-hallucination checks, multi-perspective review, or auditable process records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ithacajason](https://clawhub.ai/user/ithacajason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and academic writers use this skill to run a staged manuscript workflow that gathers literature evidence, drafts paper sections, checks citations, reviews the manuscript, revises content, and records a process summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics, citation metadata, evidence summaries, manuscript text, and revision content may be sent to the configured OpenAI-compatible provider and public literature APIs. <br>
Mitigation: Use only with content that may be shared with those services, configure approved providers, and avoid entering confidential, embargoed, or sensitive manuscript material unless that sharing is permitted. <br>
Risk: The skill claims 100% integrity and claim verification, but those checks should not be treated as proof that all claims, statistics, PRISMA counts, registration IDs, and citations are correct. <br>
Mitigation: Manually verify citations, numerical claims, study counts, registration identifiers, and source support before using generated manuscript text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ithacajason/jason-academic-writing) <br>
- [Review Rubric](references/review_rubric.md) <br>
- [API Reference](references/api_reference.md) <br>
- [Semantic Scholar API](https://api.semanticscholar.org) <br>
- [CrossRef DOI API](https://api.crossref.org/works/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON files with shell-command usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENAI_API_KEY and OPENAI_BASE_URL; writes research, draft, review, revision, integrity-check, and summary artifacts under the selected output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
