## Description: <br>
Summarize core safety information from Investigator's Brochures for clinical researchers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical researchers use this skill to extract and summarize core safety information from Investigator's Brochures, including adverse reactions, contraindications, warnings, interactions, special population precautions, overdose information, and safety updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted PDFs or DOCX files may exercise unpinned or vulnerable document parser dependencies. <br>
Mitigation: Process only trusted documents, or run the skill in a constrained environment with pinned and updated parser dependencies plus documented input size and timeout limits. <br>
Risk: Extracted safety summaries may be incomplete or unsuitable as medical advice. <br>
Mitigation: Review generated summaries against the source Investigator's Brochure and require qualified clinical review before using the output for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/ib-summarizer) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files] <br>
**Output Format:** [Markdown, JSON, or plain text safety summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write output to stdout or a user-specified file; supports Chinese or English output selection.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
