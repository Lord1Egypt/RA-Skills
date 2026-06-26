## Description: <br>
Normalize papers, PDFs, URLs, and literature notes into structured research records for project memory and retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunbinnju-star](https://clawhub.ai/user/sunbinnju-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and research operations teams use this skill to convert papers, PDFs, URLs, and literature notes into consistent bibliographic and research-content records for project memory and later retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted bibliographic fields, summaries, or writeback payloads may be incomplete or uncertain. <br>
Mitigation: Review title, authors, year, summaries, uncertain_fields, and writeback_payload before relying on the record or allowing any project memory writeback. <br>
Risk: A read-or-summarize request could be mistaken for permission to write into project memory. <br>
Mitigation: Require an explicit project_id and human review before any actual memory writeback. <br>


## Reference(s): <br>
- [Paper Ingest Normalizer on ClawHub](https://clawhub.ai/sunbinnju-star/paper-ingest-normalizer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Structured research record with bibliographic fields, summaries, uncertainty markers, and writeback payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes writeback_ready and uncertain_fields indicators; memory writeback requires review and a project_id.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
