## Description: <br>
Zenserp (zenserp.com). Use this skill for ANY Zenserp request - searching and reading data. Whenever a task involves Zenserp, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Zenserp search, image search, maps local search, and news search through an OOMOL-connected account. It is intended for retrieving structured search results through the oo CLI after inspecting each action's live schema. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and related parameters are sent to Zenserp and OOMOL services. <br>
Mitigation: Avoid submitting sensitive or confidential search terms unless that use is approved for the connected account. <br>
Risk: Zenserp actions may consume OOMOL account credit. <br>
Mitigation: Run actions only for intended searches and stop retrying when billing or insufficient-credit errors occur. <br>
Risk: The skill relies on the remote oo CLI installer and login flow for first-time setup. <br>
Mitigation: Install or authenticate only when required by command failure and only when the OOMOL provider is trusted. <br>


## Reference(s): <br>
- [ClawHub Zenserp skill page](https://clawhub.ai/oomol/oo-zenserp) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Zenserp homepage](https://zenserp.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include action data and meta.executionId when actions run successfully.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
