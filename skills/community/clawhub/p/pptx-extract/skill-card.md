## Description: <br>
Extract content from PowerPoint (.pptx) presentations to Markdown using MinerU, including slide text, structure, formatting, and optional page selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and document-processing agents use this skill to read or convert PowerPoint presentations into Markdown for review, documentation, and automated workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation content from local files or URLs may be sent to MinerU for processing, which can expose confidential slide content. <br>
Mitigation: Use the skill only with presentations approved for processing by MinerU, and avoid confidential business slides unless the data handling path is acceptable. <br>
Risk: Full extraction requires a MinerU token, creating credential-handling risk. <br>
Mitigation: Provide MINERU_TOKEN through a secure environment variable or the CLI auth flow, and avoid committing or sharing tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzlzyca/pptx-extract) <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU Open API CLI package](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text, with inline shell commands and optional files saved to an output directory.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [flash-extract can stream Markdown to stdout; full extraction requires MINERU_TOKEN; flash-extract is documented with a 10 MB / 20 page limit.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
