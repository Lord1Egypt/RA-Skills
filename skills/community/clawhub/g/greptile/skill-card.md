## Description: <br>
Query, search, and manage repositories indexed by Greptile for AI-assisted codebase intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iAhmadZain](https://clawhub.ai/user/iAhmadZain) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to index repositories in Greptile, check indexing status, ask codebase questions, and search for relevant source files and snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The status command can run unintended local code if crafted repository, branch, or remote values are supplied. <br>
Mitigation: Use only trusted repository, branch, and remote values with this version. <br>
Risk: Repository indexing and queries may expose code to Greptile. <br>
Mitigation: Index only code you are authorized to share with Greptile and prefer a fine-grained GitHub token limited to the intended repositories. <br>


## Reference(s): <br>
- [ClawHub Greptile skill page](https://clawhub.ai/iAhmadZain/greptile) <br>
- [Greptile app](https://app.greptile.com) <br>
- [Greptile API endpoint](https://api.greptile.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GREPTILE_TOKEN, a GitHub or Greptile GitHub token, and local curl, jq, and gh binaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
