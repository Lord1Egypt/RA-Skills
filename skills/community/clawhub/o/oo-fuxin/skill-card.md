## Description: <br>
Foxit Cloud API (cloudapi.fuxinsoft.cn). Use this skill for ANY Foxit Cloud API request - reading, creating, updating, and deleting data. Whenever a task involves Foxit Cloud API, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run Foxit Cloud API document workflows through an OOMOL-connected account, including conversion, compression, OCR, upload, download, page operations, protection, and task status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate Foxit Cloud API through an OOMOL-connected account, including actions that upload, merge, manipulate pages, or remove passwords. <br>
Mitigation: Install only when this account access is intended, and review every write or destructive action payload before approval. <br>
Risk: First-time setup may require installing or invoking the oo CLI. <br>
Mitigation: Verify the oo CLI installer before setup and use authentication or connection steps only when a command fails for that reason. <br>
Risk: Connector action schemas can change over time. <br>
Mitigation: Inspect the live action schema before constructing payloads so inputs match the current Foxit connector contract. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-fuxin) <br>
- [Foxit Cloud API homepage](https://cloudapi.fuxinsoft.cn) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include Foxit task data and an execution id under meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
