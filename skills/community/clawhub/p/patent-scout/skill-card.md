## Description: <br>
Searches Chinese patent information through Baidu or Google Patents by keyword or patent number and returns structured patent summaries, applicants, dates, legal status, and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yjstrivesh](https://clawhub.ai/user/yjstrivesh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and patent analysts use this skill to search Chinese patent information by keyword or CN patent number and collect structured summaries for technical research or prior-art review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Baidu-derived results are heuristic web-search results and may be incomplete or inaccurate. <br>
Mitigation: Verify important patent facts against an authoritative patent database before relying on them. <br>
Risk: Search queries may be sent to Baidu, Google Patents, and any configured proxy. <br>
Mitigation: Avoid searching confidential invention details unless those services and proxy paths are approved for the information. <br>
Risk: The skill installs npm dependencies before use. <br>
Mitigation: Review the dependency set and use the provided lockfile or an approved package mirror before installation. <br>


## Reference(s): <br>
- [Patent Scout on ClawHub](https://clawhub.ai/yjstrivesh/patent-scout) <br>
- [Baidu Search](https://www.baidu.com/) <br>
- [Google Patents](https://patents.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Shell commands] <br>
**Output Format:** [Markdown or JSON patent search summaries with optional file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are retrieved from Baidu or Google Patents and may include source links, applicant names, dates, legal status, IPC classes, and claims when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
