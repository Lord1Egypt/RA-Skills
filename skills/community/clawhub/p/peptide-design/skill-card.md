## Description: <br>
Peptide design, docking, and peptide property analysis tools exposed through SciMiner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, computational biologists, and peptide-design researchers use this skill to run SciMiner peptide docking, sequence-design, validation, and property-analysis workflows from documented SciMiner API tool docs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SciMiner API key stored locally. <br>
Mitigation: Store the key only at ~/.config/sciminer/credentials.json, do not print or commit it, and rotate it if exposure is suspected. <br>
Risk: SciMiner calls may upload user-selected scientific sequences, structures, or datasets to the service. <br>
Mitigation: Review selected files before invocation and do not submit confidential inputs unless SciMiner's data handling terms fit the use case. <br>


## Reference(s): <br>
- [ClawHub Peptide Design](https://clawhub.ai/sciminer/peptide-design) <br>
- [SciMiner Tool API Files](https://sciminer.tech/tool_api_files/) <br>
- [SciMiner API Key Utility](https://sciminer.tech/utility) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with inline JSON, invocation code or commands, task IDs, and SciMiner share_url links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local SciMiner API key and may upload user-selected scientific input files to SciMiner.] <br>

## Skill Version(s): <br>
1.0.7 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
