## Description: <br>
Converts local HTML files and web page URLs into clean Markdown using the MinerU CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation maintainers, and content migration teams use this skill to convert HTML pages or files into Markdown for documentation, archives, and Markdown-based publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the third-party mineru-open-api CLI and MinerU service token. <br>
Mitigation: Install only from trusted sources, use a dedicated MINERU_TOKEN where possible, and keep the token out of shared files and logs. <br>
Risk: Remote URLs or local HTML may contain sensitive content that is sent through MinerU tooling. <br>
Mitigation: Avoid converting sensitive HTML or private URLs unless the deployment is approved for MinerU handling that content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzlzyca/html2markdown) <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>
- [mineru-open-api npm package](https://www.npmjs.com/package/mineru-open-api) <br>
- [mineru-open-api Go package](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the mineru-open-api command and MINERU_TOKEN; converted document content is written to stdout by default or saved with -o.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
