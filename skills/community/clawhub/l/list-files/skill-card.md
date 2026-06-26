## Description: <br>
List all files uploaded by this API key. Returns URL and creation timestamp, ordered newest first. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to retrieve PDF API Hub upload history and file URLs for dashboards, audits, pipeline monitoring, and cleanup planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an API key and the returned file list may expose private file URLs and upload history. <br>
Mitigation: Confirm trust in pdfapihub.com, use a least-privileged API key when available, and limit visibility of agent outputs that include file URLs. <br>


## Reference(s): <br>
- [PDF API Hub Documentation](https://pdfapihub.com/docs) <br>
- [PDF API Hub](https://pdfapihub.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/rishabhdugar/list-files) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, guidance] <br>
**Output Format:** [JSON response with file URLs and creation timestamps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns newest files first; the optional limit query parameter can cap results from 1 to 500.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
