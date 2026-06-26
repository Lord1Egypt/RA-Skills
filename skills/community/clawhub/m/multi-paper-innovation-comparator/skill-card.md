## Description: <br>
Compare innovations across multiple academic papers in a folder and produce a rolling summ document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orbisz](https://clawhub.ai/user/orbisz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical reviewers use this skill to process up to 20 local papers, summarize each paper's contributions, compare related papers, and identify concrete follow-on research directions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads files in the selected paper folder and writes summary, state, and extracted-text files there. <br>
Mitigation: Run it only on an intended paper folder and review generated files before relying on them. <br>
Risk: The source includes a self-evolution section that asks the agent to record failures and propose changes to its own instructions. <br>
Mitigation: Ignore or remove that section unless diary logging and human-reviewed skill changes are explicitly desired. <br>
Risk: PDF text extraction quality may be poor for scanned or malformed PDFs, which can affect summaries and comparisons. <br>
Mitigation: Check extracted text and use OCR or corrected source text when extraction is incomplete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/orbisz/multi-paper-innovation-comparator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/orbisz) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown research notebook with supporting JSON state and extracted text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates summ.md, paper_summ_state.json, and extracted_text/ in the selected paper folder; output is Chinese by default unless the user requests another language.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
