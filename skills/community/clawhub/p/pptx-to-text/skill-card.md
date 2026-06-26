## Description: <br>
Extract plain text from PowerPoint (.pptx) presentations using MinerU. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and content teams use this skill to extract readable text from PowerPoint decks for search indexing, review, and preprocessing workflows. It supports quick Markdown extraction and token-based JSON extraction through MinerU. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PowerPoint files may contain confidential or regulated information, and MinerU data handling is not established by the provided evidence. <br>
Mitigation: Test with non-sensitive files first, review MinerU privacy and API terms, and avoid confidential presentations until upload, retention, and protection behavior is confirmed. <br>
Risk: Token-based extraction uses MINERU_TOKEN and the mineru-open-api CLI. <br>
Mitigation: Store the token only in the environment or the CLI's supported auth flow, avoid committing it, and review the installed package or source before use. <br>


## Reference(s): <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; extracted content may be Markdown or JSON depending on the MinerU command used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [flash-extract has documented 10 MB and 20 page limits; token-based extraction can produce JSON text fields per slide.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
