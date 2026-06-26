## Description: <br>
Extracts content from PowerPoint presentations to Markdown using MinerU. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract readable Markdown from local or URL-hosted PowerPoint files for content processing, documentation workflows, and slide review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation content may be processed through a third-party MinerU/OpenDataLab service workflow. <br>
Mitigation: Prefer public or non-sensitive decks unless MinerU privacy and retention terms have been reviewed. <br>
Risk: Running extraction against the wrong local file or URL could submit unintended slide content. <br>
Mitigation: Confirm the exact file path or URL before extraction and restrict access to MINERU_TOKEN. <br>


## Reference(s): <br>
- [Ppt Extract on ClawHub](https://clawhub.ai/mzlzyca/ppt-extract) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU API Token Management](https://mineru.net/apiManage/token) <br>
- [mineru-open-api npm package](https://www.npmjs.com/package/mineru-open-api) <br>
- [mineru-open-api Go package](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown files or stdout produced by mineru-open-api, with shell commands and token setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save extraction output to a directory with -o; progress and status messages go to stderr.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
