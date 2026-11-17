## Description: <br>
Knowlgdge-Skill helps agents process uploaded documents, assess their knowledge value, classify them with an LLM, generate fine-tuning datasets through EasyDataset, archive them in MongoDB, and retrieve answers from the local knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[somkh](https://clawhub.ai/user/somkh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to turn DOCX, PDF, Excel, image, Markdown, and text files into classified knowledge-base records and Alpaca-style datasets, then query the stored answers during later agent conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded documents and generated datasets may contain confidential or regulated information that is sent to configured LLM, vision, EasyDataset, or MongoDB services. <br>
Mitigation: Use only trusted and access-controlled services, keep deployments isolated to local or private networks, and avoid sensitive documents until data handling has been reviewed. <br>
Risk: EasyDataset on port 1717 and MongoDB on port 27017 can store or expose processed content if reachable by untrusted users. <br>
Mitigation: Do not expose these ports publicly; bind services to localhost or a private network and add authentication or network access controls where possible. <br>
Risk: Uploads, processed Markdown, and exported datasets can persist after processing. <br>
Mitigation: Define retention and deletion practices for upload, processed, dataset, and database storage before production use. <br>
Risk: Unpinned dependencies or container images can change behavior across installations. <br>
Mitigation: Pin Python dependencies and container image versions, then review installation steps before deploying in shared environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/somkh/skills/jy-knowlgdge-skill) <br>
- [Publisher profile](https://clawhub.ai/user/somkh) <br>
- [Skill architecture](docs/skill_architecture.md) <br>
- [Cold start guide](docs/cold_start.md) <br>
- [EasyDataset API reference](docs/easydataset_api.md) <br>
- [EasyDataset and MongoDB deployment guide](docs/easydataset_deploy.md) <br>
- [Troubleshooting guide](docs/troubleshooting.md) <br>
- [EasyDataset repository](https://github.com/ConardLi/easy-dataset.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and generated dataset files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output is answer-only text with a documented 45000-character cap; generated datasets are exported locally as JSON records after chain-of-thought fields are removed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
