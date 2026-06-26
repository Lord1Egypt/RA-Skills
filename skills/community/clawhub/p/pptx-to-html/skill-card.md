## Description: <br>
Convert PowerPoint (.pptx) presentations to HTML using MinerU while preserving slide content, text, and basic structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, web publishers, and content teams use this skill to convert local or URL-hosted PowerPoint decks into web-ready HTML for display, publishing, or embedding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slide contents may be processed by MinerU's external service. <br>
Mitigation: Avoid confidential presentations unless the user's organization permits MinerU or OpenDataLab processing that content. <br>
Risk: The skill relies on a token-authenticated external CLI. <br>
Mitigation: Install mineru-open-api only from trusted sources and protect MINERU_TOKEN like any other API credential. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/mzlzyca/pptx-to-html) <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>
- [mineru-open-api Go package source](https://github.com/opendatalab/MinerU-Ecosystem/tree/master/cli/mineru-open-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the mineru-open-api command and MINERU_TOKEN for token-authenticated extraction.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
