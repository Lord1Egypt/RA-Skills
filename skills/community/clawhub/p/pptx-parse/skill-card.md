## Description: <br>
PPTX Parse helps agents parse PowerPoint (.pptx) presentations into structured Markdown with MinerU while preserving slide organization and content hierarchy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content pipeline maintainers use this skill to extract organized Markdown from .pptx presentations, including slide structure, page ranges, and local-file or URL inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PPT files, URLs, and generated presentation content may be sent to an external parsing or generation service. <br>
Mitigation: Use only documents approved for that provider, and avoid confidential corporate, legal, medical, or customer data unless the service is approved for the data. <br>
Risk: Full parsing uses a MINERU_TOKEN credential. <br>
Mitigation: Store the token in the environment or the CLI's authentication flow and avoid hard-coding it into prompts, files, or shared logs. <br>


## Reference(s): <br>
- [PPTX Parse on ClawHub](https://clawhub.ai/mzlzyca/pptx-parse) <br>
- [MinerU Homepage](https://mineru.net) <br>
- [MinerU Token Management](https://mineru.net/apiManage/token) <br>
- [MinerU Project Reference](https://github.com/opendatalab/MinerU) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured Markdown from PPTX inputs; full parsing can require MINERU_TOKEN.] <br>

## Skill Version(s): <br>
0.4.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
