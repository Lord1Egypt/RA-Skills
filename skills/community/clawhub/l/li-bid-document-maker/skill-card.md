## Description: <br>
Automatically converts tender documents (PDF/Word) into professional response bid documents following Chinese bidding standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External bid and proposal teams use this skill to parse PDF or Word tender documents, plan a score-oriented response, draft a Chinese-standard bid document, and produce a PDCA quality improvement report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tender files, company records, pricing, identity details, and proprietary materials may be sensitive. <br>
Mitigation: Upload or path-reference only needed files, redact unnecessary sensitive details where possible, and review generated bid content before use. <br>
Risk: Untrusted PDF or Word documents may expose the agent environment to document-parsing risk. <br>
Mitigation: Use patched document-parsing libraries and process untrusted files in a sandbox where possible. <br>
Risk: Generated files may be written to an unintended location if paths are ambiguous. <br>
Mitigation: Confirm output paths before generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-bid-document-maker) <br>
- [Usage Guide](docs/README.en.md) <br>
- [Bid Document Workflow](references/workflows/pipeline.yaml) <br>
- [System Prompt](references/prompts/system-prompt.md) <br>
- [Tender Info Schema](references/schemas/tender-info.schema.json) <br>
- [Bid Document Schema](references/schemas/bid-document.schema.json) <br>
- [Bid Structure Template](references/templates/bid-structure.json) <br>
- [Format Rules](references/templates/format-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, files, guidance] <br>
**Output Format:** [Markdown bid documents, structured JSON summaries, scoring maps, and quality reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs commonly include a complete bid response document, PDCA quality improvement report, and scoring criteria mapping.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
