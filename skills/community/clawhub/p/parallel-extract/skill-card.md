## Description: <br>
Parallel Extract uses the Parallel API to extract clean, LLM-ready markdown from webpages, articles, PDFs, and JavaScript-heavy sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[normallygaussian](https://clawhub.ai/user/normallygaussian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract clean content from specific URLs, including articles, PDFs, and JavaScript-heavy pages, then answer with source-aware excerpts or full content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL targets and extracted page content may be processed under the user's authenticated Parallel account, which can expose sensitive material if private or confidential pages are submitted. <br>
Mitigation: Use the skill only with trusted URLs intended for Parallel processing, avoid private or token-bearing pages unless that sharing is deliberate, and delete /tmp extraction files when they contain sensitive content. <br>


## Reference(s): <br>
- [Parallel](https://parallel.ai) <br>
- [Parallel API Docs](https://docs.parallel.ai) <br>
- [Parallel Extract API Reference](https://docs.parallel.ai/api-reference/extract) <br>
- [Parallel CLI Integration](https://docs.parallel.ai/integrations/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON extraction results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed and authenticated parallel-cli; extracted JSON may be saved to /tmp for long conversations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
