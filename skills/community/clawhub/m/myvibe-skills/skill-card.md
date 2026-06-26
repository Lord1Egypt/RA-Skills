## Description: <br>
Publish static HTML, ZIP archive, or directory to MyVibe. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuzhuyule](https://clawhub.ai/user/zhuzhuyule) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to prepare and publish static web content, ZIP archives, directories, or imported URLs to MyVibe. It helps an agent detect project shape, collect metadata, confirm publishing details, and run the publish workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local content and screenshots to MyVibe. <br>
Mitigation: Review the selected project for secrets, confirm the target files, and verify public or private visibility before publishing. <br>
Risk: The skill stores authorization state for the MyVibe hub. <br>
Mitigation: Use trusted hub URLs only and manage stored tokens according to the user's credential handling policy. <br>
Risk: The security evidence notes that a successful publish can delete a user-supplied config file. <br>
Mitigation: Use disposable config files or stdin-based configuration, and keep any important configuration in a separate source file. <br>
Risk: The workflow may install or rely on global browser automation tooling for screenshot generation. <br>
Mitigation: Run the workflow in a controlled environment and review installed dependencies before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuzhuyule/myvibe-skills) <br>
- [Publisher profile](https://clawhub.ai/user/zhuzhuyule) <br>
- [MyVibe hub](https://www.myvibe.so/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON publish configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent through network publishing, screenshot upload, metadata review, and visibility selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
