## Description: <br>
A minimal example skill demonstrating .clawhubignore - the secret.md file should NOT appear in the published version. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[TSHOGX](https://clawhub.ai/user/TSHOGX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers can use this example skill to test ClawHub packaging behavior and verify that ignore rules exclude files that should not be published. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The published artifact includes secret.md even though the skill text says that file should be excluded. <br>
Mitigation: Remove secret.md from the release, verify the ignore rules, and republish the skill. <br>
Risk: secret.md contains secret-like placeholder data that could indicate accidental disclosure if real values were ever published. <br>
Mitigation: Confirm the values are fake; rotate any real credential or sensitive path that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TSHOGX/hello-example) <br>
- [Publisher profile](https://clawhub.ai/user/TSHOGX) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution; published artifact content should be reviewed before reuse.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
