## Description: <br>
Optimize GitHub Actions workflows for speed, cost, security, and reliability \u2014 analyze run times, cache strategies, job parallelism, and runner selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to review GitHub Actions workflows, diagnose slow or costly CI runs, and receive optimization, security, and reliability recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested gh commands may use the current GitHub login to read workflow run metadata. <br>
Mitigation: Run commands only in the intended repository context and confirm the active GitHub account and token scope before use. <br>
Risk: Workflow edit recommendations can affect CI security, reliability, or cost if applied without review. <br>
Mitigation: Review proposed workflow changes, test them in a pull request, and apply repository security controls before merging. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with suggested workflow changes and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include speed, cost, security, and reliability findings for GitHub Actions workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
