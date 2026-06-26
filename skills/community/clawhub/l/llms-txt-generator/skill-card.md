## Description: <br>
Generates a well-structured llms.txt file for a business website by crawling the site, filling gaps conversationally, and producing an agent-optimized Markdown file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ngm9](https://clawhub.ai/user/ngm9) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, site owners, and business operators use this skill to make a business website easier for AI agents to understand by generating a structured llms.txt draft from crawled site content and user-supplied clarifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided URLs are shown inside shell command examples, creating command-injection risk if untrusted or unsanitized values are passed through. <br>
Mitigation: Treat URLs as untrusted input, avoid unsanitized shell interpolation, and review or quote command arguments before execution. <br>
Risk: The crawler reads website pages and can extract emails and page text into local temporary files. <br>
Mitigation: Avoid internal or private URLs, review extracted content before reuse, and prefer a project-specific output path over a shared /tmp file. <br>


## Reference(s): <br>
- [llms.txt Specification & Examples](references/llms_txt_spec.md) <br>
- [llmstxt.org](https://llmstxt.org) <br>
- [ClawHub Skill Page](https://clawhub.ai/ngm9/llms-txt-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown llms.txt content with conversational guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local /tmp/llms_final.txt file after user review.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
