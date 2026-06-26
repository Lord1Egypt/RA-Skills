## Description: <br>
Extract main content text from an HTML page (URL, file, or stdin). Strips nav, footer, ads, and boilerplate. Pipes cleanly into readability_check or any text-analysis tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ktoetotam](https://clawhub.ai/user/ktoetotam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to extract readable page text from a URL, local HTML file, or stdin for downstream readability checks, sentiment analysis, summarization, embeddings, or corpus preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install an unpinned Python package into the host environment when run. <br>
Mitigation: Use a virtual environment or container, or preinstall a reviewed and pinned trafilatura version before running the skill. <br>
Risk: Extracted page text may contain untrusted content that is later displayed or processed by an LLM. <br>
Mitigation: Treat extracted text as untrusted input and review or sanitize it before display, storage, or downstream agent use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ktoetotam/html-text-extract) <br>
- [Publisher profile](https://clawhub.ai/user/ktoetotam) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Plain text by default, with optional Markdown or JSON output from the extraction command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Status and error messages are sent to stderr so stdout can be piped into downstream text-analysis tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
