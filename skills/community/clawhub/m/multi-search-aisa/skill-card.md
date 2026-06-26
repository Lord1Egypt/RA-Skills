## Description: <br>
Run multi-source evidence gathering with confidence scoring across web, academic, Tavily, and synthesis layers via AISA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and research-oriented agent users use this skill to gather evidence from multiple search sources, synthesize results, and assess confidence for questions that need more than a single search pass. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries, URLs, and extracted page content are sent to external AISA-backed services. <br>
Mitigation: Avoid using the skill with private documents, sensitive internal URLs, passwords, browser data, or confidential research unless the service and publisher are trusted. <br>
Risk: The skill requires an AISA API key. <br>
Mitigation: Provide the key through the AISA_API_KEY environment variable, keep it out of prompts and logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bibaofeng/multi-search-aisa) <br>
- [AISA service](https://aisa.one) <br>
- [AISA API endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text CLI output with search results, citations, confidence scoring, and setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; may send queries, URLs, and extracted page content to AISA-backed services.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
