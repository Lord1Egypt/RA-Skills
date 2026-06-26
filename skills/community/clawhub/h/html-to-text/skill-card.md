## Description: <br>
HTML to Text helps agents convert local HTML files or web page URLs into readable Markdown or JSON text fields using MinerU. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to strip markup from HTML files or web pages and feed readable text into search indexing, NLP pipelines, text analysis, or summarization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTML files, URLs, or generated text may be processed by the third-party MinerU service. <br>
Mitigation: Use only content that may be sent to MinerU/OpenDataLab under your policies; avoid secrets, confidential HTML, authenticated pages, internal URLs, regulated data, and private documents. <br>


## Reference(s): <br>
- [HTML to Text on ClawHub](https://clawhub.ai/mzlzyca/html-to-text) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU API Token Management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; extracted content is Markdown by default or JSON text fields when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mineru-open-api and MINERU_TOKEN; supports local HTML files and web page URLs.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
