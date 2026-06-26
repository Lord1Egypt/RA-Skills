## Description: <br>
Extracts content from local HTML files and remote HTML URLs into clean, structured Markdown using MinerU. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert HTML pages or files into Markdown for downstream reading, summarization, documentation, and content extraction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTML content, URLs, or page data may be sent through MinerU using the configured token. <br>
Mitigation: Do not process confidential HTML, intranet pages, authenticated URLs, or proprietary content unless the user has approved use of MinerU for that material. <br>
Risk: The skill depends on the external mineru-open-api CLI and a MINERU_TOKEN credential. <br>
Mitigation: Install the CLI from trusted package sources, keep the token out of prompts and logs, and verify the command target before execution. <br>
Risk: HTML extraction may omit, reorder, or simplify content from complex layouts. <br>
Mitigation: Review the generated Markdown against the source HTML before relying on it for decisions or publication. <br>


## Reference(s): <br>
- [ClawHub HTML Extract](https://clawhub.ai/mzlzyca/html-extract) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU Token Management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [MinerU document content is written to stdout by default or to an output directory when requested; progress and status messages are written to stderr.] <br>

## Skill Version(s): <br>
0.4.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
