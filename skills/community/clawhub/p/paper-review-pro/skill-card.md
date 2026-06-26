## Description: <br>
Paper Review Pro helps researchers retrieve, rank, summarize, and export papers from arXiv and Semantic Scholar with CCF-aware scoring and BibTeX support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alfredliang11](https://clawhub.ai/user/alfredliang11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and developers use this skill to find core papers for a topic, rank them by relevance and publication authority, generate structured summaries, and create research reports and BibTeX exports for literature review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries, paper titles, authors, abstracts, DOI/arXiv identifiers, and saved reports may be processed by configured services. <br>
Mitigation: Use --no-llm and --no-use-api for a more local workflow when external processing is not appropriate. <br>
Risk: The security summary flags under-disclosed network behavior around configured services and local gateway credentials. <br>
Mitigation: Verify OPENCLAW_GATEWAY_URL and related gateway credentials before allowing the skill to use an OpenClaw gateway token. <br>


## Reference(s): <br>
- [Paper Review Pro on ClawHub](https://clawhub.ai/alfredliang11/paper-review-pro) <br>
- [LLM Integration](reference/LLM_INTEGRATION.md) <br>
- [BibTeX Export](reference/BIBTEX_EXPORT.md) <br>
- [Publication Status and CCF Rating](reference/PUBLICATION_STATUS.md) <br>
- [Scoring System](reference/SCORING_SYSTEM.md) <br>
- [Bug Fixes](reference/BUGFIXES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, local report files, and BibTeX exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save local reports, paper metadata, and BibTeX files under the user's OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
