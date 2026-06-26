## Description: <br>
Create and share rich interactive artifacts such as webpages, markdown documents, and flowcharts as hosted links from any AI conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saibhaskardevatha](https://clawhub.ai/user/saibhaskardevatha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to publish, update, list, and collect feedback on shareable Orb artifacts from agent conversations. It is suited for dashboards, reports, charts, visualizations, interactive webpages, structured documents, and Mermaid flowcharts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Artifact content and uploaded image assets may be sent to Orb-hosted services. <br>
Mitigation: Confirm user intent before publishing confidential or business-sensitive material and return only the hosted artifact link. <br>
Risk: The skill asks agents to persist ORB_API_KEY in local configuration or shell files. <br>
Mitigation: Prefer a secure or session-only environment variable and avoid plaintext profile or config persistence unless the user deliberately accepts that risk. <br>


## Reference(s): <br>
- [Orb ClawHub Listing](https://clawhub.ai/saibhaskardevatha/orb) <br>
- [Orb Homepage](https://byorb.app) <br>
- [Orb API Base URL](https://api.byorb.app/v1) <br>
- [Orb Artifact Viewer](https://art.byorb.app/v/<id>) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with hosted links, inline bash curl commands, HTML/Markdown/Mermaid artifact content, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns hosted Orb artifact links rather than inline artifact payloads; requires ORB_API_KEY and curl.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact metadata version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
