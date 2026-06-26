## Description: <br>
Extract clean, readable markdown content from any URL using Jina Reader API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smile-xuc](https://clawhub.ai/user/smile-xuc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to turn web pages into markdown or JSON for research, summarization, content analysis, and follow-up processing after search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs are sent to Jina's external reader service. <br>
Mitigation: Use only public URLs that are appropriate to share with an external service; avoid private, authenticated, internal, token-bearing, and pre-signed URLs. <br>
Risk: The optional output-file argument can overwrite local content if pointed at an important path. <br>
Mitigation: Choose output paths deliberately and review the destination before writing extracted content. <br>
Risk: Fetched page content may be incomplete, blocked, or affected by service rate limits and timeouts. <br>
Mitigation: Validate extracted content before relying on it for analysis, and adjust timeout or retry strategy for slow pages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smile-xuc/haibo-jina-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, files, guidance] <br>
**Output Format:** [Markdown or JSON from command-line tools, with optional file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses requested URLs as input, supports timeout selection, and can write extracted content to a caller-provided output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
