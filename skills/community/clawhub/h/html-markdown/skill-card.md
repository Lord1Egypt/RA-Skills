## Description: <br>
Converts local HTML files and web pages to clean Markdown using MinerU's document processing engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and content teams use this skill to convert local HTML files or web pages into Markdown for documentation, content migration, and Markdown-based publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTML content or URLs submitted for conversion may be processed by MinerU's external API. <br>
Mitigation: Do not process confidential, regulated, authenticated, or internal pages unless the user has approval and understands MinerU's handling of submitted content. <br>
Risk: The skill requires a MinerU API token for HTML conversion. <br>
Mitigation: Keep MINERU_TOKEN out of prompts, logs, generated files, and source control; use the documented authentication flow or environment variable only in trusted environments. <br>


## Reference(s): <br>
- [HTML Markdown on ClawHub](https://clawhub.ai/mzlzyca/html-markdown) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU Token Management](https://mineru.net/apiManage/token) <br>
- [MinerU Repository](https://github.com/opendatalab/MinerU) <br>
- [mineru-open-api CLI](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Converted document content is emitted to stdout by default or saved with an output directory; progress and status messages are sent to stderr.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
