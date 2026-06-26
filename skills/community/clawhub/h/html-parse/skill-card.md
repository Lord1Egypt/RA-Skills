## Description: <br>
Parse HTML documents into structured Markdown using MinerU. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content managers, and data pipeline operators use this skill to convert local HTML files, remote HTML documents, and live web pages into structured Markdown while preserving document hierarchy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the third-party mineru-open-api CLI and MinerU service. <br>
Mitigation: Install the CLI only from trusted MinerU/OpenDataLab package sources and review the dependency before deployment. <br>
Risk: Parsed files, URLs, or page content may be sent to MinerU for processing. <br>
Mitigation: Avoid using the skill with confidential local files, internal URLs, or proprietary pages unless MinerU's service terms are acceptable for that content. <br>
Risk: MINERU_TOKEN is required for normal operation. <br>
Mitigation: Store MINERU_TOKEN as a secret, avoid committing it to source control, and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub HTML Parse release](https://clawhub.ai/mzlzyca/html-parse) <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>
- [MinerU open-source project](https://github.com/opendatalab/MinerU) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides use of mineru-open-api, which writes parsed document output to stdout or an output directory.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
