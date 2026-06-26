## Description: <br>
Merge multiple user-provided PDF files by uploading them to Cross-Service-Solutions, polling until completion, then returning a download URL for the merged PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrossServiceSolutions](https://clawhub.ai/user/CrossServiceSolutions) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and external users can use this skill to merge multiple PDF files through the Cross-Service-Solutions API and receive a structured result with the merged file download URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs are sent to a third-party API for processing. <br>
Mitigation: Use only documents appropriate for Cross-Service-Solutions processing, and review the provider's privacy, retention, and compliance terms before submitting confidential, regulated, legal, financial, or proprietary documents. <br>
Risk: The skill requires a Cross-Service-Solutions API key. <br>
Mitigation: Provide the key through the supported secret or environment flow and avoid echoing, logging, or embedding it in shared files. <br>


## Reference(s): <br>
- [Cross-Service-Solutions API Base URL](https://api.xss-cross-service-solutions.com/solutions/solutions) <br>
- [Cross-Service-Solutions API Key Registration](https://login.cross-service-solutions.com/register) <br>
- [Merge PDF ClawHub Release](https://clawhub.ai/CrossServiceSolutions/merge-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON result with job status, file metadata, input filenames, and merged PDF download URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires at least two PDF inputs and a user-provided Cross-Service-Solutions API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
