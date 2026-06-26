## Description: <br>
Integrates with Ocean Engine advertising APIs to help agents manage campaigns, automate launches, monitor performance, and generate ROI-focused optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AQzzzQA](https://clawhub.ai/user/AQzzzQA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Advertising optimizers, digital marketing managers, media buyers, and technical teams use this skill to manage Ocean Engine campaigns, automate launches, monitor performance, and generate ROI-oriented optimization reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch paid advertisements and change budgets, bids, creative settings, or campaign state when configured with live Ocean Engine credentials. <br>
Mitigation: Use test mode first, require manual review before live launch or batch changes, and set external budget limits in the advertising platform. <br>
Risk: Credential handling can expose production access tokens or app secrets if local configuration is saved carelessly. <br>
Mitigation: Use least-privilege or limited-scope credentials where possible, prefer environment variables, and avoid calling save_config() with production secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AQzzzQA/oceanengine-ads) <br>
- [Ocean Engine developer platform](https://developer.oceanengine.com/) <br>
- [Ocean Engine technical blog](https://blog.oceanengine.com/) <br>
- [Ocean Engine developer forum](https://bbs.oceanengine.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, Python return dictionaries, and command-line text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external advertising APIs and may create or modify live ad platform resources when configured with live credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact metadata lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
