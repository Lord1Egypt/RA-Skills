## Description: <br>
Runs multi-source AISA searches across web, academic, Tavily, and synthesis layers, then returns confidence-rated results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill when they need a single agent workflow to gather, compare, synthesize, and confidence-rate evidence from multiple search providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URLs, and research prompts are sent to the remote AISA service. <br>
Mitigation: Do not submit secrets, private documents, internal URLs, confidential research prompts, or regulated data unless that data flow is approved. <br>
Risk: The skill requires a sensitive AISA_API_KEY credential. <br>
Mitigation: Use a scoped, rotatable API key and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/multi-search-zh) <br>
- [AISA service](https://aisa.one) <br>
- [AISA API endpoint used by the client](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal-oriented text with result summaries, citations, confidence scores, and optional synthesis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; queries are sent to the remote AISA API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
