## Description: <br>
Local-first data asset manager that helps scan, classify, and report on data before deciding what to share. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shangri-la-0428](https://clawhub.ai/user/Shangri-la-0428) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data owners, and operators use this skill to inventory local files, classify individual assets, and generate text or JSON reports before sharing or registering selected data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanning broad or sensitive directories can expose more local file inventory information than intended. <br>
Mitigation: Scan only intended folders, consider --no-recursive for sensitive locations, and review generated text or JSON reports before sharing them. <br>
Risk: The skill depends on an external Python package source. <br>
Mitigation: Install only from a trusted package source, use a virtual environment, and verify the installed package before use. <br>


## Reference(s): <br>
- [Oasyce package on PyPI](https://pypi.org/project/oasyce/) <br>
- [ClawHub skill listing](https://clawhub.ai/Shangri-la-0428/oasyce-vault) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to request or review text and JSON reports produced by the local datavault CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
