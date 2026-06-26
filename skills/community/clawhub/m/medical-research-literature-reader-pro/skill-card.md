## Description: <br>
Medical Research Literature Reader Pro helps clinicians and researchers classify, critique, and interpret medical and scientific papers with track-specific appraisal and follow-up research outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians, biomedical researchers, bioinformaticians, and translational science teams use this skill to read, route, and critically appraise medical or scientific papers from PDFs, abstracts, DOIs, PMIDs, titles, figures, or free-form requests. It supports quick triage, structured reports, expert deep reviews, related-literature lists, follow-up questions, journal club kits, comparison tables, PI briefs, replication starters, and experiment-design prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outputs may be mistaken for medical advice or definitive evidence. <br>
Mitigation: Use the skill as research assistance, verify cited studies before relying on them, and route clinical decisions through qualified professional review. <br>
Risk: Inputs may include PHI, private patient details, or unpublished confidential research. <br>
Mitigation: Avoid pasting sensitive or confidential material unless authorized, and provide only the paper details needed for analysis. <br>
Risk: Incomplete inputs can lead to incomplete appraisal, especially when only a title, DOI, PMID, abstract, figure, or table is available. <br>
Mitigation: Have the skill state what information is unavailable, limit conclusions to the provided evidence, and request the abstract, methods, results, or full text when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/medical-research-literature-reader-pro) <br>
- [Track analysis modules](references/tracks.md) <br>
- [Plugin system](references/plugins.md) <br>
- [Expert deep review extensions](references/expert_review_extensions.md) <br>
- [Similar literature module](references/literature_module.md) <br>
- [Follow-up questions module](references/followup_module.md) <br>
- [Reporting style](references/reporting_style.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown reports, checklists, comparison tables, briefs, and follow-up research plans.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Adapts depth to quick read, standard report, expert deep review, or requested plugin-style deliverable; does not fabricate unavailable paper content.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
